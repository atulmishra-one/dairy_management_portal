"""
Application Module registeration
"""

from app.core import include

default_module = include('default.controllers', '/')


modules = (
    default_module,
)

