from django.db.models import Count, Exists, OuterRef, Sum
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (
    Favourite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    User,
)
from users.models import Subscription

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    FavoritSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    ShowSubscriptionsSerializer,
    SubscriptionSerializer,
    TagSerializer,
)
from .utils import create_shopping_list_buffer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @staticmethod
    def adding_author(add_serializer, model, request, author_id):
        """Кастомный метод добавления author и получения данных."""
        user = request.user
        data = {'user': user.id, 'author': author_id}
        serializer = add_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.to_representation(serializer.instance),
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False, methods=['get'], permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(author__user=request.user).annotate(
            recipes_count=Count('subscriptions')
        )
        serialized_data = ShowSubscriptionsSerializer(
            self.paginate_queryset(queryset),
            many=True,
            context={'request': request},
        ).data

        return self.get_paginated_response(serialized_data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        return self.adding_author(
            SubscriptionSerializer, Subscription, request, id
        )

    @subscribe.mapping.delete
    def delete_favorite(self, request, id):
        queryset = Subscription.objects.filter(user=request.user, author=id)
        queryset.delete()
        return response.Response(
            {'detail': 'Успешная отписка'},
            status=status.HTTP_204_NO_CONTENT,
        )


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )
        queryset = queryset.annotate(
            favorited=Exists(
                Favourite.objects.filter(user=user, recipe=OuterRef('pk'))
            ),
            in_shopping_cart=Exists(
                ShoppingCart.objects.filter(user=user, recipe=OuterRef('pk'))
            ),
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @staticmethod
    def add_to(add_serializer, model, request, recipe_id):
        user = request.user
        data = {'user': user.id, 'recipe': recipe_id}
        serializer = add_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self.add_to(FavoritSerializer, Favourite, request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        queryset = Favourite.objects.filter(user=request.user, recipe=pk)
        queryset.delete()
        return response.Response(
            {'detail': 'Рецепт успешно удалён из избранного!'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return self.add_to(ShoppingCartSerializer, ShoppingCart, request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        queryset = ShoppingCart.objects.filter(user=request.user, recipe=pk)
        queryset.delete()
        return response.Response(
            {'detail': 'Рецепт успешно удалён из корзины!'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )

        today = timezone.now()

        shopping_list_buffer = create_shopping_list_buffer(
            ingredients,
            today.strftime('%Y-%m-%d'),
            today.strftime('%Y'),
            user.get_full_name(),
        )

        filename = f'{user.username}_shopping_list.txt'

        response = HttpResponse(
            shopping_list_buffer.read(),
            content_type='text/plain;charset=UTF-8',
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
