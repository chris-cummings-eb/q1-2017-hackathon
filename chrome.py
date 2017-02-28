# modules from the python standard library
from itertools import chain
from time import sleep

# third party dependecies
from ScriptingBridge import SBApplication


class Chrome(object):
    """
        Chrome uses the pyobjc scripting bridge to osascript to do actions. Chrome is given access to a
        SBApplication object instance of Google Chrome and implements several useful methods to auotmate
        the browser.

        USAGE EXAMPLE:
        >>>chrome = Chrome()
        >>>chrome.list_tabs_at_url_partial("www.eventbrite")
        [LIST OF TAB OBJECTS]
    """

    def __init__(self):
        self.driver = SBApplication.applicationWithBundleIdentifier_("com.google.Chrome")

    def active_tab(self, window_index):
        return self.windows()[window_index].activeTab()

    def do_after_tab_loads(self, tab, callback, *args):
        while tab.loading():
            sleep(.5)
        callback(*args)

    def execute_javascript_in_tab(self, tab, javascript):
        tab.executeJavascript_(javascript)

    def list_tabs_at_url(self, url):
        """
        returns a list of tabs whose url's are an exact match for the url argument
        USAGE EXAMPLE:
        >>> chrome.list_tabs_at_url("https://www.eventbrite.com/myevent?eid=12345678901")
        <TAB OBJECT>
        """
        return [tab for tab in self.list_all_tabs() if url == tab.URL()]

    def list_tabs_at_url_partial(self, url):
        """
        same as list_tabs_at_url except the url argument can be a partial match
        """
        return [t for t in self.list_all_tabs() if url in t.URL()]

    def list_all_tabs(self):
        return [tab for window in self.windows() for tab in window.tabs()]

    def new_tab_at_url(self, url, window_index=0):
        tab = self.driver.classForScriptingClass_("tab").alloc().initWithProperties_({"URL": url})
        self.windows()[window_index].tabs().append(tab)
        return tab

    def windows(self):
        return self.driver.windows()
