"""
Application Module registration
"""

from app.core import include

default_module = include('default.controllers', '/')
dashboard_module = include('dashboard.controllers', '/dashboard')
users_module = include('users.controllers', '/users')
roles_module = include('roles.controllers', '/roles')
department_module = include('departments.controllers', '/departments')


modules = (
    default_module,
    dashboard_module,
    users_module,
    roles_module,
    department_module
)
