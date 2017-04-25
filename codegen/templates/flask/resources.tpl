from flask import (
        request, current_app
        )
from {{ service_name }}.common.utils import APIException

class {{ service_name }}():

     {% for endpoint in service_endpoints %}
     def {{ endpoint.endpoint }}(self{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}):
         result = {}
         data = {{ endpoint.endpoint }}Inputs(request)
         if not data.validate():
             raise APIException(data.errors, status_code=500)
         try:
             self.{{ endpoint.endpoint }}_impl({{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}, request)
         except Exception as e:
             current_app.logger.error(str(e))
             error = u'Internal Server Error'
             raise APIException(error, status_code=500)
         return result

     def {{ endpoint.endpoint }}_impl(self{{ endpoint.params.__len__() and ', ' or '' }}{{ endpoint.params | join(', ') }}), request):
         raise Exception("{{ endpoint.name }} not Implemented")

     {% endfor %}
