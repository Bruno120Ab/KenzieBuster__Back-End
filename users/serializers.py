from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
  id          = serializers.IntegerField(read_only = True)
  username    = serializers.CharField()
  email       = serializers.EmailField()
  first_name  = serializers.CharField(max_length = 50)
  last_name   = serializers.CharField(max_length = 50)
  birthdate   = serializers.DateField(allow_null=True, default=None)
  is_employee = serializers.BooleanField(allow_null = True, default=False)
  password    = serializers.CharField(write_only = True)

  is_superuser = serializers.BooleanField(read_only=True, default=False)

  def create(self, validated_data: dict):
    employ = validated_data['is_employee']

    if employ:
      return User.objects.create_superuser(**validated_data)
    else:
      return User.objects.create_user(**validated_data)
  
  def update(self, instance: User, validated_data: dict):
    for key, value in validated_data.items():
        setattr(instance, key, value)
        
    instance.set_password(instance.password)

    instance.save()

    return instance

  def validate_email(self, value):
    email_value = User.objects.filter(email__contains = value).first()

    if email_value: raise serializers.ValidationError("email already registered.")
    
    return value

  def validate_username(self,value):
    username_value = User.objects.filter(username__contains = value).first()

    if username_value: raise serializers.ValidationError("username already taken.")
    
    return value

class LoginSerializer(serializers.Serializer):
  username    = serializers.CharField(write_only = True)
  password    = serializers.CharField(write_only = True)
