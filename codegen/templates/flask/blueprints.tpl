{%- for module in modules %}
from {{ service_name }}.{{ module.name }} import {{ module.name }}_module
{%- endfor %}

blueprints = [
               {%- for module in modules %}
               dict(module={{ module.name }}_module, module_name="/{{ module.name }}"),
               {%- endfor %}
             ]
