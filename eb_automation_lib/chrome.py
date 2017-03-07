import re
from time import sleep
from urllib.parse import quote_plus

# third party dependecies
from ScriptingBridge import SBApplication

# utilites and helpers from the automation library
from .utils.helper_functions import *
from .utils.window_helpers import (
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
    #
    # PROTIP: Take advantage of the open_event_[LOCATION]_page methods in the next section
    # ---------------------------------------------------
    def open_salesforce_eventbrite_admin_side_by_side(self, salesforce_query, eventbrite_query):
        """A sample method for how to view two customized things at once"""

        sf_win, sf_tab = self.new_window_with_tab(url="https://salesforce.com")
        eb_win, eb_tab = self.new_window_with_tab(url=admin_search_url(eventbrite_query))
        self.vertical_split_window(window=sf_win, side="left")
        self.vertical_split_window(window=eb_win, side="right")

        return sf_tab, eb_tab

    def get_eventbrite_tab(self):
        """returns the first eventbrite tab object"""
        eventbrite_tabs = self.tabs_with_urls_that_contain_pattern("eventbrite")[0]
        if eventbrite_tabs:
            return eventbrite_tabs[0]

    def get_salesforce_tab(self):
        """returns the first salesforce tab object"""
        salesforce_tabs = self.tabs_with_urls_that_contain_pattern("salesforce")
        if salesforce_tabs:
            return salesforce_tabs[0]

    def order_lookup(self, orders, environment="production"):
        """
        opens a new tab in Evenbrite Admin Order Lookup, searching the list of orders
        returns the tab object or the created tab
        """
        if not isinstance(orders, list):
            orders = [orders]

        url = eventbrite_url_constructor(
            "admin/orderinfo/",
            parameters={"order_id": ",".join(orders)}
        )
        for order in orders:
            if not is_order_id(order):
                raise ValueError("Order list contains invalid order ids. {} is not an order id".format(order))

        return self.new_tab_at_url(url)

    def search_eventbrite_admin(self, query, environment="production", new_tab=True):
        """opens a new tab in Eventbrite Admin search, returns the tab object for the created tab"""
        url = admin_search_url(query)
        if new_tab:
            return self.new_tab_at_url(url)
        else:
            admin_tabs = self.tabs_with_urls_that_contain_pattern("admin.eventbrite")
            if admin_tabs:
                admin_tab = admin_tabs[0]
                admin_tab._set_tab_url_to(url)
                return admin_tab
            else:
                return self.new_tab_at_url(url)

    # ---------------------------------------------------
    # open_event_[LOCATION] methods simply take an event_id and open a new tab at that location.
    # These methods were made for you to quickly maneuver about the eventbrite platform in your automations
    # all of the methods in this section return the tab object that they create
    # ---------------------------------------------------

    def open_event_listing(self, event_id, environment="production", parameters=None):
        """opens a new tab at the event's listing page, returns the tab object for the created tab"""
        return self._open_event_page_location(event_id, "e")

    def open_event_edit_page(self, event_id, environment="production"):
        """opens a new tab on the Edit Page of an event id, returns the tab object"""
        return self._open_event_page_location(event_id, "edit")

    def open_event_manage_page(self, event_id, environment="production"):
        """opens a new tab on the Manage Page of an event id, returns the tab object"""
        return self._open_event_page_location(event_id, "myevent")

    # --------
    # TODO: add all of the location methods
    # --------

    # ---------------------------------------------------
    # The methods below are building block methods. They're useful for building more customized automations
    # from scratch, or that aren't specific to the primary Eventbrite workflows
    # ---------------------------------------------------

    def active_tab(self, window_index=0):
        """
        returns the tab that currently has focus i.e. the front-most tab
        """
        return self.windows()[window_index].activeTab()

    def new_tab_at_url(self, url, window_index=0):
        """opens a new tab in a window at the specified url, returns the new tab object"""
        tab = self._create_tab_object({
            "URL": url
        })
        self._append_tab_to_window(tab, window_index)

        return tab

    def new_window_with_tab(self, url=None):
        """creates a new window with a tab open at the specified url, returns the window and the tab"""
        window = self._create_window_object()

        if url is not None:
            # create new tab at url
            tab = self._create_tab_object({"URL": url})

        self._append_window_to_application(window)
        self._append_tab_to_window(tab)

        # close default tab if new tab was created
        tabs = window.tabs()
        if len(tabs) > 1:
            tabs[0].close()

        return window, tab

    def vertical_split_window(self, side="left", window=0):
        """resizes the window passed in or at the window_index and returns the size data"""
        if isinstance(window, int):
            window = self.windows(window)
        return set_window_size_by_percent(window, 50, 100, position=("upper", side))

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
        """effectively, this method is just "drawing" the window"""
        self.windows().append(window_object)

    @staticmethod
    def _click_DOM_element(tab, element_id):
        """use javascript to click an element in a tab's DOM"""
        js = get_javascript_from_file("./javascript/snippets.js", export="clickElement")
        tab.executeJavasctipt_(js)

    def _create_tab_object(self, properties={}):
        """
        helper method to allocate and initialze tab objects
        call this with a properties dict to initialize the object with props
        URL is actually the only writeable property...
        >>>self._create_tab_object({ "URL": "https://www.eventbrite.com/" })
        <GoogleChromeTab object>
        """
        return self.driver.classForScriptingClass_("tab").alloc().initWithProperties_(properties)

    def _create_window_object(self, properties={}):
        return self.driver.classForScriptingClass_("window").alloc().initWithProperties_(properties)

    def _open_event_page_location(self, event_id, path):
        """convenience helper method for opening various event pages (ie manage, waitlist etc)"""
        if is_event_id(event_id):

            url = eventbrite_url_constructor(path, parameters={"eid": event_id})
            return self.new_tab_at_url(url)

        else:
            raise ValueError("{} is not a valid Eventbrite Event ID".format(event_id))

    @staticmethod
    def _do_after_tab_loads(tab, callback, *args, **kwargs):
        """
        checks the loading status of the tab every 1/10th of a second, calls the callback function
        and returns that value after the tab has finished loading
        """
        while tab.loading():
            sleep(.1)

        return callback(*args, **kwargs)

    @staticmethod
    def _execute_javascript_in_tab(tab, javascript):
        """convenience method for calling the executeJavasctipt_ method on tab objects"""
        return tab.executeJavascript_(javascript)

    @staticmethod
    def _set_tab_url_to(tab, url):
        """convenience method for using js to move a tab to a new url"""
        tab.executeJavascript_("""window.location = {}""".format(url))

    @staticmethod
    def _set_window_position_to(window, position=[0, 0]):
        """set the position of a window object in pixels"""
        window.setPosition_(position)

    def __str__(self):
        return "GoogleChrome App Scripting Bridge - {win} open windows, {tab} total tabs".format(
            win=len(self.windows()),
            tab=len([tab for window in self.windows() for tab in window.tabs()])
        )

    def __init__(self):
        self.driver = SBApplication.applicationWithBundleIdentifier_("com.google.Chrome")
