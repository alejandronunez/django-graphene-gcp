# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_mysql.models import EnumField
from djchoices import DjangoChoices, ChoiceItem


class Category(models.Model):
    """Ad's categories model. Each ad belongs to a category"""

    name = models.CharField(max_length=20, help_text='Category name')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, unique=False, null=True,
                                        help_text='Parent Category')

    def __unicode__(self):  # pragma: no cover
        return self.name


class Ad(models.Model):
    """
    Model to handle ads
    """

    class StatusChoices(DjangoChoices):
        """
        State for ads
        """
        published = ChoiceItem('PUBLISHED', 'Ad expired')
        removed = ChoiceItem('REMOVED', 'Ad removed')

    title = models.CharField(max_length=123, help_text='Title')
    description = models.CharField(max_length=500, blank=True, null=True, help_text='Description')
    price = models.IntegerField(null=True, blank=True, help_text='Price')
    name = models.CharField(max_length=64, null=True, blank=True, help_text='Owner name')
    email = models.EmailField(null=True, blank=True, help_text='Email')
    phone = models.CharField(max_length=12, blank=True, null=True, help_text='Phone')
    created_on = models.DateTimeField(auto_now_add=True, help_text='Create')
    updated_on = models.DateTimeField(auto_now=True, help_text='Update')
    status = EnumField(choices=StatusChoices.choices, default=StatusChoices.published, help_text='Ad status')
    subcategory = models.ForeignKey(Category, help_text='Category')
