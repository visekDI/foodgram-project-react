from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка Пользователей."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'count_followers',
        'count_recipes',
    )
    readonly_fields = ('count_followers', 'count_recipes')
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    @admin.display(description='Количество подписчиков')
    def count_followers(self, obj):
        """Получаем количество подписчиков."""
        return obj.follower.count()

    @admin.display(description='Количество рецептов')
    def count_recipes(self, obj):
        """Получаем количество подписчиков."""
        return obj.recipes.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
    search_fields = [
        'author__username',
        'author__email',
        'user__username',
        'user__email',
    ]
    list_filter = ['author__username', 'user__username']
    empty_value_display = settings.EMPTY
