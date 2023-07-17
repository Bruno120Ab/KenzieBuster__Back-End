from django.urls import path
from .views import  UserView, LoginView, UserDetailsView

urlpatterns =  [ 
  path("users/", UserView.as_view()),
  path("users/login/", LoginView.as_view()),
  path("users/<int:user_id>/", UserDetailsView.as_view())
]