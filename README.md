*Install the Eventbrite python SDK and pyobjc*
From your activated virtual environment run
`pip install eventbrite`
`pip install pyobjc`

```python
from eb_wrapper import Eventbrite
from chrome import Chrome

eventbrite = Eventbrite(TOKEN)
response = eventbrite.create_event()

chrome = Chrome()
chrome.open_tab_at_url(response["event"]["url"])
```

More examples can be found in `example_usage.py`
