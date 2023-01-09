import random
import re

import bcrypt
from flask_login import login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from model.User import User
from model.project_configuration import login_manager

username_pattern = "^([a-z]|[A-Z]|[0-9]){4,16}$"


def password_criteria(password: str) -> {}:
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 4

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    # overall result
    password_ok = (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password': password_ok,
        'length': length_error,
        'digits': digit_error,
        'uppercase': uppercase_error,
        'lowercase': lowercase_error,
        'symbol': symbol_error,
    }


def username_safe(username: str) -> bool:
    if re.search(username_pattern, username):
        return True
    return False


def password_safe(password: str) -> bool:
    run_check = password_criteria(password)
    for criteria in run_check:
        if run_check[criteria]:
            return False
    return True


@login_manager.user_loader
def user_loader(user_id: int) -> User:
    return User.query.get(user_id)


def is_logged(authenticator: int):
    return current_user.is_authenticated and current_user.double_submit_num == authenticator


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
        elif not username_safe(username):
            """ Username is not safe by the standards in documentation"""
            return False
        elif not password_safe(password):
            """ Password is not safe by the standards in documentation"""
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
        if not username_safe(username):
            """ Username wasn't safe """
            return False
        user = User.query.get(username)
        if not user:
            """ No such user exists """
            return False
        if bcrypt.checkpw(password.encode(), user.password):
            """ User was able to log in"""
            user.authenticated = True
            #
            user.double_submit_num = random.randint(500000000, 10000000000)
            #
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
