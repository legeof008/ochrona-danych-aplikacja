from controller.PasswordEntryController import entry_handler
from controller.UserController import user_handler
from model.project_configuration import app, db

""" Register controllers"""
app.register_blueprint(user_handler)
app.register_blueprint(entry_handler)
with app.app_context():
    db.create_all()
 
if __name__ == '__main__':
    app.run(host="0.0.0.0")
