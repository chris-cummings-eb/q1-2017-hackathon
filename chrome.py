# modules from the python standard library
import re
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

    def active_tab(self, window_index=0):
        """
        returns the tab that currently has focus i.e. the front-most tab
        """
        return self.windows()[window_index].activeTab()

    def new_tab_at_url(self, url, window_index=0):
        """
        opens a new tab in a window at the specified url
        returns the new tab object
        """
        tab = self._create_tab_object({
            "URL": url
        })
        self._append_tab_to_window(window_index)

        return tab

    def new_window_with_tab_at_url(self, url):
        """
        creates a new window with a tab open at the specified url
        returns the new tab object
        """
        window = self._create_window_object()
        tab = self._create_tab_object({
            "URL": url
        })
        self._append_window_to_application(window)
        self._append_tab_to_window(tab)

        return tab

    def tabs(self):
        """
        returns a list of tab objects for each tab in each window
        """
        return [tab for window in self.windows() for tab in window.tabs()]

    def tabs_at_url(self, url):
        """
        returns a list of tab ojbects whose url's are an exact match for the url argument
        USAGE EXAMPLE:
        >>> chrome.tabs_at_url("https://www.eventbrite.com/myevent?eid=12345678901")
        <TAB OBJECT>
        """
        return [tab for tab in self.tabs() if url == tab.URL()]

    def tabs_with_urls_that_contain_pattern(self, pattern):
        """
        returns a list of tab objects whose urls match a pattern. It can be a simple, or complex pattern
        USAGE EXAMPLE:
        >>>evbqa_tabs = chrome.tabs_with_urls_that_contain_pattern("evbqa")
        >>>for tab in evbqa_tabs:
        ...   print(tab.id() + ": " + tab.URL())
        581: https://www.evbqa.com/e/my-special-event-32345678901
        596: https://www.evbqa.com/myevent?eid=32345678901
        597: https://admin.evbqa.co.uk
        """
        return [t for t in self.tabs() if re.search(pattern, t.URL())]

    def windows(self):
        """
        returns a list of all open window objects
        """
        return self.driver.windows()

    # - - - - - - - - - - - - - - - - - - - - - - - -
    # lower level methods below are not meant for direct use in the automation class.
    # use at your own risk, or ask for help if you have any questions!
    # - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self):
        self.driver = SBApplication.applicationWithBundleIdentifier_("com.google.Chrome")

    def _append_tab_to_window(self, tab_object, window_index=0):
        self.windows()[window_index].tabs().append(tab_object)

    def _append_window_to_application(self, window_object):
        self.windows().append(window_object)

    def _create_tab_object(self, properties={}):
        """
        call this with a properties dict to initialize the object with props
        example:
        self._create_tab_object({
            "URL": "https://www.eventbrite.com/"
        })
        """
        return self.driver.classForScriptingClass_("tab").alloc().initWithProperties_(properties)

    def _create_window_object(self, properties={}):
        return self.driver.classForScriptingClass_("window").alloc().initWithProperties_(properties)

    def _do_after_tab_loads(self, tab, callback, *args):
        """
        checks the loading status of the tab every 1/10th of a second, calls the callback function
        and returns that value after the tab has finished loading
        """
        while tab.loading():
            sleep(.1)

        return callback(*args)

    def _execute_javascript_in_tab(self, tab, javascript):
        """
        just a convenience method for calling the executeJavasctipt_ method on tab objects
        """
        return tab.executeJavascript_(javascript)

    def _get_clipboard_script(self):
        """
        helper method that gets the clipboard library to make extracting values from the dom possible
        via the system clipboard
        meant to be used in combo with other javascript executed in a tab
        """
        return self._get_javascript_from_file("vendor/clipboard.min.js", export="ALL")

    @staticmethod
    def _get_javascript_from_file(filename, export="ALL"):
        """
            returns the entire javascript file unless exports is specificed, in which case the first
            declaration that matches the string passed into exports will be returned
            exmple:
            >>> chrome._get_javascript_from_file("js_snippet.js", export="myFunction")
            function myFunction(arg1) {
                // contnent of js function
            }

            ---
            export accepts
            "ALL" -> return the whole file
            "default" -> return the default export
            "name" -> return the first declaration by name
        """

        DECLARATION_REGEX = r"(let|const|var|function)\s\w+"

        with open("./javascript/" + filename, "r") as f:
            content = f.readlines()

            if export == "ALL":
                return "".join(content)

            name_to_export = export

            if name_to_export.lower() == "default":
                for line in content[::-1]:
                    if "export default" in line:
                        name_to_export = line.split(" ")[-1].replace(";", "").strip()
                        break

            left_brackets, right_brackets = 0, 0
            lines_to_export = []
            for line in content:

                declaration = re.search(DECLARATION_REGEX, line)

                if declaration and name_to_export in declaration.group(0):
                    lines_to_export.append(line)

                    left_brackets += line.count("{")
                    right_brackets += line.count("}")

                    if line[-1] == ";":
                        break

                elif lines_to_export:
                    lines_to_export.append(line)

                    left_brackets += line.count("{")
                    right_brackets += line.count("}")

                    if left_brackets == right_brackets:
                        break
            else:
                return

            return "".join(lines_to_export)
