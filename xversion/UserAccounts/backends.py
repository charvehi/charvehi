from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User

import logging

from django.db.models import Q


User = get_user_model()

class EmailPhoneBackend(object):

    def authenticate(self, request,username=None, password=None, **kwargs):
        User = get_user_model()
        print("something")
        try:

            user = User.objects.get(Q(email=username)|Q(phone=username))
            print(user)

            print("running")
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists" % login)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None