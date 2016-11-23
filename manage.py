from flask_script import Manager
from flask_script import Server
from flask_script import Shell
from flask_assets import ManageAssets
from flask_migrate import Migrate, MigrateCommand

from app.services.extension import sqlalchemy as db

from app.application import initialize_app

try:
    from app.config.production import ProductionConfig as config_object
except ImportError:
    from app.config.local import LocalConfig as config_object


current_app = initialize_app(config_object)


def _make_context():
    return dict(app=current_app)
    
migrate = Migrate(current_app, db)

manager = Manager(current_app)
manager.add_command("runserver", Server(host='0.0.0.0'))
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("assets", ManageAssets(current_app))
manager.add_command('db', MigrateCommand)


@manager.command
def help():
    print "Hello How may i help you ?\n"

@manager.command
def create_all():
    with current_app.app_context():
        tables_before = set(db.engine.table_names())
        db.create_all()
        tables_after = set(db.engine.table_names())
    created_tables = tables_after - tables_before
    for table in created_tables:
        print 'Created table: {}'.format(table)



if __name__ == '__main__':
    manager.run()
