from django import template

register = template.Library()


@register.filter
def index_id(value, args):
    return value[int(args)].id

@register.filter
def index(value, args):
    return value[int(args)-1]

def precessor(value, args):
    return value[int(args)-1]


def successor(value, args):
    return value[int(args)+1]
