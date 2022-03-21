from django import template
from forum.models import MessageRating

register = template.Library()


@register.simple_tag
def check_user_message_rating_existance(message, user):
    try:
        if MessageRating.objects.filter(message=message).filter(user=user).exists():
            return True
    except:
        return False


@register.simple_tag
def get_user_message_rating_type(message, user):
    return MessageRating.objects.filter(message=message).get(user=user).value
