from graphene import Node, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from cookbook.ingredients.filtersets import IngredientFilterSet
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
    """
    standard scalar filter
    query {
        allIngredients(name_Icontains: "g", first: 3, orderBy: "-name") {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
    """
    """
    custom scalar filter
    query {
        allIngredients(
            name_Icontains: "g", 
            nameLenGt: 4,
            first: 3, 
            orderBy: "-name") {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }

    """
    all_ingredients = DjangoFilterConnectionField(
        IngredientNode, filterset_class=IngredientFilterSet
    )


class Mutations(ObjectType):
    """
        it seems that using pure graphene-django other than 
        `django form` and `djangorestframework serializer` is more flexible
    """

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
    not like the 
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

    """
    query part
    mutation yyy ($ingredients: [IngredientMutationInput!]) {
        ingredientBulkUpdate (ingredients: $ingredients) {
            ingredients {
                id
                name
                notes
                category {
                    id
                    name
                }
            }
        }
        ingredientAtomicBulkUpdate (ingredients: $ingredients) {
            ingredients {
                id
                name
                notes
                category {
                    id
                    name
                }
            }
        }
    }

    variables part
    {
    "ingredients": [
        {
            "id": "SW5ncmVkaWVudE5vZGU6NQ==",
            "name": "Salt1",
            "notes": "Salt1 notes",
            "categoryId": 3
        },
        {
            "id": "SW5ncmVkaWVudE5vZGU6Ng==",
            "name": "Sugar1",
            "notes": "Sugar1 notes",
            "categoryId": "Q2F0ZWdvcnlOb2RlOjM="
        }
    ]
    }
    """
    ingredient_bulk_update = BulkIngredientUpdate.Field()
    ingredient_atomic_bulk_update = AtomicBulkIngredientUpdate.Field()

