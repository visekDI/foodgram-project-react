from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet,
                    SubscribeView, TagViewSet, ShowSubscriptionsView)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('users/<int:id>/subscribe/', SubscribeView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', ShowSubscriptionsView.as_view(),
         name='subscriptions'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
