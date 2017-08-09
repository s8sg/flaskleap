from flask import Blueprint
from {{ service_name }}.{{ module.name }}.routes import routes

# define blueprint
{{ module.name }}_module = Blueprint('{{ module.name }}_module', __name__)

# Register all routes for the Blueprint
for route in routes:
    {{ module.name }}_module.add_url_rule(
        route.pop('url'),
        endpoint=route.pop('endpoint_name'),
        view_func=route.pop('endpoint'),
        methods=route.pop('methods'))
