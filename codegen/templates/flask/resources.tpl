from flask import (
        request, current_app
        )
from {{ service_name }}.common.utils import APIException
from flask_inputs.validators import JsonSchema
from flask_inputs import Inputs
{%- for endpoint in service_endpoints %} {% if endpoint.methods["post"] %} 
from {{ service_name }}.schemas import {{ endpoint.methods.post["validator"] }}
{%- endif %} {% endfor %}

{% for endpoint in service_endpoints %} {% if endpoint.methods["post"] %} 
class {{ endpoint.endpoint }}Inputs(Inputs):
    json = [JsonSchema(schema={{ endpoint.methods.post["validator"] }})]

{% endif %} {% endfor %}
class {{ service_name }}():

     {% for endpoint in service_endpoints %}
     # Validator for Endpoint :{{ endpoint.endpoint }}
     def {{ endpoint.endpoint }}(self{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}):
         result = {}
         {% if endpoint.methods["post"] %} 
         data = {{ endpoint.endpoint }}Inputs(request)
         if not data.validate():
             raise APIException(data.errors, status_code=500)
         {% endif %}
         try:
             self.{{ endpoint.endpoint }}_impl(request{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }})
         except Exception as e:
             current_app.logger.error(str(e))
             error = u'Internal Server Error'
             raise APIException(error, status_code=500)
         return result

     # Endpoint {{ endpoint.endpoint }} abstract implementation
     def {{ endpoint.endpoint }}_impl(self, request{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}):
         raise Exception("{{ endpoint.name }} not Implemented")

     {% endfor %}
