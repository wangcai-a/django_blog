from django import template
from likes.models import Likes, LikeRecord
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def get_likes_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    count = Likes.objects.filter(content_type=ct, object_id=obj.pk).count()
    return count


@register.simple_tag(takes_context=True)
def get_likes_status(context, obj):
    ct = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=ct, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''