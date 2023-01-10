import json

from flask import Blueprint, request, render_template, redirect, make_response
from flask_login import login_required, current_user

from controller.service.UserHandlingService import UserHandlingService, is_logged, password_criteria
from model.project_configuration import db

user_handler = Blueprint('user_handler', __name__, template_folder='../static/templates')
service = UserHandlingService(db)


@user_handler.route("/", methods=["GET"])
def redirect_login():
    return redirect("/login", 301)


@user_handler.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.cookies.get("token") and is_logged(int(request.cookies.get("token"))):
        return redirect("/entry", 302)

    form_username = request.form.get("form-username")
    form_password = request.form.get("form-password")

    if service.login(form_username, form_password):
        response = make_response(redirect("/entry", 302))
        response.set_cookie("XRS", value=str(current_user.double_submit_num))
        return response
    else:
        return render_template("login.html", result_info="Wrong login or password")


@user_handler.route("/logout", methods=["GET"])
@login_required
def logout():
    service.logout()
    return redirect("/login", 302)


@user_handler.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get('username')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')

    if password != password_repeat:
        return render_template("register.html", result_info="Passwords do not match")
    elif service.register(username, password):
        return redirect("/login", 302)
    else:
        return render_template("register.html",
                               result_info="User already exists or password is not strong enough or username is not "
                                           "as defined.")


@user_handler.route("/password", methods=["POST"])
def password_check():
    password = request.json.get("check")

    return json.dumps(password_criteria(password))
