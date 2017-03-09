@SOCKET_IO.on('connect')
def update_automations():
    emit(
        'automations_list_update',
        {'automations': SERVER.automations_list},
        broadcast=True
     )


@SOCKET_IO.on('dispatch')
def dispatch_automation(data):
    to_dispatch = data.get('automations')

    for automation in to_dispatch:
        module, *_ = [m for m in SERVER.automation_modules if m.__name__ == automation['module']]
        automation_args = automation['args'] if automation['args'] else ()

        def automation_func(*args):
            SERVER.toggle_automation_status(automation['id'])
            f = getattr(module, automation['object_name'])
            f(*args)
            SERVER.toggle_automation_status(automation['id'])

        SERVER.dispatch(Task(automation_func, automation_args, description=automation['description']))

    emit(
        'automations_list_update',
        {'automations': SERVER.automations_list},
        broadcast=True
     )


@SERVER.route('/dashboard', methods=['GET'])
def dashboard_handeler():
    return render_template('index.html')
