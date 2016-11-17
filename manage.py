from flask_script import Manager
from flask_script import Server
from flask_script import Shell

from app.application import initialize_app

try:
    from app.config.production import ProductionConfig as config_object
except ImportError:
    from app.config.local import LocalConfig as config_object


current_app = initialize_app(config_object)


def _make_context():
    return dict(app=current_app)


manager = Manager(current_app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def help():
    print "Hello How may i help you ?\n"

    
if __name__ == '__main__':
    manager.run()
