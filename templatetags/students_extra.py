from django import template

register = template.Library()


@register.simple_tag
def field(field):
    if type(field) is str:
        return'<td></td><td></td>'
    return u'<td>{0.errors}{0.label}</td><td>{0}</td>'.format(field)
