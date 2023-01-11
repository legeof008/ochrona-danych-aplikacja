from model.project_configuration import db


class PasswordEntry(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    servicename = db.Column(db.String)
    owner = db.Column(db.String, nullable=False)

    salt = db.Column(db.LargeBinary, nullable=False)
    mac_key = db.Column(db.LargeBinary, nullable=False)
    nonce_len = db.Column(db.Integer)

    def __init__(self, username: str, password: bytes, servicename: str, owner: str, salt: bytes,
                 mac_key: bytes, nonce_len: int):
        self.username = username
        self.password = password
        self.servicename = servicename
        self.owner = owner
        self.salt = salt
        self.mac_key = mac_key
        self.nonce_len = nonce_len

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
