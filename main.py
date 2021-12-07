from flask import Flask, render_template, url_for, request, redirect
import tmdb_client
from datetime import date



app = Flask(__name__)


FAVOURITES = set()




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
    return render_template('today.html', movies=movies, today=today)


@app.route("/favourites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVOURITES.add(movie_id)
    return redirect(url_for('homepage'))


@app.route('/favourites')
def favourite_movies():
    if FAVOURITES:
        movies = []
        for movie_id in FAVOURITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movie_details['star'] = 1
            movies.append(movie_details)
    else:
        movies = []
    
    return render_template('favourites.html', movies=movies)
    


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}



if __name__ == '__main__':
    app.run(debug=True)