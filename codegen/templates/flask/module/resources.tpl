from flask import (
        request, current_app
        )
from {{ service_name }}.common.utils import APIException


class {{ module.name }}():

     {% for endpoint in module.endpoints %}
     def {{ endpoint.endpoint }}(self{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}):
         result = {}
         {%- for request in endpoint.requests %}
         print(g.{{ request }})
         {%- endfor %}

         {% if 'response' in  endpoint -%}
         # return {{ endpoint.response.0 }}, {{ endpoint.response.1 }}, {{ endpoint.response.2 }}
         {%- else %}
         # pass
         #{%- endif %}
         try:
             # TODO:Implement 
             raise Exception("{{ endpoint.name }} not Implemented")
         except Exception as e:
             current_app.logger.error(str(e))
             error = u'Internal Server Error'
             raise APIException(error, status_code=500)
         return result


     {% endfor %}
