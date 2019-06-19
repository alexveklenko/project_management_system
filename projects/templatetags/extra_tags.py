from django import template

register = template.Library()


@register.simple_tag
def set_query_parameter(url, param_name, param_value):
    from urllib.parse import (
        urlencode,
        parse_qs,
        urlsplit,
        urlunsplit,
    )
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)
    if param_value:
        query_params[param_name] = [param_value]
    elif param_name in query_params:
        del query_params[param_name]
    new_query_string = urlencode(query_params, doseq=True)
    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
