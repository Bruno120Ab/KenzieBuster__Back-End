from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status
from rest_framework import permissions

from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.permission import AnyUserOrEmployee
from movies.models import Movie

from django.shortcuts import get_object_or_404

class MovieView(APIView, PageNumberPagination):
  authentication_classes = [JWTAuthentication]
  permission_classes = [AnyUserOrEmployee]

  def get(self, request):
    movies = Movie.objects.get_queryset().order_by('id')

    result_page = self.paginate_queryset(movies, request)

    serializer = MovieSerializer(instance=result_page, many=True)

    return self.get_paginated_response(data = serializer.data)

  def post(self, request: Request):
    serializer = MovieSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save(user=request.user)

    return Response(data = serializer.data, status = status.HTTP_201_CREATED)

class MovieDetailView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [AnyUserOrEmployee]

  def get(self, request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    serializer = MovieSerializer(movie)

    return Response(data = serializer.data, status = status.HTTP_200_OK)

  def delete(self, request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    movie.delete()

    return Response(status = status.HTTP_204_NO_CONTENT)

class MovieOrdervView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request: Request, movie_id: int) -> Response:
    movie = get_object_or_404(Movie, id=movie_id)

    user = request.user

    serializer = MovieOrderSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save(movie=movie, user=user)

    return Response(data = serializer.data, status = status.HTTP_201_CREATED)
