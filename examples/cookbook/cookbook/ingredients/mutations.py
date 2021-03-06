from django.db.transaction import atomic
from graphene import Boolean, Field, ID, Int, List, Mutation, NonNull, String
from graphene.relay.node import Node
from graphene.types.inputobjecttype import InputObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.rest_framework.mutation import SerializerMutation

from cookbook.ingredients.forms import CategoryForm
from cookbook.ingredients.models import Category, Ingredient
from cookbook.ingredients.serializers import IngredientSerializer
from cookbook.ingredients.types import CategoryNode, IngredientNode


class IngredientMutationInput(InputObjectType):
    id = ID()
    #     name = String(required=True)
    # no more required for partial update
    name = String()
    notes = String()
    # validation in `graphql.type.GraphQLID.parse_value->(coerce_string)`
    # category_id = ID()
    # validation in `graphql.type.GraphQLInt.parse_value->(coerce_int)`
    category_id = Int()


# simple mutation
class CategoryCreate(Mutation):
    """
    mutation {
        categoryCreate(name: "Condiment") {
            created
            category {
                id
                name
            }
        },
        _debug {
            sql {
                rawSql,
                sql,
                vendor
            }
        }
    }   
    """

    # The class attributes define the response of the mutation
    created = Boolean()
    category = Field(CategoryNode)

    class Arguments:
        # The input arguments for this mutation
        name = String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        # some discussion not resolved at the time of writing
        # refer to
        # https://docs.graphene-python.org/en/latest/types/objecttypes/#resolver-parameters
        # https://github.com/graphql-python/graphene/issues/810
        # stick with classmethod for the time being
        name = kwargs.get("name", "")
        obj, created = Category.objects.get_or_create(name=name)
        return cls(created=created, category=obj)


class BulkIngredientUpdate(Mutation):
    class Input:
        # [IngredientMutationInput]!
        # ingredients = List(IngredientMutationInput, required=True)
        # [IngredientMutationInput!]
        ingredients = List(NonNull(IngredientMutationInput))

    ingredients = List(IngredientNode)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        ingredients = kwargs.get("ingredients")
        ids = []
        for ingredient_dict in ingredients:
            _, pk = Node.from_global_id(ingredient_dict.pop("id", "_:missing"))
            Ingredient.objects.filter(id=pk).update(**ingredient_dict)
            ids.append(pk)
        qs = Ingredient.objects.filter(id__in=ids)
        return cls(ingredients=qs)


class AtomicBulkIngredientUpdate(Mutation):
    class Input:
        # [IngredientMutationInput]!
        # ingredients = List(IngredientMutationInput, required=True)
        # [IngredientMutationInput!]
        ingredients = List(NonNull(IngredientMutationInput))

    ingredients = List(IngredientNode)

    # @classmethod
    # def mutate(cls, root, info, **kwargs):
    #     ingredients = kwargs.get("ingredients")
    #     objs = []
    #     pks = []
    #     fields = ("name", "category_id")
    #     for ingredient_dict in ingredients:
    #         _, pk = Node.from_global_id(ingredient_dict.pop("id", "_:missing"))
    #         obj = Ingredient.objects.get(id=pk)
    #         for field, value in ingredient_dict.items():
    #             setattr(obj, field, value)
    #         objs.append(obj)
    #         pks.append(pk)
    #     Ingredient.objects.bulk_update(objs, fields)
    #     result = Ingredient.objects.filter(id__in=pks)
    #     return cls(ingredients=result)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        ingredients = kwargs.get("ingredients")
        ids = []
        # transaction for the time being
        # refer to
        # https://github.com/graphql-python/graphene-django/issues/835
        with atomic():
            for ingredient_dict in ingredients:
                _, pk = Node.from_global_id(ingredient_dict.pop("id", "_:missing"))
                Ingredient.objects.filter(id=pk).update(**ingredient_dict)
                ids.append(pk)
        qs = Ingredient.objects.filter(id__in=ids)
        return cls(ingredients=qs)


# django model form mutation
class CategoryFormMutation(DjangoModelFormMutation):
    """
    DjangoModelFormMutation supports no DELETE mutation,
    so we will have to do a delete mutation manually
    """

    class Meta:
        form_class = CategoryForm

    # @classmethod
    # def get_form_kwargs(cls, root, info, **input):
    #     # by now `input` is sth like
    #     # {
    #     #   "id": "5", # str
    #     #   "name": "Staple 1",
    #     # }
    #     # not sth like
    #     # {
    #     #   "id": 5, # int!!!
    #     #   "name": "Staple 1",
    #     # }
    #     # this kind of transformation is done by FormClass
    #     kwargs = {"data": input}

    #     pk = input.pop("id", None)
    #     if pk:
    #         instance = cls._meta.model._default_manager.get(pk=pk)
    #         kwargs["instance"] = instance

    #     return kwargs


# drf model serializer mutation
class IngredientSerializerMutation(SerializerMutation):
    class Meta:
        # model_operations = ["create", "update"]
        serializer_class = IngredientSerializer


"""
bulk mutation below forms
1. multi-fields in one request 
    (server side execute_fields_serially (one by one),
        errors affect independently)
2. single-field, array-inputs in one request 
    (client side extra codes, server side not atomic. 
        Or need a extra batch=True in GraphQlView)
3. atomic single-field, array-inputs in one request 
    (client and server need extra codes)
"""

"""
1. multi-fields in one request

query part
mutation xxx($formInput: CategoryFormMutationInput!, $formInput1: CategoryFormMutationInput!) {
	a: categoryFormUpdate (input: $formInput){
		category {
            id
            name
        }
	}
  b: categoryFormUpdate (input: $formInput1){
		category {
            id
            name
        }
	}
}
variables part
{
  "formInput": {
    "id": 5, // pk
    "name": "Staple 3"
  },
  "formInput1": {
    "id": "Q2F0ZWdvcnlOb2RlOjQ=", // global id (it will fail for the time being)
    "name": "Frozen 1"
  }
}
"""

"""
2. single-field, array-inputs in one request
3. atomic single-field, array-inputs in one request
client requests are the same, need server side do the transaction control

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

