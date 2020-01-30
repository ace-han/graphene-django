import graphene
from cookbook.ingredients.schema import (
    Queries as IngredientQueries,
    Mutations as IngredientMutations,
)
from cookbook.recipes.schema import (
    Queries as RecipeQueries,
    Mutations as RecipeMutations,
)

from graphene_django.debug import DjangoDebug


class Query(
    IngredientQueries, RecipeQueries, graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    IngredientMutations, graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
