from Quartz import CGMainDisplayID, CGGetActiveDisplayList, CGDisplayBounds
import sys


MENU_BAR_HEIGHT = 23


def create_window_position(window_size, position, display_size=None):
    """returns a window position tuple"""
    if not (
        position[0].lower() in ["upper", "lower"] and
        position[1].lower() in ["left", "right"]
    ):
        raise ValueError("Position is not valid. must be in upper, lower, left, right")

    if display_size is None:
        display_size = get_display_size()

    max_width, max_height = display_size
    max_height = max_height - MENU_BAR_HEIGHT
    window_width, window_height = window_size

    x_position, y_position = 0, 0
    if position[0] == "lower":
        y_position = max_height - window_height
    if position[1] == "right":
        x_position = max_width - window_width

    return (x_position, y_position)


def set_window_size_by_percent(window, width_percent, height_percent, position=("upper", "left")):
    """
    position and size that window and return the size and position
    """

    max_width, max_height = get_display_size()
    max_height = max_height - MENU_BAR_HEIGHT

    width = max_width * (width_percent / 100)
    height = (max_height * (height_percent / 100))

    window_size_and_position = create_window_size_object(
        size=(width, height),
        position=create_window_position((width, height), position)
    )

    try:
        set_window_size(window, window_size_and_position)
    except AttributeError as e:
        raise AttributeError("Not a scriptable window object. Error: {}".format(e))

    return window_size_and_position


def create_window_size_object(size=None, position=(0, 0)):
    """
    pass in a tuple of (width, height) where width and height are decimals
    returns a size object from a tuple of width, height in number of pixels
    optionally can specifify the position
    """
    display_size = get_display_size()

    if size is None:
        size = display_size

    elif (
        size[0] > display_size[0] and
        size[1] > display_size[1]
    ):
        size = display_size

    return [[position[0], position[1]], [size[0], size[1]]]


def get_window_size(window):
    try:
        size = window.bounds()
    except AttributeError as e:
        raise AttributeError("Not a scriptable window object. Error: {}".format(e))

    return (size.size.width, size.size.height)


def set_window_size(window, size=None):
    """
    set the size of a window object, pass in the return value from create_window_size_object
    called with your desired (width, height), (x-position, y-position)
    """
    if size is None:
        size = create_window_size_object()
    try:
        window.setBounds_(size)
    except AttributeError as e:
        raise AttributeError("Not a scriptable window object. Error: {}".format(e))


def get_display_size(display_id=None):
    if display_id is None:
        display_id = CGMainDisplayID()

    size_data = CGDisplayBounds(display_id)
    return (size_data.size.width, size_data.size.height)


def get_device_active_displays(count=3):
    error, active_displays, number_of_active_displays = CGGetActiveDisplayList(
        count, None, None
    )
    if error:
        print(
            "There was a problem getting the active display list.\nError Message:",
            error,
            file=sys.stderr
        )
        sys.exit(-1)

    display_data = {}
    main_display_id = CGMainDisplayID()

    for count, display_id in enumerate(active_displays):
        if display_id == main_display_id:
            display_data["main"] = display_id
            continue
        elif count == 2:
            display_data["secondary"] = display_id
            continue

        display_data["other_{}".format(count)] = display_id

    return display_data
