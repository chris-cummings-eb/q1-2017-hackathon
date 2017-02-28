pip install eventbrite
pip install pyobjc

from eb_wrapper import Eventbrite
from chrome import Chrome

eventbrite = Eventbrite(TOKEN)
response = eventbrite.create_event()

chrome = Chrome()
chrome.open_tab_at_url(response["event"]["url"])

----
sample usage script in test.py
----
