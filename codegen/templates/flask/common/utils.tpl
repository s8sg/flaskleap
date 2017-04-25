from flask import (Response, jsonify)


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class APIResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, response, **kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if response.startswith('<?xml'):
                kwargs['mimetype'] = 'application/xml'
            if response.startswith('<!DOCTYPE html'):
                kwargs['mimetype'] = 'text/html'
        return super(APIResponse, self).__init__(response, **kwargs)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(APIResponse, cls).force_type(rv, environ)
