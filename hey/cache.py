from datetime import timedelta

from django.core.cache import cache # default cache
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def user_tz_key(user_id: str) -> str:
    return f'user_{user_id}_tz_offset'

def get_user_tz(user_id: str) -> timezone.timezone:
    """Get user timezone from cache or database.

    This is cached since a lot of Friend data is date-dependent.
    Constantly asking the database for Friend.user.account.timezone
    would generate either a three-part join or several queries
    for *each friend* in friend_list, checkins, etc.
    Caching cuts this down substantially.
    """
    cache_string = user_tz_key(user_id)
    tz = cache.get(cache_string)
    if tz is None: # Check database
        user = User.objects.get(pk=user_id)
        tz = user.account.timezone
        cache.set(cache_string, tz)
    return timezone.get_fixed_timezone(timedelta(hours=tz))

def delete_user_tz(user_id: str) -> None:
    cache_string = user_tz_key(user_id)
    cache.delete(cache_string)
