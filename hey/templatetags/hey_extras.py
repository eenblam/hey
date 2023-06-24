from datetime import datetime

from django.template.defaultfilters import register

@register.filter
def style_last_contact(last_contact):
    if last_contact is None or last_contact == "":
        return ""
    try:
        if last_contact.year == datetime.today().year:
            return last_contact.strftime("%b %d")
        else:
            return last_contact.strftime("%b %d, %Y")
    except AttributeError:
        return ""