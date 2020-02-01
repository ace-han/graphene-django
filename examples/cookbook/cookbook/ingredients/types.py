from graphene.relay.node import Node
from graphene_django.types import DjangoObjectType

from cookbook.ingredients.models import Category, Ingredient

# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node,)
        filter_fields = ["name", "ingredients"]


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        interfaces = (Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
            "category": ["exact"],
            "category__name": ["exact"],
        }