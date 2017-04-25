from {{ service_name }}.{{ module.name }}.views import {{ module.name }}_impl


resource = hello_impl()

routes = [
        {%- for endpoint in module.endpoints %}
        dict(url="{{ endpoint.url }}", endpoint_name="{{ endpoint.name }}",
             endpoint=resource.{{ endpoint.endpoint }}, methods=[{%- for method in endpoint.methods %}"{{ method }}",{%- endfor %}]),
        {%- endfor %}
        ]
