from flask import (
        request, current_app
        )
from {{ service_name }}.common.utils import APIException
from flask_inputs3.validators import JsonSchema
from flask_inputs3 import Inputs
{%- for endpoint in service_endpoints %} {% if endpoint.methods["post"] %}
from {{ service_name }}.schemas import {{ endpoint.methods.post["validator"] }}
{%- endif %} {% endfor %}
{%- for endpoint in service_endpoints %} {% if endpoint.methods["delete"] %}
from {{ service_name }}.schemas import {{ endpoint.methods.delete["validator"] }}
{%- endif %} {% endfor %}


{% for endpoint in service_endpoints %} {% if endpoint.methods["post"] %}
class {{ endpoint.endpoint }}_inputs(Inputs):
    json = [JsonSchema(schema={{ endpoint.methods.post["validator"] }})]


{% endif %} {% endfor %}
{% for endpoint in service_endpoints %} {% if endpoint.methods["delete"] %}
class {{ endpoint.endpoint }}_inputs(Inputs):
    json = [JsonSchema(schema={{ endpoint.methods.delete["validator"] }})]


{% endif %} {% endfor %}
class {{ service_name | format_as('class') }}():

     def __init__(self):
         pass

     {% for endpoint in service_endpoints %}
     # Validator for Endpoint :{{ endpoint.endpoint }}
     def {{ endpoint.endpoint }}(self{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}):
         result = {}
         {% if endpoint.methods["post"] %}
         data = {{ endpoint.endpoint }}_inputs(request)
         if not data.validate():
             raise APIException(data.errors, status_code=500)
         {% endif %}
         {% if endpoint.methods["delete"] %}
         data = {{ endpoint.endpoint }}_inputs(request)
         if not data.validate():
             raise APIException(data.errors, status_code=500)
         {% endif %}
         try:
             result = self.{{ endpoint.endpoint }}_impl(request{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }})
         except Exception as e:
             current_app.logger.error(e)
             error = u'Internal Server Error: %s' % str(e)
             raise APIException(error, status_code=500)
         return result

     # Endpoint {{ endpoint.endpoint }} abstract implementation
     def {{ endpoint.endpoint }}_impl(self, request{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}):
         raise Exception("{{ endpoint.name }} not Implemented")

     {% endfor %}
