# Automation Workshop Class Instructions
## 1. Install brew
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
## 2. Install atom
`brew cask install atom`
## 3. Open Atom, from Atom the Menu, choose: Install Shell Commands then CLOSE ATOM
## 4. Install Atom plugins
`apm install linter linter-pep8 autocomplete-python`
## 5. Install python3 and virtualenv
`brew install python3 && pip3 install virtualenv`
## 6. Create a project folder
`mkdir ~/automations && cd ~/automations`
## 7. Follow How to use instructions below

# How to use
## 1. Create and activate a python3 virtual environment
`virtualenv -p python3 venv && . venv/bin/activate`
## 2. Clone this repo
`git clone https://github.com/chris-cummings-eb/q1-2017-hackathon.git`  
## 3. install the library
`cd q1-2017-hackathon && pip install -e .`
## 4. change to your project directory and use the lib like this
`cd .. && cp q1-2017-hackathon/run_dashboard.py . && cp q1-2017-hackathon/my_automations_template.py ./my_automations.py && atom my_automations.py run_dashboard.py`  
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
