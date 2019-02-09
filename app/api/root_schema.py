"""
Graphql Schema definition for api project
"""
import graphene
from graphene_django.debug import DjangoDebug
from ads.schema import AdMutation, AdQuery, CategoryQuery


class RootQuery(AdQuery, CategoryQuery, graphene.ObjectType):
    """
    This class inherit from multiple queries Class of the project
    """
    debug = graphene.Field(DjangoDebug, name='_debug')


class RootMutation(AdMutation, graphene.ObjectType):
    """
    This class inherit from multiple mutation Class of the project
    """
    debug = graphene.Field(DjangoDebug, name='_debug')


SCHEMA = graphene.Schema(query=RootQuery, mutation=RootMutation)
