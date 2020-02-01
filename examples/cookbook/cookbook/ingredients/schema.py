from graphene import Node, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from cookbook.ingredients.mutations import (
    CategoryCreate,
    CategoryFormMutation,
    IngredientSerializerMutation,
    BulkIngredientUpdate,
    AtomicBulkIngredientUpdate,
)
from cookbook.ingredients.types import CategoryNode, IngredientNode


# from graphene_django.rest_framework.mutation import SerializerMutation
class Queries(ObjectType):
    # without id resolver
    # category = Field(CategoryNode)
    # without `graphene.relay.node#Node.node_resolver`
    # category = Field(
    #     CategoryNode,
    #     id=Argument(ID, required=True, description="ID of the category."),
    #     description="Look up a category by ID.",
    # )
    category = Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class Mutations(ObjectType):
    category_create = CategoryCreate.Field()
    """
    query part
    mutation xxx ($formInput: CategoryMutationInput!){
        categoryCreate(name: "Frozen") {
            created
            category {
                id
                name
            }
        }
        categoryFormCreate(input: $formInput) {
            category {
                id
                name
            }
        }
    }
    variables part
    {
        "formInput":{
        "name": "Staple"
        }  
    }
    """
    category_form_create = CategoryFormMutation.Field()
    """
    query part
    mutation xxx($formInput: CategoryFormMutationInput!) {
        categoryFormUpdate (input: $formInput){
            category {
                id
                name
            }
        }
    }
    variables part
    {
        "formInput": {
            // pk not global_id
            // refer to
            // https://github.com/graphql-python/graphene-django/issues/867
            // https://github.com/graphql-python/graphene-django/issues/728
            "id": 5, 
            "name": "Staple"
        }
    }
    """
    category_form_update = CategoryFormMutation.Field()
    """
    query part 
    mutation yyy ($input1: IngredientSerializerMutationInput!) {
        ingredientSerializerCreate (input: $input1){
            id
            name
            notes
            category
            categoryObj {   // `xxxObj` for a nested detail
                id
                name
            }
        }
    }
    variables part
    {
        "input1":{
            "name": "Sugar",
            "notes": "Sugar notes",
            "category": "3" // String type!!!
        }
    }
    """
    ingredient_serializer_create = IngredientSerializerMutation.Field()
    ingredient_serializer_update = IngredientSerializerMutation.Field()
    ingredient_bulk_update = BulkIngredientUpdate.Field()
    ingredient_atomic_bulk_update = AtomicBulkIngredientUpdate.Field()

