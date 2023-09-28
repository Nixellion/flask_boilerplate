'''
Authentication related views
'''

from flask import Blueprint, request, redirect, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from utilities.string_utils import render_template_themed
from configuration import read_config
from loguru import logger as log
config = read_config()

# region LOGIN
app = Blueprint("auth", __name__)
login_manager = LoginManager()

class User(UserMixin):
    """
    User class for Flask.
    UserMixin can't be combined with Peewee model, because it will override some functions like get_id.
    """

    def __init__(self, id):
        self.user = None
        self.id = "username"
        # self.access_level = self.userData['access_level']

    def check_password(self, password):
        log.warning("CHECK PASSWORD SKIPPED, DEV MODE NEEDS IMPLEMENTATION")
        return True
    
    def has_clearance(self, level):
        log.warning("CHECK CLEARANCE SKIPPED, DEV MODE NEEDS IMPLEMENTATION")
        return True


    def __repr__(self):
        return self.name


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username)

        if user.check_password(password):
                login_user(user)
                # client_ip = get_real_ip(request)
                # log.debug("Redirect to: {}".format(redirect_to))
                return redirect("/admin")
        else:
            return Response("Username or password incorrect")
    else:
        return render_template_themed("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/login_test")
@login_required
def login_test():
    return Response("You are logged in.")
# endregion

