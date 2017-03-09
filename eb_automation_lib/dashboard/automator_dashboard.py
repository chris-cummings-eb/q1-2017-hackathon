import importlib.util
from inspect import getmembers, isfunction
import re
import time

from flask import (
    Flask,
    render_template,
    request
)
from flask.views import View
from flask_socketio import (
    emit,
    Namespace,
    send,
    SocketIO
)

from ..utils import import_utils
from ..task import Queue, Task
from .. import default_automations


def _serialize(module_list=[], include_defaults=True):
    """returns a list of meta information about the functions in each module in module_list
    plus the functions in the default_automations module of this package. if include_defaults=False
    default_automations functions will not be included
    """
    modules = module_list + [default_automations] if include_defaults else module_list
    return [
            {
                'id': '{}-{}-{}'.format(module.__name__, obj.__name__, index),
                'name': import_utils.display_name(obj),
                'description': import_utils.description(obj),
                'module': module.__name__,
                'object_name': obj.__name__,
                'args': None,
                'icon': import_utils.icon_type(obj),
                'dispatched': False
            }
            for index, module in enumerate(modules)
            for _, obj in getmembers(module, isfunction)
            ]


class AutomatorDashboard(Flask):
    def __init__(self, your_modules=[], include_defaults=True):
        Flask.__init__(self, __name__.split('.')[0])

        self.automations_list = _serialize(module_list=your_modules, include_defaults=include_defaults)
        self.automation_modules = your_modules + [default_automations] if include_defaults else your_modules
        self.queue = Queue(max_workers=4)
        self.queue.start_work()

        self.template_folder = "{root}/{template}".format(
            root=self.root_path,
            template='/dashboard/static/javascript/dist/'
        )
        self.static_folder = "{root}/{static}".format(
            root=self.root_path,
            static='/dashboard/static/javascript/dist/'
        )

        self.add_url_rule(
            '/dashboard',
            view_func=TemplateView.as_view('dashboard', template_name='index.html')
        )

    def dispatch(self, data, callback=None, cb_args=()):
        for automation in data.get('automations'):
            module, *_ = [m for m in self.automation_modules if m.__name__ == automation.get('module')]
            automation_args = automation.get('args') or ()

            def do(*args):
                self.toggle_automation_status(automation.get('id'))
                f = getattr(module, automation.get('object_name'))
                f(*args)
                self.toggle_automation_status(automation.get('id'))

            self.queue.put(Task(do, automation_args, description=automation.get('description')))

        if callable(callback):
            return callback(*cb_args)

        return

    def toggle_automation_status(self, automation_ids):
        if isinstance(automation_ids, str):
            automation_ids = [automation_ids]

        updated_list = []
        for num in automation_ids:
            for automation in self.automations_list:
                if automation['id'] == num:
                    automation['dispatched'] = not automation.get('dispatched')

            updated_list.append(automation)


class TemplateView(View):
    def __init__(self, template_name='index.html'):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)


class DashboardMessages(Namespace):
    def __init__(self, dispatch_func, *args, namespace='/'):
        Namespace.__init__(self, namespace=namespace)
        self.dispatch_func = dispatch_func
        self.dispatch_cb_args = args

    def on_connect(self):
        automations_list, *_ = self.dispatch_cb_args
        emit(
            'automations_list_update',
            {'automations': automations_list},
            broadcast=True
         )

    def on_dispatch(self, data):
        def emit_cb(*args):
            automations_list, *_ = args
            emit('automations_list_update', {'automations': automations_list}, broadcast=True)

        self.dispatch_func(data, emit_cb, cb_args=self.dispatch_cb_args)


def start_dashboard(your_modules=[], include_defaults=True, port=5555):
    server = AutomatorDashboard(your_modules, include_defaults=include_defaults)
    socketio = SocketIO(server)
    socketio.on_namespace(DashboardMessages(server.dispatch, server.automations_list))
    socketio.run(server, port=port)
