import bcrypt
from model.project_configuration import app, db
from model.User import User
from model.PasswordEntry import PasswordEntry

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin_user = User("lul", bcrypt.hashpw("lul".encode(), bcrypt.gensalt()).decode("utf-8"))
        db.session.add(admin_user)
        db.session.commit()
    app.run(host="0.0.0.0", port=8080)
