from datetime import datetime, timedelta
from eventbrite import Eventbrite as Eb
from utilities import create_timestamp

API_URLS = {
    "production": "https://www.eventbriteapi.com/v3/",
    "qa": "https://www.evbqaapi.com/v3/"
}


class Eventbrite(Eb):

    def __init__(self, oauth_token, environment="qa"):

        if environment not in API_URLS.keys():
            raise ValueError("environment must be in: {}".format(API_URLS.keys()))

        Eb.__init__(self, oauth_token, eventbrite_api_url=API_URLS[environment])

    @staticmethod
    def create_event_data(**kwargs):
        """
        Create event data with default values, or pass in a keyword arguments with keys that correspond with event field
        names. Default start/end dates is 30 days from current date
        FIELD NAMES:
            description, start, end, currency, organizer_id, hide_start_date, hide_end_date, shareable, invite_only,
            password, venue_id, online_event, listed, logo, category_id, subcategory_id, format_id, capacity,
            source, show_remaining
        """

        start_time = datetime.now() + timedelta(days=30)

        event_data = {
            "event.name.html": "Test Event: {date}".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "event.description.html": "Event description text.",
            "event.start.utc": create_timestamp(start_time),
            "event.start.timezone": "America/Chicago",
            "event.end.utc": create_timestamp(start_time + timedelta(hours=3)),
            "event.end.timezone": "America/Chicago",
            "event.currency": "USD",
            "event.organizer_id": "",
            "event.hide_start_date": "",
            "event.hide_end_date": "",
            "event.shareable": "",
            "event.invite_only": "",
            "event.password": "",
            "event.venue_id": "",
            "event.online_event": "",
            "event.listed": "",
            "event.logo.id": "",
            "event.category_id": "",
            "event.subcategory_id": "",
            "event.format_id": "",
            "event.capacity": "",
            "event.source": "",
            "event.show_remaining": "",
        }

        for k, v in kwargs.items():
            if "start" in k:
                if k == "start_time":
                    event_data["event.start.utc"] = v
                elif k == "start_timezone":
                    event_data["event.start.timezone"] = v
                continue

            if "end" in k:
                if k == "end_time":
                    event_data["event.end.utc"] = v
                elif k == "end_timezone":
                    event_data["event.end.timezone"] = v
                continue

            else:
                for field_name in event_data.keys():
                    if k in field_name.split("."):
                        event_data[field_name] = v
                        break

        return event_data

    @staticmethod
    def create_ticket_data(**kwargs):

        ticket_data = {
            # string: Name of this ticket type
            "ticket_class.name": "Test {}".format(datetime.now().strftime("%H:%M:%S")),

            # string: Description of the ticket
            "ticket_class.description": "This is a ticket description",

            # integer: Total available number of tickets
            "ticket_class.quantity_total": "100",

            # string: e.g. $45 would be ‘USD,4500’
            "ticket_class.cost": "USD,10000",

            # boolean: Is this a donation?
            "ticket_class.donation": "False",

            # boolean: Is this a free ticket?
            "ticket_class.free": "False",

            # boolean: Absorb fees?
            "ticket_class.include_fee": "False",

            # boolean: Split fees?
            "ticket_class.split_fee": "False",

            # boolean: ticket desc behind readmore link
            "ticket_class.hide_description": "True",

            # list: ([“online”], [“online”, “atd”], [“atd”])
            "ticket_class.sales_channels": "",

            # datetime: empty = when event published
            "ticket_class.sales_start": "",

            # datetime: empty = 1hr before event start
            "ticket_class.sales_end": "",

            # string: start sales after ticket id
            "ticket_class.sales_start_after": "",

            # integer: Minimum number per order
            "ticket_class.minimum_quantity": "",

            # integer: Max per order empty = unlimited
            "ticket_class.maximum_quantity": "",

            # boolean: Hide when not on sale
            "ticket_class.auto_hide": "",

            # datetime: reveal date for auto-hide
            "ticket_class.auto_hide_before": "",

            # datetime: re-hide date for auto-hide
            "ticket_class.auto_hide_after": "",

            # boolean: Hide this ticket
            "ticket_class.hidden": "",

            # string: confirmation message per ticket
            "ticket_class.order_confirmation_message": "",
        }

        for k, v in kwargs.items():
            for field_name in ticket_data.keys():
                if k in field_name.split("."):
                    ticket_data[field_name] = v
                    break

        return ticket_data

    def create_event(
        self,
        event_data=create_event_data.__func__(),
        ticket_data=[create_ticket_data.__func__()],
        publish=False
    ):

        event = self.post_event(event_data)

        if event.get("error"):
            return {"error": event}

        tickets = {}
        for ticket in ticket_data:
            response = self.post_event_ticket_class(event["id"], ticket)
            tickets[response["id"]] = response

        if publish:
            self.publish_event(event["id"])

        return {"event": event, "tickets": tickets, "error": None}
