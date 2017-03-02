from datetime import datetime, timedelta
from urllib.parse import urlencode
import re


EB_DOMAINS = {
    "dev": "evbdev",
    "production": "eventbrite",
    "qa": "evbqa",
    "stage": "evbstage"
}

EB_TLDS = {
    "US": ".com",
    "UK": ".co.uk",
    "BR": ".br",
    "DE": ".de"
}

EB_SUBDOMAINS = {
    "www": "www",
    "admin": "admin"
}

EB_EVENT_REGEX = r"[0-9]{11}"
EB_ORDER_REGEX = r"[0-9]{9}"
EB_ORG_REGEX = r"[0-9]{10}"
EMAIL_REGEX = r"""^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])"""


def create_timestamp(date=datetime.now()):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def url_constructor(domain, path=None, parameters=None, protocol="http", subdomain=None, top_level_domain=".com"):

    if isinstance(parameters, dict):
        params = urlencode(parameters)
    else:
        params = parameters

    return "{protocol}://{subdomain}{domain}{top_level_domain}{path}{parameters}".format(
        protocol=protocol,
        subdomain=subdomain + "." if subdomain else "",
        domain=domain,
        top_level_domain=top_level_domain if top_level_domain.startswith(".") else ".com",
        path="/" + path if path else "",
        parameters="?" + params if params else ""
    )


def eventbrite_url_constructor(path, parameters=None, environment="production", subdomain="www", locale="US"):

    if locale in EB_TLDS.keys():
        tld = EB_TLDS[locale]

    elif locale in EB_TLDS.values():
        tld = locale

    else:
        raise ValueError("{} not an available tld for Eventbrite".format(tld))

    if environment not in EB_DOMAINS.keys():
        raise ValueError("{} is not a valid Eventbrite environment or domain".format(environment))

    return url_constructor(
        EB_DOMAINS[environment],
        path=path,
        parameters=parameters,
        protocol="https",
        subdomain=subdomain,
        top_level_domain=tld
    )


def is_event_id(string):
    return bool(re.match(EB_EVENT_REGEX, string))


def is_order_id(string):
    return bool(re.match(EB_ORDER_REGEX, string))


def is_organizer_id(string):
    return bool(re.match(EB_ORG_REGEX, string))


def is_email_address(string):
    return bool(re.match(EMAIL_REGEX, string))


def extract_event_id(string):
    match = re.search(EB_EVENT_REGEX, string)
    return match.group(0) if match else None


def extract_order_id(string):
    match = re.match(EB_ORDER_REGEX, string)
    return match.group(0) if match else None


def extract_organizer_id(string):
    match = re.match(EB_ORG_REGEX, string)
    return match.group(0) if match else None


def extract_email_address(string):
    match = re.match(EMAIL_REGEX, string)
    return match.group(0) if match else None


def get_axios_javascript_lib():
    """returns the contents of axios.min.js as a string"""
    return get_javascript_from_file("vendor/axios.min.js", export="ALL")


def get_clipboard_javascript_lib():
    """returns the contents of clipboard.min.js as a string"""
    return get_javascript_from_file("vendor/clipboard.min.js", export="ALL")


def get_javascript_from_file(filename, export="ALL"):
    """
        returns the entire javascript file unless exports is specificed, in which case the first
        declaration that matches the string passed into exports will be returned
        exmple:
        >>> get_javascript_from_file("js_snippet.js", export="myFunction")
        function myFunction(arg1) {
            // contnent of js function
        }

        ---
        export argument should be one of the following
        "ALL" -> return the whole file
        "default" -> return the default export
        "name" -> return the first declaration by name
    """

    DECLARATION_REGEX = r"(let|const|var|function)\s\w+"

    with open("./javascript/" + filename, "r") as f:
        content = f.readlines()

        if export == "ALL":
            return "".join(content)

        name_to_export = export

        if name_to_export.lower() == "default":
            for line in content[::-1]:
                if "export default" in line:
                    name_to_export = line.split(" ")[-1].replace(";", "").strip()
                    break

        left_brackets, right_brackets = 0, 0
        lines_to_export = []
        for line in content:

            declaration = re.search(DECLARATION_REGEX, line)

            if declaration and name_to_export in declaration.group(0):
                lines_to_export.append(line)

                left_brackets += line.count("{")
                right_brackets += line.count("}")

                if line[-1] == ";":
                    break

            elif lines_to_export:
                lines_to_export.append(line)

                left_brackets += line.count("{")
                right_brackets += line.count("}")

                if left_brackets == right_brackets:
                    break
        else:
            return

        return "".join(lines_to_export)
