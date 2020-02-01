from graphene import Boolean, Field, Mutation, String
from graphene_django.forms.mutation import DjangoModelFormMutation

from cookbook.ingredients.forms import CategoryForm
from cookbook.ingredients.models import Category
from cookbook.ingredients.types import CategoryNode


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
class CategoryFormMutation(DjangoModelFormMutation):
    """
    DjangoModelFormMutation supports no DELETE mutation,
    so we will have to do a delete mutation manually
    """

    category = Field(CategoryNode)

    class Meta:
        form_class = CategoryForm


# drf model serializer mutation
# class CategorySerializerMutation(SerializerMutation):
#     pass


# bulk