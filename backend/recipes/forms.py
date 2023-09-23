from django.forms import ModelForm

# # CheckboxSelectMultiple,
#     ModelForms
#     # ModelMultipleChoiceField,
from .models import ImportIngredient


class IngredientImportForm(ModelForm):
    """Форма добавления ингридиентов при импорте."""

    class Meta:
        model = ImportIngredient
        fields = ('csv_file',)


# class RecipeAdminForm(ModelForm):
#     """Форма для админки рецептов"""

#     tags = ModelMultipleChoiceField(
#         queryset=Tag.objects.all(),
#         widget=CheckboxSelectMultiple,
#         required=False,
#         label=("Tags"),
#     )

#     class Meta:
#         model = Recipe
#         fields = ('author', 'name', 'image', 'text', 'cooking_time')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['tags'].required = True
