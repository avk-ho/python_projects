from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app)

app.app_context().push()

##USER AUTHENTICATION
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Prevent access to users other than the admin, ie the user with id==1
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        
        return f(*args, **kwargs)

    return decorated_function
        

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(1000), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # One to Many (BlogPost)
    posts = db.relationship("BlogPost", backref="author")
    # One to Many (Comment)
    comments = db.relationship("Comment", backref="user")

    def get_id(self):
        return super().get_id()

    def is_authenticated(self):
        return super().is_authenticated

    def is_active(self):
        return super().is_active

    def is_anonymous(self):
        return super().is_anonymous

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Many to One (User)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # One to Many (Comment)
    comments = db.relationship("Comment", backref="blogpost")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # Many to One (User)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Many to One (BlogPost)
    blogpost_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))

db.create_all()


##ROUTES
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data

        # User doesn't exist
        if User.query.filter_by(email=email).first() is None:
            password = generate_password_hash(
                register_form.password.data, method="pbkdf2:sha256",
                salt_length=8)

            new_user = User(
                email=register_form.email.data,
                name=register_form.name.data,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("get_all_posts"))

        # User already exists
        else:
            flash("You already have an account with that email. Please log in instead.")
            return redirect(url_for("login"))

    return render_template("register.html", form=register_form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        # Correct email
        if user is not None:
            password = form.password.data
            # Correct password
            if check_password_hash(password=password, pwhash=user.password):
                login_user(user)

                return redirect(url_for("get_all_posts"))
        
        flash("Wrong email/password. Please retry or register.")

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    comments = requested_post.comments

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        # User is not logged in
        if not current_user.is_authenticated:
            flash("Please log in or register to comment.")

            return redirect(url_for("login"))

        # User is logged in
        else:
            new_comment = Comment(
                text=comment_form.comment.data,
                blogpost=requested_post,
                user=current_user
            )
            db.session.add(new_comment)
            db.session.commit()

            return redirect(url_for("show_post", post_id=requested_post.id))
    
    return render_template("post.html", post=requested_post, comments=comments, form=comment_form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["POST", "GET"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
