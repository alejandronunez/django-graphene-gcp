"""
Form to ads schema
"""
from __future__ import unicode_literals

from django import forms
from ads.models import Ad


class CreateAdForm(forms.ModelForm):
    """
    Form to create ad
    """

    class Meta(object):
        """Meta class"""
        model = Ad
        fields = ('title', 'description', 'subcategory', 'price', 'name', 'email', 'phone')


class DeleteAdForm(forms.ModelForm):
    """Form to mark an ad as sold"""

    class Meta(object):
        """Meta class"""
        model = Ad
        fields = ()

    def save(self, commit=True):
        """Remove ad"""
        super(DeleteAdForm, self).save(commit)
