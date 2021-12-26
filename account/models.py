import uuid

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.utils.models import Entity


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self,username, name, address1 ,phone_number,  password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.name = name
        user.phone_number = phone_number
        user.address1 = address1
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not username:
            raise ValueError('يجب امتلاك حساب')

        user = self.model(
            username=username
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, Entity):

    username = models.CharField(max_length=255, null=False, unique=True)
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    address1 = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

