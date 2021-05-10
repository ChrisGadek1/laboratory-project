from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None, must_change_password=True):
        if not username:
            raise ValueError("Users must have an username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have an last name ")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            must_change_password=must_change_password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password, must_change_password=False):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            must_change_password=must_change_password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='Data stworzenia konta', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Ostatnie logowanie", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    object = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        values = self.get_all_permissions()
        if perm in values:
            return True

        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.has_perm(perm=app_label):
            return True
        return False
