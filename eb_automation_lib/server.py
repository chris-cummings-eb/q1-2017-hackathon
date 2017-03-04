from flask import Flask, request
server = Flask(__name__)

LAST_REQUEST = "error"


@server.route("/", methods=["POST"])
def handler():
    value = request.form.get("value")
    if value:
        LAST_REQUEST = value
        with open("reqests.txt", w) as f:
            f.write(value)
        return "received"
    else:
        LAST_REQUEST = "error"
        return "error"


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == "__main__":
    server.run()
