from flask import current_app


@current_app.context_processor
def base_processor():
    def copyright():
        return '%s' % current_app.config.get('COPY_RIGHT')

    return dict(
        copyright=copyright()
    )