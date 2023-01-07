from flask import Blueprint, request, render_template, redirect
from flask_login import login_required

from controller.service.UserHandlingService import UserHandlingService, is_logged
from model.project_configuration import db

user_handler = Blueprint('user_handler', __name__, template_folder='../static/templates')
service = UserHandlingService(db)


@user_handler.route("/", method=["GET"])
def redirect_login():
    return redirect("/login", 301)


@user_handler.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html")
    if is_logged():
        return redirect("/entry")

    form_username = request.form.get("form-username")
    form_password = request.form.get("form-password")

    if service.login(form_username, form_password):
        return redirect("/entry")
    else:
        return render_template("login_page.html", result_info="Wrong login or password")


@user_handler.route("/logout", methods=["GET"])
@login_required
def logout():
    return redirect(service.logout(), 302)


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
        return render_template("register.html", result_info="User like this already exists")
