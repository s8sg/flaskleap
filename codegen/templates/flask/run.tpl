#!/usr/bin/env python
from {{ service_name }}.app import create_app


def run_app():
    app = create_app('config/config.py')
    app.run()
