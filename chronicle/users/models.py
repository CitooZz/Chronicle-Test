from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(DefaultUserManager):
    """Custom User Manager."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User, automatically fills 'username' as email
        """
        return super(UserManager, self).create_user(
            email=email, username=email, password=password, **extra_fields
        )


class AllUserManager(DefaultUserManager):
    pass


class GenderChoice(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"


class User(AbstractUser):
    """Custom User Model."""

    first_name = models.CharField(_("first name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=6, choices=GenderChoice.choices)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200, blank=True)

    is_deleted = models.BooleanField(default=False)

    objects = UserManager()
    all_objects = AllUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_deleted:
            return

        self.is_deleted = True
        self.save()
