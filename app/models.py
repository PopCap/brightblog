from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin

#flask_login doesn't know anything about database so must define own user_loader function
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.Text())
    # passing datetime.utcnow as function instead of its result so it can be
    # can be handled server side and display user's local time
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}: {}>'.format(self.title, self.body)

class Comment(db.Model):
    _N = 6 # number of digits used for each component of path

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')
        
    def save(self):
        db.session.add(self)
        # first save comment without path to get assigned an id
        db.session.commit()
        prefix = self.parent.path + '.' if self.parent else ''
        # if (self.parent) self.post_id = self.parent.post_id
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        # save again after being able to build path
        db.session.commit()
    
    # used to get indentation level for nested comments
    def level(self):
        return len(self.path) # self._N - 1