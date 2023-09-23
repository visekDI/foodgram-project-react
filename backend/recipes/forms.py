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
