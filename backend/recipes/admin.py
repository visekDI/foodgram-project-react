import csv

from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import TokenProxy

from .forms import IngredientImportForm, RecipeAdminForm
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
    list_editable = ('color',)
    empty_value_display = '-пусто-'


@admin.register(ImportIngredient)
class ImportIngredient(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = (
        'id',
        'author',
        'name',
        'get_ingredients',
        'get_tags',
        'in_favorites',
        'get_image',
    )
    fields = (
        'name',
        'author',
        'text',
        'image',
        'tags',
        'cooking_time',
    )
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngredientInline,)
    empty_value_display = '- пусто -'
    filter_horizontal = ("tags",)

    @admin.display(description='Изображение')
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorites.count()

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        ingredients_list = []
        for ingredient in obj.ingredients.all():
            ingredients_list.append(ingredient.name.lower())
        return ', '.join(ingredients_list)

    @admin.display(description='Теги')
    def get_tags(self, obj):
        ls = [_.name for _ in obj.tags.all()]
        return ', '.join(ls)


@admin.register(IngredientInRecipe)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(Favourite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
