from model.project_configuration import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String)
    double_submit_num = db.Column(db.Integer, default=0)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
