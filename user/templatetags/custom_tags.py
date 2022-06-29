import locale
import re

from django import template


register = template.Library()
numeric_test = re.compile("^\d+$")
locale.setlocale(locale.LC_NUMERIC, 'ru_RU.utf8')


@register.filter(name="print_dir")
def print_dir(item):
    print(item)
    print(type(item))
    print(dir(item))


@register.filter(name="get_table_headers")
def get_table_headers(model, fields):
    arr = []
    for field in fields:
        arr.append(model._meta.get_field(field).verbose_name)
    return arr


@register.filter(name="getattribute")
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return 0


@register.filter(name="plus")
def plus(value, value_2):
    if not value and not value_2:
        return 0
    if not value:
        return value_2
    elif not value_2:
        return value
    return value + value_2


@register.filter(name="minus")
def minus(value, value_2):
    if not value and not value_2:
        return 0
    elif not value:
        return value_2 * -1
    elif not value_2:
        return value
    return value - value_2


@register.filter(name="mul")
def mul(value, value_2):
    return value * value_2


@register.filter(name="fix_float")
def fix_float(value):
    return str(value)


@register.filter(name="percent")
def mul(value, value_2):
    return value * (value_2 / 100)


@register.filter(name="is_image")
def is_image(value):
    return str(value).endswith('.jpg') or str(value).endswith('.png')


@register.filter(name="to_local")
def mul(value):
    if isinstance(value, float) or isinstance(value, int):
        return locale.format('%d', value, grouping=True)
    else:
        return value


@register.simple_tag
def setvar(value):
    return value
