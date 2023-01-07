import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
import requests

TMBD_API_KEY = "KEY"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEY'
Bootstrap(app)

# Setting up the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Creating the Movie table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.String)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String)

# db.create_all()

# Adding one entry to the Movie table
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg",
# )
# db.session.add(new_movie)
# db.session.commit()

# Creating the edit rating/review form
class EditRatingReviewForm(FlaskForm):
    new_rating = FloatField(label="Your rating out of 10 (ex: 7.8)", validators=[DataRequired()])
    new_review = StringField(label="Your new review (optionnal)")
    submit = SubmitField("Done")

# Creating the add movie form
class AddMovieForm(FlaskForm):
    title = StringField(label="Movie title", validators=[DataRequired()])
    submit = SubmitField(label="Add movie")


# Routes
@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating.desc()).all()
    rank = 1
    for movie in all_movies:
        # print(movie.title)
        movie.ranking = rank
        rank += 1

    db.session.commit()
    return render_template("index.html", movies=reversed(all_movies))

@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = AddMovieForm()

    if form.validate_on_submit():
        # Requesting movie information on themoviedb.org
        tmdb_request_url = "https://api.themoviedb.org/3/search/movie"

        parameters = {
            "api_key": TMBD_API_KEY,
            "query": form.title.data,
        }

        response = requests.get(url=tmdb_request_url, params=parameters)
        data = response.json()

        movies_data = data["results"]

        

        return render_template("select.html", movies=movies_data)

    return render_template("add.html", form=form)


@app.route("/select_movie/<id>", methods=["POST", "GET"])
def select_movie(id):
    tmdb_request_url = f"https://api.themoviedb.org/3/movie/{id}"

    parameters = {
        "api_key": TMBD_API_KEY,
    }

    response = requests.get(url=tmdb_request_url, params=parameters)
    data = response.json()

    if response.ok:
        img_url_base = "https://image.tmdb.org/t/p/w500"

        title = data["original_title"]
        year = data["release_date"]
        poster = img_url_base + data['poster_path']
        description = data["overview"]
        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            img_url=poster,
        )
        db.session.add(new_movie)
        db.session.commit()

        movie = Movie.query.filter_by(title=title).first()
        movie_id = movie.id

        return redirect(url_for("edit_rating", id=movie_id))

    return render_template("select.html")


@app.route("/edit_rating/<id>", methods=["GET", "POST"])
def edit_rating(id):
    movie = Movie.query.get(id)
    form = EditRatingReviewForm()
    if form.validate_on_submit():
        if form.new_review.data is not None:
            movie.review = form.new_review.data
        movie.rating = form.new_rating.data
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)

@app.route("/delete_movie/<id>")
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
