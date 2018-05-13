
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,Group,PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_admin=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        print('email=%s,name=%s' % (email, name))
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.is_admin = is_admin
        print(user.is_admin)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, name=name, is_admin=True)
        # user.is_admin = True
        # user.save(using=self._db)
        return user

