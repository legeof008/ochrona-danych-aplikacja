import bcrypt
from flask_login import login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from model.User import User
from model.project_configuration import login_manager


@login_manager.user_loader
def user_loader(user_id: int) -> User:
    return User.query.get(user_id)


def is_logged():
    return current_user.is_authenticated


def list_users() -> [str]:
    try:
        all_users_queried = User.query.all()
        all_users = []
        for user in all_users_queried:
            all_users.append(user.username)
        return all_users
    except:
        print("Problem getting users !")
        return None


class UserHandlingService:
    def __init__(self, database: SQLAlchemy):
        self.database = database

    def register(self, username: str, password: str) -> bool:
        user = User.query.get(username)
        if user:
            """ Cannot register the same user twice """
            return False
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User(username, hashed_password)
        try:
            self.database.session.add(new_user)
            self.database.session.commit()
        except:
            print("Unable to add user to the database !")
            return False
        return True

    def login(self, username: str, password: str) -> bool:
        user = User.query.get(username)
        if not user:
            """ No such user exists """
            return False
        if bcrypt.checkpw(password.encode(), user.password):
            """ User was able to log in"""
            user.authenticated = True
            self.database.session.add(user)
            self.database.session.commit()
            login_user(user, remember=True)
            return True
        return False

    def logout(self):
        user = current_user
        user.authenticated = False
        self.database.session.add(user)
        self.database.session.commit()
        logout_user()
