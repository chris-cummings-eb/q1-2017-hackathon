from eb_automation_lib.chrome import Chrome

chrome = Chrome()

def open_google():
    chrome.new_tab(url='http://google.com')
