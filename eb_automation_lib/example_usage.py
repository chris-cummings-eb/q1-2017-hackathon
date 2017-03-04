from datetime import datetime, timedelta
from time import sleep

from chrome import Chrome
from eb_wrapper import Eventbrite
from utilities import create_timestamp, get_clipboard_javascript_lib

# import your own tokens something like this
from private.auth_constants import PROD_TOKEN, QA_TOKEN


def test_eb_wrapper():
        chrome = Chrome()

        # REMEMBER: you'll need to create your own tokens
        # and import them
        eventbrite = Eventbrite(QA_TOKEN, environment="qa")
        # eventbrite = Eventbrite(PROD_TOKEN, environment="production")

        # _data config dicts are used to override default settings.
        # configuration is not required

        # I want custom event title and description, so I create data
        # with those fields specified
        my_event_data = eventbrite.create_event_data(
            name="Great Event Title!!",
            description="this is some badass desription text"
        )

        # I want custom ticket data so I create a list of tickets
        # to create
        my_ticket_data = [
            eventbrite.create_ticket_data(name="ticket one"),  # ticket with simple change
            eventbrite.create_ticket_data(),  # ticket with default data
            eventbrite.create_ticket_data(**{
                "name": "my complicated ticket name",
                "description": "this ticket has description text",
                "hide_description": "False",
                "cost": "USD,33020",  # $100 USD ticket
                "quantity_total": "500",
                "include_fee": "True",
                "order_confirmation_message": "thanks for purchasing this special ticket. I hope you like it",
                "sales_end": create_timestamp(datetime.now() + timedelta(days=39))
            })  # ticket with lots of custom data
        ]

        # create a single event with the configurations above
        response = eventbrite.create_event(
            event_data=my_event_data,
            ticket_data=my_ticket_data,
            publish=False
        )

        if not response.get("error"):
            # if there was no error, open event edit page in new chrome tab
            chrome.open_event_edit_page(
                response["event"]["id"],
                environment="qa"
            )
        else:
            print("there was an error:", response["error"])


def test_js():
    chrome = Chrome()
    js = get_clipboard_javascript_lib()
    chrome.active_tab().executeJavascript_(js)


if __name__ == "__main__":
    test_eb_wrapper()
    test_js()
