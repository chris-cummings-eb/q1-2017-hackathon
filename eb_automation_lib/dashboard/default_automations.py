from ..chrome import Chrome as __Chrome


def open_event_listing(self, event_id=27849228793, environment="qa"):
    """description text"""
    chrome = __Chrome()
    chrome.open_event_listing(event_id, environment=environment)


def somefunc():
    """the actual docstring
    ##NAME: cool automation 2000
    ##DESCRIPTION: this automation is mega cool
    ##TYPE: chrome
    """
    print('somefunc')


def blah_blah():
    """prints blah_blah"""
    print('blah_blah')


def ooooooooooo():
    print('oooooooo')
