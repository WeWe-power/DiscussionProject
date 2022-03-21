from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')

        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username.lower(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class MessageRatingQueryset(models.QuerySet):
    def get_likes(self):
        return self.filter(value__in=['Like', ])

    def get_dislikes(self):
        return self.filter(value__in=['Dislike', ])


class MessageRatingManager(models.Manager):

    def get_queryset(self):
        return MessageRatingQueryset(self.model, using=self._db)

    def count_likes(self):
        return self.get_queryset().get_likes().count()

    def count_dislikes(self):
        return self.get_queryset().get_dislikes().count()

    def check_user_rate_exist(self, user):
        """
        Checks if user liked or disliked  message
        """
        return self.get_queryset().get_likes().filter(user=user) and self.get_queryset().get_dislikes().filter(
            user=user)
