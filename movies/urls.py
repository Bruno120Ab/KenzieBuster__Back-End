from django.urls import path

from movies.views import MovieView, MovieDetailView, MovieOrdervView

urlpatterns =  [ 
  path("movies/", MovieView.as_view()),
  path("movies/<int:movie_id>/", MovieDetailView.as_view()),
  path("movies/<int:movie_id>/orders/", MovieOrdervView.as_view()),
]