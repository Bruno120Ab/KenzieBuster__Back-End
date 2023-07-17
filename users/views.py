from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Request, Response, status

from users.serializers import UserSerializer, LoginSerializer
from users.permission import AuthenticatedUser
from users.models import User

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

class UserView(APIView):
  def post(self, request: Request):
      serializer = UserSerializer(data=request.data)

      serializer.is_valid(raise_exception=True)

      serializer.save()

      return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
  def post(self, request: Request):
      serializer = LoginSerializer(data=request.data)
      
      serializer.is_valid(raise_exception=True)

      user = authenticate(**serializer.validated_data)

      if not user: return Response({"detail": "No active account found with the given credentials"}, status= status.HTTP_401_UNAUTHORIZED)

      refresh = RefreshToken.for_user(user)

      token_dict = {"refresh": str(refresh), "access": str(refresh.access_token)}

      return Response(token_dict, status.HTTP_200_OK)    

class UserDetailsView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated, AuthenticatedUser | IsAdminUser]

  def get(self, request: Request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    self.check_object_permissions(request=request, obj=user_obj)

    serializer = UserSerializer(user_obj)

    return Response(data = serializer.data, status = status.HTTP_200_OK)

  def patch(self, request: Request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    self.check_object_permissions(request=request, obj=user_obj)

    serializer = UserSerializer(user_obj, request.data, partial=True)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(data = serializer.data, status = status.HTTP_200_OK)