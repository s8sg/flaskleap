from {{ service_name }}.{{ module.name }}.views import {{ module.name | format_as('class') }}Impl


resource = {{ module.name | format_as('class') }}Impl()

routes = [
        {%- for endpoint in module.endpoints %}
        dict(url="/{{ endpoint.url }}", endpoint_name="{{ endpoint.name }}",
             endpoint=resource.{{ endpoint.endpoint }}, methods=[{%- for method in endpoint.methods %}"{{ method }}",{%- endfor %}]),
        {%- endfor %}
        ]
