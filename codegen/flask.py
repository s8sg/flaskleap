from __future__ import absolute_import
import json
import six
import re
import yaml
from collections import OrderedDict
from .base import Code, CodeGenerator
from .jsonschema import Schema, SchemaGenerator, build_default
from operator import itemgetter

SUPPORT_METHODS = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']
RESERVED_MODULES = ['common', 'config', 'app', 'blueprints', 'resources',
                    'routes', 'run', 'schemas', 'views']


class AppDesc(Code):
    template = 'flask/__init__.tpl'
    dest_template = '%(package)s/__init__.py'
    override = False


class AppStart(Code):
    template = 'flask/__main__.tpl'
    dest_template = '%(package)s/__main__.py'
    override = False


class App(Code):
    template = 'flask/app.tpl'
    dest_template = '%(package)s/app.py'
    override = False


class Blueprint(Code):
    template = 'flask/blueprints.tpl'
    dest_template = '%(package)s/blueprints.py'
    override = True


class Router(Code):
    template = 'flask/routes.tpl'
    dest_template = '%(package)s/routes.py'
    override = True


class Runner(Code):
    template = 'flask/run.tpl'
    dest_template = '%(package)s/run.py'
    override = False


class Resource(Code):
    template = 'flask/resources.tpl'
    dest_template = '%(package)s/resources.py'
    override = True


class Views(Code):
    template = 'flask/views.tpl'
    dest_template = '%(package)s/views.py'
    override = False


class Common(Code):
    template = 'flask/common/__init__.tpl'
    dest_template = '%(package)s/common/__init__.py'
    override = False


class Utils(Code):
    template = 'flask/common/utils.tpl'
    dest_template = '%(package)s/common/utils.py'
    override = False


class Config(Code):
    template = 'flask/config/__init__.tpl'
    dest_template = '%(package)s/config/__init__.py'
    override = False


class ConfigFile(Code):
    template = 'flask/config/config.tpl'
    dest_template = '%(package)s/config/config.py'
    override = False


class Module(Code):
    template = 'flask/module/__init__.tpl'
    dest_template = '%(package)s/%(module_name)s/__init__.py'
    override = False


class ModuleModel(Code):
    template = 'flask/module/models.tpl'
    dest_template = '%(package)s/%(module_name)s/models.py'
    override = False


class ModuleRoutes(Code):
    template = 'flask/module/routes.tpl'
    dest_template = '%(package)s/%(module_name)s/routes.py'
    override = True


class ModuleResource(Code):
    template = 'flask/module/resources.tpl'
    dest_template = '%(package)s/%(module_name)s/resources.py'
    override = True


class ModuleViews(Code):
    template = 'flask/module/views.tpl'
    dest_template = '%(package)s/%(module_name)s/views.py'
    override = False


class Specification(Code):
    template = 'flask/specification.tpl'
    dest_template = '%(package)s/swagger.json'
    override = True


class Server(Code):
    template = 'flask/service/server.tpl'
    dest_template = 'server.py'
    override = False


class Setup(Code):
    template = 'flask/service/setup.tpl'
    dest_template = 'setup.py'
    override = False


class SetupConfig(Code):
    template = 'flask/service/setup_cfg.tpl'
    dest_template = 'setup.cfg'
    override = False


class Wsgi(Code):
    template = 'flask/service/wsgi.tpl'
    dest_template = 'wsgi.py'
    override = False


class Dockerfile(Code):
    template = 'flask/service/Dockerfile.tpl'
    dest_template = 'Dockerfile'
    override = False


class DockerEntrypoint(Code):
    template = 'flask/service/docker-entrypoint.tpl'
    dest_template = 'docker-entrypoint.sh'
    override = False


class Manifest(Code):
    template = 'flask/service/MANIFEST.tpl'
    dest_template = 'MANIFEST.in'
    override = False


class Makefile(Code):
    template = 'flask/service/Makefile.tpl'
    dest_template = 'Makefile'
    override = False


class Readme(Code):
    template = 'flask/service/README.tpl'
    dest_template = 'README.md'
    override = False


class Requirements(Code):
    template = 'flask/service/requirements.tpl'
    dest_template = 'requirements.txt'
    override = False


class ServiceConfig(Code):
    template = 'flask/service/config/config.tpl'
    dest_template = 'config/config.py'
    override = False


class Tox(Code):
    template = 'flask/service/tox.tpl'
    dest_template = 'tox.ini'
    override = False


class Test(Code):
    template = 'flask/service/test/__init__.tpl'
    dest_template = 'test/__init__.py'
    override = False


class TestCode(Code):
    template = 'flask/service/test/test.tpl'
    dest_template = 'test/test.py'
    override = True


