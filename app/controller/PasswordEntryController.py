from flask import Blueprint, request, render_template, redirect
from flask_login import login_required, current_user

from controller.service.PasswordEntryService import PasswordEntryService, list_all
from model.project_configuration import db

entry_handler = Blueprint('entry_handler', __name__, template_folder='/static/templates', static_folder='../static',
                          static_url_path='')
service = PasswordEntryService(db)


@entry_handler.route('/entry', methods=["POST", "GET"])
@login_required
def entries():
    all_entries = service.list_by_name(request.form.get('search_by_user')) if request.method == "POST" else list_all()
    return render_template("entry.html", entries=all_entries, user=current_user.username)


@entry_handler.route('/entry-add', methods=["GET", "POST"])
@login_required
def add_entry():
    if request.method == "GET":
        return render_template("entry-add.html")
    username = request.form.get('username')
    password = request.form.get('password')
    servicename = request.form.get('servicename')
    special_password = request.form.get('special_password')
    if not special_password:
        return render_template("entry-add.html",result_info="The encryption password is required !")

    service.add(username, password, special_password, servicename, current_user.username)
    return redirect("/entry", 302)


@entry_handler.route('/entry-delete', methods=["POST"])
@login_required
def delete_entry():
    entry_id = request.args.get('id')
    if service.delete(int(entry_id)):
        return redirect("/entry", 302)
    else:
        return "Not authorized to delete entry", 404
