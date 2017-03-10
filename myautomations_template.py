from eb_automation_lib.chrome import Chrome
from eb_automation_lib import eb_wrapper as ebapi

chrome = Chrome()
eventbrite = ebapi.Eventbrite('YOUR TOKEN')


def open_google():
    chrome.new_tab(url='http://www.google.com')
    chrome.open_event_page_location()

# ---------------------------
# Put your automations below:
# ---------------------------


# this runs when you type the following in your terminal
# python my_automations.py
if __name__ == '__main__':
    open_google()
