from flask import current_app

@current_app.template_filter()
def site_title(s):
    return "%s - %s" % (current_app.config.get('SITE_TITLE'), s)