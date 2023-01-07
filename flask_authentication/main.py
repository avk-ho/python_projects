from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def is_authenticated(self):
        return super().is_authenticated
    
    def is_active(self):
        return super().is_active

    def is_anonymous(self):
        return super().is_anonymous

    def get_id(self):
        return super().get_id()

#Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # User currently does not exist
        if User.query.filter_by(email=request.form["email"]).first() is None:
            password = generate_password_hash(
                request.form["password"],
                method="pbkdf2:sha256",
                salt_length=8
            )
            new_user = User(
                email=request.form["email"],
                password=password,
                name=request.form["name"]
            )
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)

            return redirect(url_for("secrets"))

        # User already exists (email present in database)
        else:
            flash("You've already signed up with that email, log in instead!")

            return redirect(url_for("login"))


    return render_template("register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        submitted_email = request.form["email"]
        submitted_password = request.form["password"]
        user = User.query.filter_by(email=submitted_email).first()
        if user is not None:
            if check_password_hash(password=submitted_password, pwhash=user.password):
                login_user(user)

                return redirect(url_for("secrets", name=current_user.name))

        error = "The login are wrong or do not exist. Please try again."

    return render_template("login.html", error=error)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    return send_from_directory("static", "files/cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