class SwaggerSpec(Code):
    template = 'flask/service/swagger.tpl'
    dest_template = 'swagger.yaml'
    override = True


def _swagger_to_flask_url(url, swagger_path_node):
    types = {
        'integer': 'int',
        'long': 'int',
        'float': 'float',
        'double': 'float'
    }
    node = swagger_path_node
    params = re.findall(r'\{([^\}]+?)\}', url)
    url = re.sub(r'{(.*?)}', '<\\1>', url)

    def _type(parameters):
        for p in parameters:
            if p.get('in') != 'path':
                continue
            t = p.get('type', 'string')
            if t in types:
                yield '<%s>' % p['name'], '<%s:%s>' % (types[t], p['name'])

    for old, new in _type(node.get('parameters', [])):
        url = url.replace(old, new)

    for k in SUPPORT_METHODS:
        if k in node:
            for old, new in _type(node[k].get('parameters', [])):
                url = url.replace(old, new)

    return url, params


if six.PY3:
    def _remove_characters(text, deletechars):
        return text.translate({ord(x): None for x in deletechars})
else:
    def _remove_characters(text, deletechars):
        return text.translate(None, deletechars)


def _path_to_endpoint(swagger_path):
    return _remove_characters(
        swagger_path.strip('/').replace('/', '_').replace('-', '_'),
        '{}')


def _path_to_resource_name(swagger_path):
    return _remove_characters(swagger_path.title(), '{}/_-')


def _endpoint_id(endpoint, method):
    return endpoint + "_" + method


def _endpoint_name(resource_name, method):
    return resource_name + method.title()


def _sanitize_module_name(name, illegal_names=RESERVED_MODULES):
    """Append '_api' to module names when they conflict with our modules."""
    return re.sub(r'^((%s)(_api)*)$' %
                  '|'.join(illegal_names), r'\1_api', name)


def _location(swagger_location):
    location_map = {
        'body': 'json',
        'header': 'headers',
        'formData': 'form',
        'query': 'args'
    }
    return location_map.get(swagger_location)


