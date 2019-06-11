import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# tell the log in manager what the login route is (for the redirect on not logged in users)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config) # import config variables and execute for app

    db.init_app(app)
    db_file_path = os.path.join(app.root_path, 'site.db')

    if not os.path.isfile(db_file_path): # if there is no db create db
        print('db not found - creating db')
        db.create_all()
    else:
        print('db already created')

    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.init_app(app)

    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app