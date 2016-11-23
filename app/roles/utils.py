from flask import render_template
from flask import current_app
from flask import url_for


def user_functions():
    for rule in current_app.url_map.iter_rules():
        if not ( rule.endpoint.endswith('static') or rule.endpoint.endswith('logout') ) :
            yield "{:50s}".format(rule.endpoint)