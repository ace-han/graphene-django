from django.db.models.functions import Length

from django_filters import FilterSet, NumberFilter, OrderingFilter

from cookbook.ingredients.models import Ingredient


class IngredientFilterSet(FilterSet):
    order_by = OrderingFilter(fields=(("name", "-name"),))

    name_len_gt = NumberFilter(method="filter_name_len_gt")

    class Meta:
        model = Ingredient
        fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
            "category": ["exact"],
            "category__name": ["exact"],
        }

    def filter_name_len_gt(self, queryset, name, value):
        # refer to
        # https://stackoverflow.com/questions/12314168/django-filter-on-the-basis-of-text-length/45260608
        queryset = queryset.annotate(text_len=Length("name")).filter(text_len__gt=value)
        return queryset

