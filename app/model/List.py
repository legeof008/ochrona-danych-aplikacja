from model.project_configuration import db


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, unique=True)
    salt = db.Column(db.LargeBinary, nullable=False)
    mac_key = db.Column(db.LargeBinary, nullable=False)
    owner = db.Column(db.String, nullable=False)

    def __init__(self, salt, mac_key, owner):
        self.salt = salt
        self.mac_key = mac_key
        self.owner = owner

    def get_id(self):
        return self.id
