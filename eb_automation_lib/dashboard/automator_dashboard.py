from collections import deque
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

from ..utils import import_utils, clipboard
from ..utils.helper_functions import string_contains_tags, extract_eb_vals
from ..task import Queue, Task
from .. import default_automations


def _serialize(module_list=[], include_defaults=True):
    """returns a list of meta information about the functions in each module at the file paths in module_list
    plus the functions in the default_automations module of this package. if include_defaults=False
    default_automations functions will not be included
    """
    modules = [import_utils.get_module_from_filepath(module) for module in module_list]
    if include_defaults:
        modules.append(default_automations)

    return [
            {
                'id': '{}-{}-{}'.format(module.__name__, obj.__name__, index),
                'name': import_utils.display_name(obj),
                'description': import_utils.description(obj),
                'module': module.__name__,
                'object_name': obj.__name__,
                'args': import_utils.get_args(obj),
                'icon': import_utils.icon_type(obj),
                'tags': import_utils.tag_type(obj),
                'dispatched': False,
                'hidden': False,
                'filtered': False
            }
            for index, module in enumerate(modules)
            for _, obj in getmembers(module, isfunction)
            ]


class AutomatorDashboard(Flask):
    def __init__(self, your_modules=[], include_defaults=True):
        Flask.__init__(self, __name__.split('.')[0])

        self.automations_list = _serialize(module_list=your_modules, include_defaults=include_defaults)
        self.automation_modules = your_modules
        self.include_defautls = include_defaults
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
            automation_args_meta = automation.get('args')
            automation_args = extract_eb_vals(clipboard.get_clipboard())[:len(automation_args_meta)]

            def do(*args):
                self.toggle_automation_status(automation.get('id'))
                f = getattr(module, automation.get('object_name'))
                f(*args)
                self.toggle_automation_status(automation.get('id'))

            self.queue.put(Task(do, args=automation_args, description=automation.get('description')))

        if callable(callback):
            return callback(*cb_args)

        return

    def refresh_automations_list(self, *args, callback=None):
        self.automations_list = args[0]
        if callable(callback):
            callback(*args)

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
    def __init__(self, callbacks={}, args={}, namespace='/'):
        Namespace.__init__(self, namespace=namespace)
        self.callbacks = callbacks
        self.args = args

    def on_connect(self):
        automations_list = self.args.get('dispatch')
        value = clipboard.get_clipboard()
        emit(
            'automations_list_update',
            {
                'automations': automations_list,
                'clipboard': value,
                'tags': string_contains_tags(value)
            }
         )

    def on_dispatch(self, data):
        def emit_cb(*args):
            automations_list = self.args.get('dispatch')
            emit('automations_list_update', {'automations': automations_list})

        do = self.callbacks.get('dispatch')
        do(data, callback=emit_cb, cb_args=self.args.get('dispatch'))

    def on_refresh(self):
        def emit_cb(*args):
            args = self.args.get('refresh')
            emit('automations_list_update', {'automations': args[0]})

        do = self.callbacks.get('refresh')
        do(self.args.get('refresh'), callback=emit_cb)


def monitor_clipboard(on_change):
    pb = clipboard.OS_CLIPBOARD
    old_change_count = pb.changeCount()
    while True:
        time.sleep(.5)
        new_change_count = pb.changeCount()
        if new_change_count != old_change_count:
            old_change_count = new_change_count
            value = clipboard.get_clipboard()
            data = {
                'clipboard': value,
                'tags': string_contains_tags(value)
                }
            on_change('clipboard', data, namespace='/')


def start_dashboard(your_modules=[], include_defaults=True, port=5555):
    server = AutomatorDashboard(your_modules, include_defaults=include_defaults)
    socketio = SocketIO(server, async_mode='threading')
    socketio.on_namespace(DashboardMessages(
        callbacks={'dispatch': server.dispatch, 'refresh': server.refresh_automations_list},
        args={'dispatch': (server.automations_list),
              'refresh': (_serialize(module_list=server.automation_modules, include_defaults=server.include_defautls))}
    ))

    def do():
        with server.test_request_context('/'):
            monitor_clipboard(socketio.emit)

    server.queue.put(Task(do))
    socketio.run(server, port=port)
