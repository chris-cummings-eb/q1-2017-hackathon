import importlib.util
import re
from inspect import getmembers, isfunction

from flask import (
    Flask,
    render_template,
    request
)
from flask_socketio import (
    emit,
    send,
    SocketIO
)

from ..utils import import_utils
from . import default_automations

server = Flask(
    __name__.split('.')[0],
)

server.config['SECRET_KEY'] = 'lolwut!'
socketio = SocketIO(server)


def get_automations(module_list=[], include_defaults=True):
    """returns a list of meta information about the functions in each module in module_list
    plus the functions in the default_automations module of this package. if include_defaults=False
    default_automations functions will not be included
    """
    modules = module_list + [default_automations] if include_defaults else module_list
    return [
            {
                'id': '{}-{}-{}'.format(module.__name__, obj.__name__, index)',
                'name': import_utils.display_name(obj),
                'description': import_utils.description(obj),
                'module': module.__name__,
                'object_name': obj.__name__,
                'icon': import_utils.icon_type(obj),
                'dispatched': False
            }
            for index, module in enumerate(modules)
            for _, obj in getmembers(module, isfunction)
            ]


def run_server(port=None, static_path=None, template_path=None):
    server.template_folder = "{root}/{template}".format(
        root=server.root_path,
        template='/dashboard/static/javascript/dist/' if template_path is None else template_path,
    )
    server.static_folder = "{root}/{static}".format(
        root=server.root_path,
        static='/dashboard/static/javascript/dist/' if static_path is None else static_path
    )
    socketio.run(
        server,
        port=port
    )


@socketio.on('connect')
def handle_connect():
    emit(
        'automations_list_update',
        {'automations': get_automations()},
        broadcast=True
     )


@server.route('/dashboard', methods=['GET'])
def dashboard_handeler():
    return render_template('index.html')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
