from {{ service_name }}.{{ module.name }}.resources import {{ module.name | format_as('class') }}
from {{ service_name }}.app import rbac


class {{ module.name | format_as('class') }}Impl({{ module.name | format_as('class') }}):

    def __init__(self):
        # TODO: Implement the class
        pass
