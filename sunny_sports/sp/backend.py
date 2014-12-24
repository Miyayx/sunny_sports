# import the User object
from models.models import MyUser
from django.contrib.auth.models import check_password

class MyBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        print username,password

        try:
            # Try to find a user matching your username
            user = (MyUser.objects.filter(phone=username) | MyUser.objects.filter(nickname=username) | MyUser.objects.filter(email=username) )[0]

            #  Check the password is the reverse of the username
            pwd_valid = user.check_password(password)
            if pwd_valid:
                # Yes? return the Django user object
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except MyUser.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None
