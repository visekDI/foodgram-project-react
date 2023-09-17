import csv

from django.contrib import admin, messages
from django.contrib.admin import display
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

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


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    readonly_fields = ('added_in_favorites',)
    list_filter = (
        'author',
        'name',
        'tags',
    )

    def get_queryset(self, request):
        return (
            Recipe.objects.select_related('author')
            .prefetch_related(
                'ingredients',
                'tags',
            )
            .annotate(favorites_count=Count('favorites'))
        )

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    model = Ingredient
    list_display = ('pk', 'name', 'measurement_unit')
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = ('recipe',)


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = ('recipe',)


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(ImportIngredient)
class ImportIngredient(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')
