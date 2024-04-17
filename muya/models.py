from datetime import datetime
from muya import db, login_Manager
from flask_login import UserMixin

@login_Manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    service = db.relationship('Service', backref='author', lazy=True)
    review = db.relationship('Review', backref='review_author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}' )"
    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_files = db.Column(db.String(120), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review = db.relationship('Review', backref='service_name', lazy=True)

    def __repr__(self):
        return f"Service('{self.title}','{self.date_posted}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like_or_dislike = db.Column(db.Boolean, nullable=False, default=True)
    date_posted = db.Column(db.DateTime(120), nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.comment}','{self.date_posted}','{self.like_or_dislike}')"