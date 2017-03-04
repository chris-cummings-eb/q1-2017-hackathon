# How to use
## 1. Create and activate a python3 virtual environment
`$ virtualenv -p python3 venv`  
`$ . venv/bin/activate`
## 2. Clone this repo
`$ git clone https://github.com/chris-cummings-eb/q1-2017-hackathon.git`  
## 3. install the library
```
$ cd q1-2017-hackathon
$ pip install -e .
```
## 4. change to your project directory and use the lib like this
**Example**
```python
# import the library
from eb_automation_lib import Chrome, Eventbrite

# import your own tokens something like this
from private.auth_constants import PROD_TOKEN, QA_TOKEN

eventbrite = Eventbrite(TOKEN)
response = eventbrite.create_event()

chrome = Chrome()
chrome.open_tab_at_url(response["event"]["url"])
```

#How to contribute to this library
1. Follow the installation instructions above
2. Create a branch `git branch my_branch_name && git checkout my_branch_name`
3. Make your changes
4. Push
5. Create a pull request or contact me
