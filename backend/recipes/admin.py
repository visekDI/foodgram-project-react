import csv

from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from rest_framework.authtoken.models import TokenProxy

from .forms import IngredientImportForm
from .models import (
    Favourite,
    ImportIngredient,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name', 'measurement_unit')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = IngredientImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with open(
                    form_object.csv_file.path, encoding='utf-8'
                ) as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['name', 'measurement_unit']:
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    Ingredient.objects.bulk_create(
                        Ingredient(
                            name=row[0],
                            measurement_unit=row[1],
                        )
                        for row in rows
                    )
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        form = IngredientImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientInRecipe
    min_num = 1
    extra = 3


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка Тегов"""

    model = Tag
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(ImportIngredient)
class ImportIngredient(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    inlines = (IngredientInRecipe,)
    readonly_fields = ('added_in_favorites',)
    search_fields = ('name',)
    list_filter = (
        'author',
        'name',
        'tags',
    )

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .select_related('author')
            .prefetch_related('tags')
            .annotate(favorites_count=Count('favorites'))
        )
        return queryset

    @admin.display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites_count


@admin.register(IngredientInRecipe)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')


@admin.register(Favourite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related('user')
            .prefetch_related(
                'recipe__ingredients',
                'recipe__tags',
            )
        )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related('user')
            .prefetch_related(
                'recipe__ingredients',
                'recipe__tags',
            )
        )


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
