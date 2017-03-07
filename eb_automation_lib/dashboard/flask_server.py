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

server = Flask(
    __name__.split('.')[0],
)

server.config['SECRET_KEY'] = 'lolwut!'
socketio = SocketIO(server)


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
    emit('connected yo')


@server.route('/dashboard', methods=['GET'])
def dashboard_handeler():
    return render_template('index.html')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
