from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager, MessageRatingManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(null=True, default=None)
    bio = models.TextField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    objects = UserManager()


class Topic(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='host', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField()

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.name


class Message(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:100]


class MessageRating(models.Model):
    LIKE = 'Like'
    DISLIKE = 'Dislike'
    CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_author')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_author')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    value = models.CharField(choices=CHOICES,
                             default='Like', max_length=50)

    objects = MessageRatingManager()

    def __str__(self):
        return str(self.value)
