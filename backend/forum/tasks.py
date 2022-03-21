import redis
import json
from celery import shared_task

from .models import Message, User

client = redis.Redis(host='redis', port=6379, db=0)


@shared_task
def get_top_liked_messages():
    """
    Get messages ordered by like count
    """
    messages = Message.objects.all()
    top_rated = {}
    for message in messages:
        like_count = message.messagerating_set.filter(value='Like').count()
        top_rated[message.body] = like_count
    client.set('best_messages',
               json.dumps({k: v for k, v in sorted(top_rated.items(), key=lambda item: item[1], reverse=True)}))
    return 'Success'


@shared_task
def get_top_disliked_messages():
    """
    Get messages ordered by dislike count
    """
    messages = Message.objects.all()
    top_rated = {}
    for message in messages:
        like_count = message.messagerating_set.filter(value='Dislike').count()
        top_rated[message.body] = like_count
    client.set('worst_messages',
               json.dumps({k: v for k, v in sorted(top_rated.items(), key=lambda item: item[1], reverse=True)}))
    return 'Success'


@shared_task
def get_users_with_best_score():
    """
    Get users ordered by score calculated by formula
    likes_count * 2 - dislike_count * 3
    """
    users = User.objects.all()
    top_rated = {}
    for user in users:
        points = user.message_author.filter(value='Like').count() * 2 - user.message_author.filter(
            value='Dislike').count() * 3
        top_rated[user.name] = points
    client.set('users_scoring',
               json.dumps({k: v for k, v in sorted(top_rated.items(), key=lambda item: item[1], reverse=True)}))
    return 'Success'
