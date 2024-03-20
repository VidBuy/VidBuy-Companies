
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from .encrypt_k7s2 import encrypter, decrypter, validate_dc
from os.path import *
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .VertexClient import dbORM


db = SQLAlchemy()
DB_NAME = "vdc-db.db"

def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'akmkakddopeaceaksmdak2223#'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///Database.db'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
      return User.query.get(int(id))

    @app.errorhandler(500)
    def internal_server_error(e):
      return render_template('broken-page.html'), 500

    FL_Login = LoginManager(app)
    FL_Login.login_view = 'login'


    class UserClass:
        def __init__(self, id):
            self.id = id

        @staticmethod
        def is_authenticated():
            return True

        @staticmethod
        def is_active():
            return True

        @staticmethod
        def is_anonymous():
            return False

        def get_id(self):
            return self.id


        @FL_Login.user_loader
        def load_user(id):
            try:
                u = dbORM.find_one("USER", "id", id)
                if not u:
                    return None
                return UserClass(id=dbORM.get_all("USER")[f'{u}']['id'])
            except:
                anonymous = {
                    "0": {
                        'id': '0',
                        'name': 'NULL',
                        'username': 'NULL',
                        'email': 'NULL',
                        'password': 'NULL',
                        'gender': 'NULL',
                        'is_payed_for': 'NULL',
                        'is_admin': 'NULL'
                    }
                }
                return UserClass(id=anonymous['0']['id'])

    @app.route("/login", methods=['GET', 'POST']) 
    def login():
        User = dbORM.get_all("USER")

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = dbORM.find_one("USER", "email", email)
            if user and check_password_hash(User[f'{user}']['password'], password):
                # flash("Logged in successfully.", category='Success')

                t_user = UserClass(id=f'{user}')

                login_user(t_user, remember=True)

                # flash("What do you think of VidBuy?", category='Prompt')

                return redirect(url_for('views.viewDashBoard'))
            else:
                flash("Incorrect password or email. Please try again.", category="Error occurred")

        return render_template('login.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully.", category='Success')
        return redirect(url_for('login'))

    @app.route("/signup", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            gender = request.form.get("gender")
            password1 = request.form.get('password')
            password2 = request.form.get('password2')
            soo = request.form.get("state_of_origin")
            age = request.form.get("age")
            sor = request.form.get("state_of_residence")
            dob = request.form.get("date_of_birth")
            country = request.form.get("country")
            gender = request.form.get("gender")
            individuality_status = request.form.get("individuality_status")


            user = dbORM.find_one("USER", 'email', email)

            if user:
                flash("Email is already taken. Please use a different email.", category='Error occurred')
            elif len(email) < 4:
                flash('Invalid email: Email must be at least 4 characters long.', category='Error occurred')
            elif len(name) < 2:
                flash('Invalid name: Name must be at least 2 characters long.', category='Error occurred')
            elif password1 != password2:
                flash('Passwords do not match. Please re-enter your password.', category='Error occurred')
            elif len(password1) < 8:
                flash('Password is too short. It must be at least 8 characters long.', category='Error occurred')
            else:
                hashed_password = generate_password_hash(password1)
                new_user = {
                    'name': name,
                    'username': f"@{name.replace(' ', '').lower()}",
                    'email': email,
                    'password': password1,
                    'age': age,
                    'state_of_origin': soo,
                    'state_of_residence': sor,
                    'date_of_birth': dob,
                    'country': country,
                    'gender': gender,
                    'individuality_status': individuality_status,
                    'app_theme': 'light'
                }


                # for key, details in new_user.items():
                dbORM.add_entry("USER", f"{encrypter(str(new_user))}")

                flash('Account created successfully.', category='Success')

                t_user = UserClass(id=dbORM.find_one("USER", 'email', email))

                login_user(t_user, remember=True)

                return redirect(url_for('views.viewDashBoard'))

        return render_template("signup.html")

    return app

def create_db(the_app):
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    if not isfile(db_path):
        with the_app.app_context():
            db.create_all()
        print("Database created!")

    