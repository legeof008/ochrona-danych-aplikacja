from model.project_configuration import db


class PasswordEntry(db.Model):
    __tablename__ = 'passwordentry'
    id = db.Column(db.Integer, unique=True)
    username = db.Column(db.Integer, primary_key=True, unique=True)
    password = db.Column(db.LargeBinary, nullable=False)
    servicename = db.Column(db.String)
    owner = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, username, password, servicename, owner):
        self.username = username
        self.password = password
        self.servicename = servicename
        self.owner = owner

    def get_id(self):
        return self.id

    def get_owner(self):
        return self.owner

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_servicename(self):
        return self.servicename

