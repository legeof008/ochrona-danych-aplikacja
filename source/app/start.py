from controller.PasswordEntryController import entry_handler
from controller.UserController import user_handler
from model.project_configuration import app, db

""" Register controllers"""
app.register_blueprint(user_handler)
app.register_blueprint(entry_handler)
with app.app_context():
    db.create_all()
 
if __name__ == '__main__':
#    with app.app_context():
#        db.create_all()
    #    admin_user = User("lul", bcrypt.hashpw("lul".encode(), bcrypt.gensalt()).decode("utf-8"))
    #    db.session.add(admin_user)
    #    db.session.commit()
   app.run(host="0.0.0.0")
