from .chrome import Chrome
chrome = Chrome()


def open_event_listing(event_id, environment="production", parameters=None):
    """opens a new tab at the event's listing page, returns the tab object for the created tab"""
    return chrome._open_event_page_location(event_id, "e")


def open_event_edit_page(event_id, environment="production"):
    """opens a new tab on the Edit Page of an event id, returns the tab object"""
    return chrome.open_event_page_location(event_id, "edit")


def open_event_manage_page(event_id, environment="production"):
    """opens a new tab on the Manage Page of an event id, returns the tab object"""
    return chrome.open_event_page_location(event_id, "myevent")


def open_salesforce_eventbrite_admin_side_by_side(query):
    """opens two windows side by side searching sf and admin for the same thing
    great for viewing a customer account in both places at once
    """

    sf_win, sf_tab = self.new_window(url="https://salesforce.com")
    eb_win, eb_tab = self.new_window(url=admin_search_url(eventbrite_query))
    self.vertical_split_window(sf_win.index(), side="left")
    self.vertical_split_window(eb_win.index(), side="right")

    return sf_tab, eb_tab


def order_lookup(orders, environment="production"):
    """opens a new tab in Evenbrite Admin Order Lookup, searching the list of orders
    returns the tab object or the created tab
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
    """opens a new tab in Eventbrite Admin search, returns the tab object for the created tab"""
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
