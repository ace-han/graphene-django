from django.forms.models import ALL_FIELDS, ModelForm
from cookbook.ingredients.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ALL_FIELDS
