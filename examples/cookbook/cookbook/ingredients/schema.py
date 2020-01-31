from graphene import Argument, Boolean, Field, ID, Node, Mutation, ObjectType, String
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.types import DjangoObjectType

from cookbook.ingredients.forms import CategoryForm
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


# django model form mutation
class CategoryMutation(DjangoModelFormMutation):
    category = Field(CategoryNode)

    class Meta:
        form_class = CategoryForm


# drf model serializer mutation

# bulk

# small combination
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
    category_form_create = CategoryMutation.Field()
    category_form_update = CategoryMutation.Field()
