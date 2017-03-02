**Clone this repo**  
`git clone https://github.com/chris-cummings-eb/q1-2017-hackathon.git`  

**Create and activate a python3 virtual environment**  
`virtualenv -p python3 venv`  
`. venv/bin/activate`  

**Install the Eventbrite python SDK and pyobjc**  
From your activated virtual environment run  
`pip install -r requirements.txt`  

**Example**
```python
from eb_wrapper import Eventbrite
from chrome import Chrome

eventbrite = Eventbrite(TOKEN)
response = eventbrite.create_event()

chrome = Chrome()
chrome.open_tab_at_url(response["event"]["url"])
```

More examples can be found in `example_usage.py`
Feel free to just run it try it out `python example_usage.py`

#How to contribute to this library
1. Follow the installation instructions above
2. Create a branch  
2. * `git branch my_branch_name && git checkout my_branch_name`
3. Make your changes
4. Push
5. Create a pull request or contact me
