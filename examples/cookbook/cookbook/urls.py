from django.conf.urls import url
from django.contrib import admin

from graphene_django.views import GraphQLView

from django.http import HttpResponse


def index(request):
    print("hahaha")
    return HttpResponse("ok")


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^index/", index),
    url(r"^graphql$", GraphQLView.as_view(graphiql=True)),
]
