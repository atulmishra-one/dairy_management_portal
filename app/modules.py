"""
Application Module registeration
"""

from app.core import include

default_module = include('default.controllers', '/', 'templates')
dashboard_module = include('dashboard.controllers', '/dashboard', 'templates', 'static')
users_module = include('users.controllers', '/users', 'templates', 'static')
roles_module = include('roles.controllers', '/roles', 'templates', 'static')


modules = (
    default_module,
    dashboard_module,
    users_module,
    roles_module
)
