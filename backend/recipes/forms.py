from django.forms import (
    CheckboxSelectMultiple,
    ModelForm,
    ModelMultipleChoiceField,
)

from .models import ImportIngredient, Recipe, Tag


class IngredientImportForm(ModelForm):
    """Форма добавления ингридиентов при импорте."""

    class Meta:
        model = ImportIngredient
        fields = ('csv_file',)


class RecipeAdminForm(ModelForm):
    """Форма для админки рецептов"""

    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label=("Tags"),
    )

    class Meta:
        model = Recipe
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = True
