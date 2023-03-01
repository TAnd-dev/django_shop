from django.db.models import QuerySet

from shop.models import Purchase
from users.models import UserProfile, CustomUser


def get_user_profile(user_id: int) -> UserProfile:
    return UserProfile.objects.get(user__pk=user_id)


def get_user(user_id: int) -> CustomUser:
    return CustomUser.objects.get(pk=user_id)


def get_user_purchases(user_id: int) -> QuerySet:
    return Purchase.objects.filter(user=user_id).all()
