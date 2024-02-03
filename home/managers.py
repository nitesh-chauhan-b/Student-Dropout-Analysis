# managers.py
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_school_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_school_user', True)
        return self.create_user(username, password, **extra_fields)

    def create_government_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_government_user', True)
        # extra_fields.setdefault('state', state)
        return self.create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)
