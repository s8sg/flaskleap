import os
import json
from flask import (Flask, jsonify)
from flasgger import Swagger
from {{ service_name }}.common.utils import (APIException, APIResponse)
from werkzeug.wsgi import DispatcherMiddleware
from aaa_client import RBAC

config_variable_name = 'SERVICE_CONFIG_PATH'
default_config_path = os.path.join(os.path.dirname(__file__),
                                   'config/config.py')
os.environ.setdefault(config_variable_name, default_config_path)

rbac = None
# TODO: Define Global resource (e.g. DB object)


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name:
        app.config.from_pyfile(config_name)
    else:
        app.config.from_envvar(config_variable_name)

    app.wsgi_app = DispatcherMiddleware(Flask('dummy_app'), {
	            app.config['APPLICATION_ROOT']: app.wsgi_app})

    init_app(app)
    template = None
    with open('{{ service_name }}/swagger.json', 'r') as swagger_file:
        template = json.load(swagger_file)
    Swagger(app, template=template)

    return app


def init_app(app):
    app.logger.info("initializing app context")

    rbac_server = app.config.get("AAA_SERVER", "127.0.0.1:8080")
    rbac = RBAC(rbac_server, cache=True)
    # TODO: Init GLocal Object (e.g DB Object)

    # Define API Exception Handler
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Define the app teardown handler
    # @app.teardown_appcontext
    # def destroy_app(error):
    #     app.logger.info("destroying app context")
    #     ldapManager.close()

    # Set API Response Handler
    app.response_class = APIResponse

    # Delay import the blueprints
    from {{ service_name }}.blueprints import blueprints
    # Register Blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint.pop("module"),
                               url_prefix=blueprint.pop("module_name"))
    # delay imports the routes
    from {{ service_name }}.routes import routes
    # Register routes
    for route in routes:
        app.add_url_rule(route.pop('url'),
                         endpoint=route.pop('endpoint_name'),
                         view_func=route.pop('endpoint'),
                         methods=route.pop('methods')
                         )
