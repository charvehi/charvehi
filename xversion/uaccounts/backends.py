from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import UserProfileInfo


class UserProfileInfoBackend(object):
    def authenticate(self, request, email=None, password=None):

        try:
            # Try to find a user matching your username
            user = UserProfileInfo.objects.get(email=email, password=password)
            #passcode = UserProfileInfo.objects.get(password=password)

            #  Check the password is the reverse of the username
            if user is not None:
                if user.password == password:
                # Yes? return the Django user object
                    user.is_active = True
                    return user
            else:
                # No? return None - triggers default login failed
                return None
        except UserProfileInfo.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return UserProfileInfo.objects.get(email=user_id)
        except UserProfileInfo.DoesNotExist:
            return None




'''class UserProfileInfo(object):
    def authenticate(self, email, password):
        existing_user = User.objects.get(username=email)
        if not existing_user:
            user_data1 = UserProfileInfo.objects.get(email=email)
            #user_data2 = UserProfileInfo.objects.get(password=password)
            print("...%s...." % user_data1)
            if email == user_data1.email:
                return email
            else:
                return None
        else:
            return existing_user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None'''