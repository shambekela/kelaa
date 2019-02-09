from flask_script import Manager, Shell
from app import create_app, db, flask_whooshalchemyplus
from flask_migrate import Migrate, MigrateCommand
from app.models import *
import os

app = create_app(os.environ.get('ENVIRONMENT') or 'development')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
	return dict(app=app, db=db)

with app.app_context():
	flask_whooshalchemyplus.whoosh_index(app, Question)

if __name__ == '__main__':
	manager.run()