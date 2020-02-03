from graphene.relay.node import Node

from graphene_django.types import DjangoObjectType
from cookbook.graphql.core.connection import CountableDjangoObjectType

from cookbook.ingredients.models import Category, Ingredient
from cookbook.ingredients.filtersets import IngredientFilterSet

# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(CountableDjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node,)
        # filter_fields = ["name", "ingredients"]
        # Allow for some more advanced filtering here
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "ingredients": ["exact"],
        }


# class IngredientNode(CountableDjangoObjectType):
class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        interfaces = (Node,)
        # filter_fields = {
        #     "name": ["exact", "icontains", "istartswith"],
        #     "notes": ["exact", "icontains"],
        #     "category": ["exact"],
        #     "category__name": ["exact"],
        # }
        # demo via a filterset_class
        # filterset_class = IngredientFilterSet
