# -*- coding: utf-8 -*-
"""
Graphql Schema definition for ads App
"""
from __future__ import unicode_literals
from graphene import Field, List, Int
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.types import DjangoObjectType
from ads.models import Ad, Category
from ads.forms import DeleteAdForm, CreateAdForm
from ads.filters import AdFilter


class AdType(DjangoObjectType):
    """
    Ad model Type
    """
    class Meta(object):
        """Meta Class"""
        model = Ad
        use_connection = True
        exclude_fields = ()

    def resolve_email(self, info, **kwargs):
        """Resolve email field"""

        return "This the email:%d" % self.email


ALL_ADS = DjangoFilterConnectionField(AdType, filterset_class=AdFilter, description='List all ads')


class CategoryType(DjangoObjectType):
    """
    Category Model Type
    """
    subcategories = List(lambda: CategoryType, description='Subcategories children of this category')
    ads = ALL_ADS

    class Meta(object):
        """Meta class"""
        model = Category
        use_connection = True
        only_fields = ('name', 'parent_category')

    def resolve_subcategories(self, info):
        """
        Resolve all subcategories of a given category.
        :param info: Schema info
        """
        return self.category_set.all()

    def resolve_ads(self, info, **kwargs):
        """
        Resolve all the ads of a category.
        Note that if the category is a parent category, there is no direct relation between
        the ads and the category in DB. The relation is through de subcategories.
        :param info: Schema info
        :param kwargs: Pagination and filtering args.
        """
        if self.parent_category is None:
            return Ad.objects.filter(subcategory__in=self.category_set.all())
        return self.ad_set.all()


class DeleteAdMutation(DjangoModelFormMutation):
    """
    Remove ad payload with the following fields:

     ad: ad instance.

     errors: errors description.

    """
    ad = Field(AdType)

    class Meta(object):
        """Meta Class"""
        model = Ad
        form_class = DeleteAdForm

    @classmethod
    def perform_mutate(cls, form, info):
        """
        Factory method of this mutation
        :type form: MarkAdForm
        :param form: Django form
        :param info: Schema info
        :return: id of instance
        """
        ad_instance = form.remove()
        return ad_instance.id


class CreateAdMutation(DjangoModelFormMutation):
    """
    Create ad without user
    """

    class Meta(object):
        """Meta Class"""
        model = Ad
        form_class = CreateAdForm

    @classmethod
    def perform_mutate(cls, form, info):
        """
        Factory method of this mutation
        :type form: CreateAdWithoutUserForm
        :param form: CreateAdWithoutUserForm instance
        :param info: Schema info
        :return: instance of this class
        """
        ad_instance = form.save()
        return cls(ad=ad_instance)


class AdMutation(object):
    """
    Root Class of the ads app mutations
    """
    create_ad = CreateAdMutation.Field(description='New ad')


class AdQuery(object):
    """
    Root class of the ads app queries
    """
    ads = ALL_ADS
    ad = Field(AdType, id=Int(required=True), description='Ad detail')

    @classmethod
    def resolve_ad(cls, instance, info, **kwargs):
        """
        Ad query resolution
        """
        return Ad.objects.get(pk=kwargs.get('id'))


class CategoryQuery(object):
    """
    Root class of the category model queries
    """
    categories = List(CategoryType, description='List of categories')
    category = Field(CategoryType, id=Int(required=True), description='A category')

    @classmethod
    def resolve_categories(cls, instance, info):
        """
        Resolve all categories
        :param instance: Query instance
        :param info: Schema info
        :return: All parent categories
        """
        return Category.objects.filter(parent_category=None)

    @classmethod
    def resolve_category(cls, instance, info, **kwargs):
        """
        Resolve single category.
        :param instance: Query instance
        :param info: Schema info
        :return: CategoryType node of Category model.
        """
        return Category.objects.get(pk=kwargs.get('id'))
