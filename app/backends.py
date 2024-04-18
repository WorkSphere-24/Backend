from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("run")
        print(email)
        print(password)
        UserModel = get_user_model()
        print(UserModel)
        try:
            user = UserModel.objects.get(email=email)
            print(user)
            print(user.password)
        except UserModel.DoesNotExist:
            return None
            
        if user.check_password(password):
            return user
        else:
            print("errror")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
