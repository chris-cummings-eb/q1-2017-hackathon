from time import sleep


from eb_automation_lib.chrome import Chrome
from eb_automation_lib.dashboard.automator_dashboard import start_dashboard
from eb_automation_lib import Task, Queue

automation_modules = []

# HOW TO ADD YOUR OWN AUTOMATIONS TO THE DASHBOARD
"""
import my_automations  # import your modules

# then append each of your modules to the automation_modules list.
automation_modules.append(my_automations)
"""

task_queue = Queue()
task_queue.start_work()
task_queue.put(Task(
    start_dashboard,
    args=(automation_modules,)
))

chrome = Chrome()
tab = chrome.tabs_with_urls_that_contain_pattern('/dashboard')
if tab:
    tab = tab[0]
    chrome.driver.activate()
else:
    chrome.driver.activate()
    tab = chrome.tabs()[0]
    while tab.loading():
        sleep(.1)
    chrome._execute_javascript_in_tab(
        tab,
        """
        console.log('in')
        window.open(
            'http://localhost:5555/dashboard',
            'Eventbrite Automator Dashboard',
            'width=400,height=770,resizable,status=0,toolbar=no,menubar=no'
        )
        """
    )


task_queue.join()
