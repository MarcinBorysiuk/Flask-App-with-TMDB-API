import tmdb_client
from unittest.mock import Mock


def test_get_movies_list(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)


   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
    mock_single_movie = "movie 500"
    single_movie_mock = Mock()
    single_movie_mock.return_value = mock_single_movie
    monkeypatch.setattr("tmdb_client.get_single_movie", single_movie_mock)
    single_movie = tmdb_client.get_single_movie(500)
    assert single_movie == mock_single_movie

   
def test_get_movie_images(monkeypatch):
   mock_movie_image = "movie500.jpg"
   movie_image_mock = Mock()
   movie_image_mock.return_value = mock_movie_image
   monkeypatch.setattr("tmdb_client.get_movie_images", movie_image_mock)
   movie_image = tmdb_client.get_movie_images(500)
   assert movie_image == mock_movie_image


def test_get_single_movie_cast(monkeypatch):
    mock_single_movie_cast = "movie 700 cast"
    cast_single_movie_mock = Mock()
    cast_single_movie_mock.return_value = mock_single_movie_cast
    monkeypatch.setattr("tmdb_client.get_single_movie", cast_single_movie_mock)
    single_movie_cast = tmdb_client.get_single_movie(700)
    assert single_movie_cast == mock_single_movie_cast