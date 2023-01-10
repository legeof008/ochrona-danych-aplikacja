from flask import Blueprint, request, render_template, redirect, make_response
from flask_login import login_required, current_user

from controller.service.PasswordEntryService import PasswordEntryService, authorized_with, decrypt_with
from controller.service.UserHandlingService import password_safe
from model.project_configuration import db

entry_handler = Blueprint('entry_handler', __name__, template_folder='/static/templates', static_folder='../static',
                          static_url_path='')
service = PasswordEntryService(db)


@entry_handler.route('/entry', methods=["POST", "GET"])
@login_required
def entries():
    all_entries = service.list_by_name(current_user.username)
    return render_template("entry.html", entries=all_entries, user=current_user.username)


@entry_handler.route('/entry-add', methods=["GET", "POST"])
@login_required
def add_entry():
    if request.method == "GET":
        return render_template("entry-add.html")

    username = request.json.get('username')
    password = request.json.get('password')
    servicename = request.json.get('servicename')
    special_password = request.json.get('special_password')

    if not special_password:
        return make_response("The encryption password is required !")
    if not password_safe(special_password):
        return make_response("The encryption password is not safe !")
    if authorized_with(request):
        service.add(username, password, special_password, servicename, current_user.username)
    return redirect("/entry", 302)


@entry_handler.route('/entry-delete', methods=["POST"])
@login_required
def delete_entry():
    if not authorized_with(request):
        return "Not authorized to delete entry", 401
    entry_id = request.json.get('id')
    if service.delete(int(entry_id)):
        return redirect("/entry", 302)
    else:
        return "Not authorized to delete entry", 401


@entry_handler.route('/entry-reveal', methods=["POST"])
@login_required
def reveal_entry():
    if not authorized_with(request):
        return "Not authorized to reveal entry", 401
    entry_id = request.json.get('id')
    if not request.json.get('password'):
        return "Password not present", 400
    password = request.json.get('password')
    entry = service.get(entry_id)
    plaintext = decrypt_with(entry.username, password, entry.password, entry.salt, entry.mac_key)[0:-entry.nonce_len]
    return plaintext, 200
