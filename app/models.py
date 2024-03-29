from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serialiser
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                            default='default.jpg')
    # the image file is going to be hashed so it is 20 characters long
    password = db.Column(db.String(60), nullable=False)
    # the password will also be hashed but to 60
    posts = db.relationship('Post', backref='author', lazy=True)
    # this posts relationship is not a column but an addtional query that runs in the back
    # ground to collect all the posts from a user

    def get_reset_token(self, expires_sec=1800): # 30 mins
        '''returns a token in utf-8'''
        s = Serialiser(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        '''Checks the token is still live - if not error it returns the user'''
        s = Serialiser(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # this user_id is a column but we are letting the db know that it is a key from a
    # another table in the db from the user model

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