class FlaskGenerator(CodeGenerator):

    dependencies = [SchemaGenerator]

    def __init__(self, swagger):
        super(FlaskGenerator, self).__init__(swagger)
        self.package = None
        # Default group factor is one
        #  Which implies that, more than one occurance of the first URL block
        # will create a new module
        # A group factor zero implies no grouping
        self.group_factor = 1
        # Default group segment count is 1
        # which implies that only the first block of the URL segments
        # will be matched for grouping
        # The value of group segment is always >= 1
        # self.group_segment_count = 1
        # NOTE: Not being used now
        self.author = ""
        self.mail = ""
        self.version = ""

    def _dependence_callback(self, code):
        if not isinstance(code, Schema):
            return code
        schemas = code
        # schemas default key likes `('/some/path/{param}', 'method')`
        # use flask endpoint to replace default validator's key,
        # example: `('some_path_param', 'method')`
        validators = OrderedDict()
        for k, v in six.iteritems(schemas.data['validators']):
            locations = {_location(loc): val for loc, val in six.iteritems(v)}
            validators[(_path_to_endpoint(k[0]), k[1])] = locations

        # filters
        filters = OrderedDict()
        for k, v in six.iteritems(schemas.data['filters']):
            filters[(_path_to_endpoint(k[0]), k[1])] = v

        # scopes
        scopes = OrderedDict()
        for k, v in six.iteritems(schemas.data['scopes']):
            scopes[(_path_to_endpoint(k[0]), k[1])] = v

        schemas.data['validators'] = validators
        schemas.data['filters'] = filters
        schemas.data['scopes'] = scopes
        self.schemas = schemas
        self.validators = validators
        self.filters = filters
        return schemas

    def _process_data(self):

        views = {}
        service_endpoints = []
        modules = {}

        endpoint_store = {}

        for paths, data in self.swagger.search(['paths', '*']):
            swagger_path = paths[-1]
            url, params = _swagger_to_flask_url(swagger_path, data)
            ep = _path_to_endpoint(swagger_path)
            nm = _path_to_resource_name(swagger_path)

            methods = dict()
            for method in SUPPORT_METHODS:
                if method not in data:
                    continue
                methods[method] = {}
                validator = self.validators.get((ep, method.upper()))
                if validator:
                    methods[method]['requests'] = list(validator.keys())
                    methods[method]['validator'] = validator['json']

                for status, res_data in six.iteritems(
                        data[method].get('responses', {})):
                    if isinstance(status, int) or status.isdigit():
                        example = res_data.get('examples', {}).get(
                                'application/json')

                        if not example:
                            example = build_default(res_data.get('schema'))
                        response = example, int(status), build_default(
                                res_data.get('headers'))
                        methods[method]['response'] = response
                        break
            for method in methods:
                # Generate the endpoint Id/Name considering the methods type
                name = _endpoint_name(nm, method)
                endpoint = _endpoint_id(ep, method)

                module_name = ""
                modified_url = ""
                if url.startswith("/"):
                    module_name = url.split('/')[1]
                    modified_url = "/".join(url.split('/')[2:])
                else:
                    module_name = url.split('/')[0]
                    modified_url = "/".join(url.split('/')[1:])
                if (self.group_factor > 0):
                    # Check if this endpoint belongs in an existing module
                    module = modules.get(module_name)
                    if module:
                        module["endpoints"].append({
                            'url': modified_url,
                            'params': params,
                            'endpoint': endpoint,
                            'methods': {method: methods[method]},
                            'name': name
                        })
                        continue

                # Check if a module can be created
                if (self.group_factor > 0) and \
                   (module_name in endpoint_store) and \
                   (len(endpoint_store[module_name]) == self.group_factor):
                    oldEndpoints = endpoint_store[module_name]
                    for oldendpoint in oldEndpoints:
                        oldendpoint_url = oldendpoint['url']
                        oldmodified_url = ""
                        if url.startswith("/"):
                            oldmodified_url = "/".join(
                                              oldendpoint_url.split('/')[2:])
                        else:
                            oldmodified_url = "/".join(
                                              oldendpoint_url.split('/')[1:])
                        oldendpoint['url'] = oldmodified_url
                    del endpoint_store[module_name]
                    newEndpoint = dict(
                                        url=modified_url,
                                        params=params,
                                        endpoint=endpoint,
                                        methods={method: methods[method]},
                                        name=name
                                       )
                    endpoints = [newEndpoint]
                    endpoints.extend(oldEndpoints)
                    endpoints = sorted(endpoints, key=itemgetter('name'))

                    modules[module_name] = {
                        "name": _sanitize_module_name(module_name),
                        "endpoints": endpoints
                    }
                # Add it as a endpoint
                else:
                    if module_name in endpoint_store:
                        endpoint_store[module_name].append(
                                        dict(
                                             url=url,
                                             params=params,
                                             endpoint=endpoint,
                                             methods={method: methods[method]},
                                             name=name
                                            ))

                    else:
                        endpoint_store[module_name] = [
                                        dict(
                                             url=url,
                                             params=params,
                                             endpoint=endpoint,
                                             methods={method: methods[method]},
                                             name=name
                                            )]
        for endpoint_group in endpoint_store:
            service_endpoints.extend(endpoint_store[endpoint_group])
        views["service_endpoints"] = sorted(service_endpoints,
                                            key=itemgetter('name'))
        views["modules"] = sorted(modules.values(), key=itemgetter('name'))
        views["service_name"] = self.package
        views["base_path"] = self.swagger.base_path
        views["AUTHOR"] = self.author
        views["MAIL"] = self.mail
        views["VERSION"] = self.version
        return views

    def _process(self):
        # Get Views
        views = self._process_data()
        yield AppDesc(views)
        yield AppStart(views)
        yield App(dict(with_ui=True, **views))
        yield Blueprint(views)
        yield Router(views)
        yield Runner(views)
        yield Resource(views)
        yield Views(views)
        yield Common()
        yield Utils(views)
        yield Config(views)
        yield ConfigFile(views)

        for module in views["modules"]:
            yield Module(dict(module=module, service_name=self.package),
                         dist_env=dict(module_name=module["name"]))
            yield ModuleModel(dict(module=module, service_name=self.package),
                              dist_env=dict(module_name=module["name"]))
            yield ModuleRoutes(dict(module=module, service_name=self.package),
                               dist_env=dict(module_name=module["name"]))
            yield ModuleViews(dict(module=module,
                              service_name=self.package),
                              dist_env=dict(module_name=module["name"]))
            yield ModuleResource(dict(module=module,
                                 service_name=self.package),
                                 dist_env=dict(module_name=module["name"]))

        swagger = {}
        swagger.update(self.swagger.origin_data)
        swagger.pop('host', None)
        swagger.pop('schemes', None)
        yield Specification(dict(swagger=json.dumps(swagger, indent=2)))
        yield SwaggerSpec(dict(swagger=yaml.dump(self.swagger.origin_data,
                                                 default_flow_style=False)))
        yield Setup(views)
        yield SetupConfig()
        yield Server(views)
        yield Wsgi(views)
        yield Dockerfile(views)
        yield DockerEntrypoint(views)
        yield Manifest()
        yield Makefile(views)
        yield Readme(views)
        yield Requirements()
        yield ServiceConfig(dict(base_path=self.swagger.base_path))
        yield Tox(views)
        yield Test()
        yield TestCode(views)
