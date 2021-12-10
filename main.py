from flask import Flask, render_template, url_for, request, redirect
import tmdb_client
from datetime import date
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class FavouriteMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)



@app.route('/')
def homepage():
    movie_list = ['popular', 'top_rated', 'upcoming', 'now_playing']
    selected_list = request.args.get('list_type', "popular")
    if selected_list not in movie_list:
        selected_list = movie_list[0]
    movies = tmdb_client.get_movies(how_many=30, list_type=selected_list)
        
    return render_template("homepage.html", movies=movies, current_list=selected_list, movie_list=movie_list)


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
   details = tmdb_client.get_single_movie(movie_id)
   cast = tmdb_client.get_single_movie_cast(movie_id)
   return render_template("movie_details.html", movie=details, cast=cast)


@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route('/today')
def today():
    movies = tmdb_client.airing_today()
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    return render_template('today.html', movies=movies, today=today)


@app.route("/favourites/add", methods=['POST'])
def add_to_favorites():
    all_favourites = FavouriteMovie.query.all()
    FAVOURITES = [movie.movie_id for movie in all_favourites]
    data = request.form
    movie_id = data.get('movie_id')
    if movie_id:
        if int(movie_id) in FAVOURITES:
            return redirect(url_for('homepage'))
        else:
            movie_to_add = FavouriteMovie(movie_id=movie_id)
            db.session.add(movie_to_add)
            db.session.commit()         
    return redirect(url_for('homepage'))


@app.route('/favourites')
def favourite_movies():
    all_favourites = FavouriteMovie.query.all()
    FAVOURITES = [movie.movie_id for movie in all_favourites]
    if FAVOURITES:
        movies = []
        for movie_id in FAVOURITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template('favourites.html', movies=movies)
    

@app.route('/favourites/delete/<int:id>')
def delete_movie(id):
    movie_to_delete = FavouriteMovie.query.filter_by(movie_id=id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('favourite_movies'))


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}



if __name__ == '__main__':
    app.run(debug=True)