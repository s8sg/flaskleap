from {{ service_name }}.views import {{ service_name | format_as('class') }}Impl


resource = {{ service_name | format_as('class') }}Impl()

routes = [
    {%- for endpoint in service_endpoints %}
    dict(url="{{ endpoint.url }}", endpoint_name="{{ endpoint.name }}",
    endpoint=resource.{{ endpoint.endpoint }}, methods=[{%- for method in endpoint.methods %}"{{ method }}",{%- endfor %}]),
    {%- endfor %}
]
