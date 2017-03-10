from AppKit import NSPasteboard, NSStringPboardType
from Foundation import NSString, NSUTF8StringEncoding

OS_CLIPBOARD = NSPasteboard.generalPasteboard()


def set_clipboard(value):
    OS_CLIPBOARD.declareTypes_owner_([NSStringPboardType], None)
    OS_CLIPBOARD.setData_forType_(
        NSString.stringWithString_(value).nsstring().dataUsingEncoding_(NSUTF8StringEncoding),
        NSStringPboardType
    )


def get_clipboard():
    OS_CLIPBOARD = NSPasteboard.generalPasteboard()
    return OS_CLIPBOARD.stringForType_(NSStringPboardType)
