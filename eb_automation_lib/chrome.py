import re
from time import sleep

# third party dependecies
from ScriptingBridge import SBApplication

from .task import Task, Queue

# utilites and helpers from the automation library
from .utils.helper_functions import *
from .utils.helper_functions import (
    eventbrite_url_constructor,
    get_javascript_from_file
)
from .utils.window_helpers import (
    get_window_size,
    create_window_position,
    set_window_size_by_percent
)


class Chrome(object):
    """
        Chrome uses the pyobjc scripting bridge to osascript to do actions. Chrome is given access to an
        SBApplication object instance of Google Chrome and implements several useful methods to auotmate
        the browser.

        ==============================
        INFORMATION ABOUT THIS LIBRARY
        ==============================

        -----------------------------------------------
                # indicates a comment that contains information about what happened in an example,
        -----------------------------------------------

        -----------------------------------------------
                #---
                # This indicates a heading for a group of methods and contains
                # information about the group / section, and how to use it in your scripts
                #---
        -----------------------------------------------

        -----------------------------------------------
                The following indicates an example on how a method can be used in your script.
                Here, # describes the result of calling that method if there is no return value,
                or the return value is considered a side effect

                >>>chrome = Chrome()
                >>>chrome.search_eventbrite_admin("customer@email.com")  # a new tab is opened at admin.eventbrite.com
        -----------------------------------------------
    """

    # ---------------------------------------------------
    # The methods here at the top are meant for direct use in the automation hackathon course and are
    # intended to serve as an example for how to build your own automations and provide some useful,
    # high-level building-blocks suited for common Eventbrite workflows.
    # ---------------------------------------------------
    def get_eventbrite_tab(self):
        """returns the first eventbrite tab object"""
        eventbrite_tabs = self.tabs_with_urls_that_contain_pattern("eventbrite")
        if eventbrite_tabs:
            return eventbrite_tabs[0]

    def get_salesforce_tab(self):
        """returns the first salesforce tab object"""
        salesforce_tabs = self.tabs_with_urls_that_contain_pattern("salesforce")
        if salesforce_tabs:
            return salesforce_tabs[0]

    # ---------------------------------------------------
    # The methods below are building block methods. They're useful for building more customized automations
    # from scratch, or that aren't specific to the primary Eventbrite workflows
    # ---------------------------------------------------

    def active_tab(self, window_index=0):
        """returns the tab that currently has focus i.e. the front-most tab"""
        return self.windows()[window_index].activeTab()

    def new_tab(self, url=None, window_index=0):
        """create a new tab, returns the tab"""
        props = {}
        if url:
            props['URL'] = url

        tab = self._create_tab_object(properties=props)
        self._append_tab_to_window(tab, window_index=window_index)
        return tab

    def new_window(self, url=None, window_props={}):
        """create a new window. If url is specified, the tab is set to that location
        returns the window and tab
        """
        window = self._create_window_object(properties=window_props)
        self._append_window_to_application(window)
        if url:
            tab = self.new_tab({"URL": url}, window_index=window.index())
            return window, tab

        return window, window.tabs()[0]

    def open_event_page_location(self, event_id, path):
        """convenience method for opening various event pages (ie manage, waitlist etc)"""
        if is_event_id(event_id):
            url = eventbrite_url_constructor(path, parameters={"eid": event_id})
            return self.new_tab(url)
        else:
            raise ValueError("{} is not a valid Eventbrite Event ID".format(event_id))

    def set_tab_url_to(self, tab, url):
        """uses js to send a tab to a new url"""
        self._execute_javascript_in_tab(tab, """window.location = {}""".format(url))

    @staticmethod
    def set_window_position_to(window, position=('upper', 'right')):
        """set the position a window to ('upper', 'left'), ('lower', 'left'),
        ('upper', 'right'), or ('lower', 'right')
        """
        window.setPosition_(
            create_window_position(get_window_size(window), position)
        )

    def tabs(self):
        """returns a list of tab objects for each tab in each window"""
        return [tab for window in self.windows() for tab in window.tabs()]

    def tabs_at_url(self, url):
        """
        returns a list of tab ojbects whose url's are an exact match for the url argument
        >>> chrome.tabs_at_url("https://www.eventbrite.com/myevent?eid=12345678901")
        <TAB OBJECT>
        """
        return [tab for tab in self.tabs() if url == tab.URL()]

    def tabs_with_urls_that_contain_pattern(self, pattern):
        """
        returns a list of tab objects whose urls match a pattern. It can be a simple, or complex pattern
        >>>evbqa_tabs = chrome.tabs_with_urls_that_contain_pattern("evbqa")
        >>>for tab in evbqa_tabs:
        ...   print(tab.id() + ": " + tab.URL())
        581: https://www.evbqa.com/e/my-special-event-32345678901
        596: https://www.evbqa.com/myevent?eid=32345678901
        597: https://admin.evbqa.co.uk
        """
        return [t for t in self.tabs() if re.search(pattern, t.URL())]

    def vertical_split_window(self, window_index, side="left"):
        """resizes the window at window index and positions it to the left or right side"""
        return set_window_size_by_percent(self.windows(window_index), 50, 100, position=("upper", side))

    def windows(self, index=None):
        """returns a list of all open window objects or the window at the specified index"""
        windows = self.driver.windows()
        return windows[index] if index is not None else windows

    # - - - - - - - - - - - - - - - - - - - - - - - -
    # the methods below are NOT MEANT FOR USE IN THE HACKATHON COURSE.
    # use at your own risk, or ask for help if you have any questions!
    # - - - - - - - - - - - - - - - - - - - - - - - -

    def _append_tab_to_window(self, tab_object, window_index=0):
        """push an initialized tab onto a window's tabs array"""
        self.windows()[window_index].tabs().append(tab_object)

    def _append_window_to_application(self, window_object):
        """add an initialized window to chrome"""
        self.windows().append(window_object)

    def _block_until_loaded(self, tab):
        while tab.loading():
            pass

    def _click_DOM_element(self, tab, element_id):
        """use javascript to click an element in a tab's DOM"""
        js = get_javascript_from_file("./javascript/snippets.js", export="clickElement")
        self._execute_javascript_in_tab(tab, js)

    def _create_tab_object(self, properties={}):
        """
        returns an allocated and initialized tab object
        call this with a properties dict to initialize the tab at a url
        >>>self._create_tab_object({ "URL": "https://www.eventbrite.com/" })
        <GoogleChromeTab object>
        """
        return self.driver.classForScriptingClass_("tab").alloc().initWithProperties_(properties)

    def _create_window_object(self, properties={}):
        """returns an allocated and initialized pyobjc window object"""
        return self.driver.classForScriptingClass_("window").alloc().initWithProperties_(properties)

    def _do_after_tab_loads(self, tab, callback, *callback_args):
        """asynchronously waits for the tab to load, then calls the callback
        NOTE: not safe for executing javascript in multiple tabs at once
        """
        def do():
            self._block_until_loaded(tab)
            callback(*callback_args)
        self.queue.put(Task(do))

    def _execute_javascript_in_tab(self, tab, javascript):
        """asynchronously executes javascript in the given tab
        NOTE: this method is not safe to use inside iterators
        """
        def do():
            self._block_until_loaded(tab)
            tab.executeJavasctipt_(javascript)
        self.queue.put(Task(do))

    def __str__(self):
        return "GoogleChrome App Scripting Bridge - {win} open windows, {tab} total tabs".format(
            win=len(self.windows()),
            tab=len([tab for window in self.windows() for tab in window.tabs()])
        )

    def __init__(self):
        self.driver = SBApplication.applicationWithBundleIdentifier_("com.google.Chrome")
        self.queue = Queue(max_workers=4)
