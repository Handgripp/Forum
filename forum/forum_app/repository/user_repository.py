from django.utils import timezone
from django.contrib.auth import get_user_model


class UserRepository:

    @staticmethod
    def get_all():
        User = get_user_model()
        return User.objects.all()

    @staticmethod
    def create(username, email, password):
        User = get_user_model()
        user = User.objects.create_user(username=username, email=email, password=password)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return user
