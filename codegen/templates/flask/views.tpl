from {{ service_name }}.resources import {{ service_name | format_as('class') }}
from {{ service_name }}.app import rbac


class {{ service_name | format_as('class') }}Impl({{ service_name | format_as('class') }}):
    # TODO: Implement handler methods for defined endpoints
    pass
