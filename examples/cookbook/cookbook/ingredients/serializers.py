from rest_framework.serializers import ModelSerializer, ALL_FIELDS

from cookbook.ingredients.models import Ingredient, Category
from rest_framework.fields import SerializerMethodField


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ALL_FIELDS


class IngredientSerializer(ModelSerializer):
    """
    for SerializerMutation
    """

    # category = ModelField()
    category_obj = CategorySerializer(read_only=True, source="category")

    # category_detail = SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ALL_FIELDS

    def get_category_detail(self, instance):
        """
            this won't work for the time being since 
            `graphene_django.rest_framework.mutation.py#SerializerMutation.perform_mutate`
            SerializerMethodField.get_attribute(obj) return obj itself
            can't get result from `serializer.get_xxx(obj)` 
        """
        category = getattr(instance, "category", None)
        if not category:
            return None
        ser = CategorySerializer(instance.category)
        return ser.data

