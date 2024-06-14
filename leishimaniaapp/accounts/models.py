import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from leishimaniaapp.core.models import BaseModelUuid


class User(AbstractUser, BaseModelUuid):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "username"]

    def __str__(self):
        return self.name
