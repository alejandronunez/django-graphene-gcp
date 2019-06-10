"""
api URL Configuration
"""
from django.conf import urls
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from api import root_schema

urlpatterns = [
    urls.url(r'^dev/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=root_schema.SCHEMA))),
]
