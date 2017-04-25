from __future__ import absolute_import
from collections import OrderedDict

from .base import Code, CodeGenerator
from .parser import schema_var_name
import six


class Schema(Code):

    template = 'jsonschema/schemas.tpl'
    dest_template = '%(package)s/schemas.py'
    override = True


def _parameters_to_schemas(params):
    locations = ['body', 'header', 'formData', 'query']
    for location in locations:
        required = []
        properties = {}
        type_ = 'object'
        for param in params:
            if param.get('in') != location:
                continue
            if location == 'body':
                # schema is required `in` is `body`
                yield location, param['schema']
                continue

            prop = param.copy()
            prop.pop('in')
            if param.get('required'):
                required.append(param['name'])
                prop.pop('required')
            properties[prop['name']] = prop
            prop.pop('name')
        if len(properties) == 0:
            continue
        yield location, dict(required=required, properties=properties)


def build_data(swagger):

    # (endpoint, method) = {'body': schema_name or schema,
    #                       'query': schema_name, ..}
    validators = OrderedDict()
    # (endpoint, method) = {'200': {'schema':, 'headers':, 'examples':},
    #                       'default': ..}
    filters = OrderedDict()
    # (endpoint, method) = [scope_a, scope_b]
    scopes = OrderedDict()

    # path parameters
    for path, _ in swagger.search(['paths', '*']):
        path_param = []
        try:
            path_param = swagger.get(path + ('parameters',))
        except KeyError:
            pass

        # methods
        for p, data in swagger.search(path + ('*',)):
            if p[-1] not in ['get', 'post', 'put', 'delete',
                             'patch', 'options', 'head']:
                continue
            method_param = []
            try:
                method_param = swagger.get(p + ('parameters',))
            except KeyError:
                pass

            endpoint = p[1]  # p: ('paths', '/some/path', 'method')
            method = p[-1].upper()

            # parameters as schema
            validator = dict(_parameters_to_schemas(path_param + method_param))
            if validator:
                validators[(endpoint, method)] = validator

            # responses
            responses = data.get('responses')
            if responses:
                filter = {}
                for status, res_data in six.iteritems(responses):
                    if isinstance(status, int) or status.isdigit():
                        filter[int(status)] = dict(
                            headers=res_data.get('headers'),
                            schema=res_data.get('schema')
                        )
                filters[(endpoint, method)] = filter

            # scopes
            for security in data.get('security', []):
                scopes[(endpoint, method)] = list(security.values()).pop()
                break

    schemas = OrderedDict([(schema_var_name(path), swagger.get(path))
                          for path in swagger.definitions])

    data = dict(
        schemas=schemas,
        validators=validators,
        filters=filters,
        scopes=scopes,
    )
    return data


class SchemaGenerator(CodeGenerator):

    def _process(self):
        yield Schema(build_data(self.swagger))


