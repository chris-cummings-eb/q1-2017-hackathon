from time import sleep

from chrome import Chrome
from eb_wrapper import Eventbrite

if __name__ == "__main__":
    chrome = Chrome()

    # qa testing
    eventbrite = Eventbrite("", environment="qa")

    # prod testing
    # eventbrite = Eventbrite("", environment="production")

    my_event_data = eventbrite.create_event_data(
        name="hello this is my test event",
        description="this is some badass desription text"
    )

    my_ticket_data = [
        eventbrite.create_ticket_data(name="ticket one"),
        eventbrite.create_ticket_data(name="ticket two"),
        eventbrite.create_ticket_data(name="ticket three")
    ]

    # create a single event with one ticket
    # all default data
    response = eventbrite.create_event(
        event_data=my_event_data,
        ticket_data=my_ticket_data,
        publish=False
    )

    if not response["error"]:
        # open event edit page in new chrome tab
        chrome.new_tab_at_url(
            "https://evbqa.com/edit?eid={event_id}".format(
                event_id=response["event"]["id"]
            )
        )
    else:
        print("there was an error:", response["error"])
