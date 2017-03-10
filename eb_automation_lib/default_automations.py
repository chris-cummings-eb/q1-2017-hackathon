from .chrome import Chrome
from .utils.helper_functions import (
    admin_search_url,
    eventbrite_url_constructor
)
chrome = Chrome()


def open_event_listing(event_id, environment="production", parameters=None):
    """opens a new tab at the event's listing page, returns the tab object for the created tab
    ##NAME: Open Event Page
    ##DESCRIPTION: open an event page when an eid is on clipboard
    ##TAGS: event
    ##ICON: chrome
    """
    return chrome._open_event_page_location(event_id, "e")


def open_event_edit_page(event_id, environment="production"):
    """opens a new tab on the Edit Page of an event id, returns the tab object
    ##NAME: Open Edit Page
    ##DESCRIPTION: open edit page when an eid is on clipboard
    ##TAGS: event
    ##ICON: chrome
    """
    return chrome.open_event_page_location(event_id, "edit")


def open_event_manage_page(event_id, environment="production"):
    """opens a new tab on the Manage Page of an event id, returns the tab object
    ##NAME: open manage page
    ##DESCRIPTION: open manage page when an eid is on clipboard
    ##TAGS: event
    ##ICON: chrome
    """
    return chrome.open_event_page_location(event_id, "myevent")


def open_salesforce_eventbrite_admin_side_by_side(query):
    """opens two windows side by side searching sf and admin for the same thing
    great for viewing a customer account in both places at once
    ##NAME: salesforce / eventbrite split view
    ##DESCRIPTION: open sf and eb admin side by side
    ##TAGS: event, order, email
    ##ICON: chrome
    """

    sf_win, sf_tab = chrome.new_window(url="https://salesforce.com")
    eb_win, eb_tab = chrome.new_window(url=admin_search_url(query))
    chrome.vertical_split_window(sf_win.index(), side="left")
    chrome.vertical_split_window(eb_win.index(), side="right")

    return sf_tab, eb_tab


def order_lookup(orders, environment="production"):
    """opens a new tab in Evenbrite Admin Order Lookup, searching the list of orders
    returns the tab object or the created tab
    ##NAME: Order Lookup
    ##DESCRIPTION: lookup orders in eb admin
    ##TAGS: order
    ##ICON: chrome
    """
    if not hasattr(orders, '__iter__'):
        orders = [].append(orders)

    url = eventbrite_url_constructor(
        "admin/orderinfo/",
        parameters={"order_id": ",".join(orders)}
    )
    for order in orders:
        if not is_order_id(order):
            raise ValueError("Order list contains invalid order ids. {} is not an order id".format(order))

    return chrome.new_tab(url)


def search_eventbrite_admin(query, environment="production", new_tab=True):
    """opens a new tab in Eventbrite Admin search, returns the tab object for the created tab
    ##NAME: EB Admin Search
    ##DESCRIPTION: search admin for eb-related values on the clipboard
    ##TAGS: event, order, email, organizer
    ##ICON: chrome
    """
    url = admin_search_url(query)
    if new_tab:
        return chrome.new_tab(url)
    else:
        admin_tabs = chrome.tabs_with_urls_that_contain_pattern("admin.eventbrite")
        if admin_tabs:
            admin_tab = admin_tabs[0]
            admin_tab.set_tab_url_to(url)
            return admin_tab
        else:
            return chrome.new_tab(url)
