from django.db import models

from bleach import clean

from . import forms
from .utils import get_bleach_default_options


class BleachField(models.TextField):
    def __init__(self, allowed_tags=None, allowed_attributes=None,
                 allowed_styles=None, allowed_protocols=None,
                 strip_tags=None, strip_comments=None, *args, **kwargs):

        super(BleachField, self).__init__(*args, **kwargs)

        self.bleach_kwargs = get_bleach_default_options()

        if allowed_tags:
            self.bleach_kwargs["tags"] = allowed_tags
        if allowed_attributes:
            self.bleach_kwargs["attributes"] = allowed_attributes
        if allowed_styles:
            self.bleach_kwargs["styles"] = allowed_styles
        if allowed_protocols:
            self.bleach_kwargs["protocols"] = allowed_protocols
        if strip_tags:
            self.bleach_kwargs["strip"] = strip_tags
        if strip_comments:
            self.bleach_kwargs["strip_comments"] = strip_comments

    def formfield(self, **kwargs):
        """
            Makes field for ModelForm
        """

        # If field doesn't have any choice return BleachField
        if not self.choices:
            return forms.BleachField(
                label=self.verbose_name,
                max_length=self.max_length,
                allowed_tags=self.bleach_kwargs.get("tags"),
                allowed_attributes=self.bleach_kwargs.get("attributes"),
                allowed_styles=self.bleach_kwargs.get("styles"),
                allowed_protocols=self.bleach_kwargs.get("protocols"),
                strip_tags=self.bleach_kwargs.get("strip"),
                strip_comments=self.bleach_kwargs.get("strip_comments"),
            )

        return super(BleachField, self).formfield(**kwargs)

    def pre_save(self, model_instance, add):
        data = getattr(model_instance, self.attname)
        if data:
            clean_value = clean(
                data,
                **self.bleach_kwargs
            )
            setattr(model_instance, self.attname, clean_value)
            return clean_value
        return data
