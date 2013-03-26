#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from hstore_flattenfields import models as hs_models

class Category(models.Model):
    name = models.CharField(
        max_length=80,
        null=False,
        verbose_name='Nome'
    )


class CustomDynamicField(hs_models.DynamicField):
    category = models.ForeignKey(Category,
        null=True,
        blank=True,
        related_name='dynamic_fields',
        verbose_name=u'Categoria'
    )


class Product(hs_models.HStoreModel):
    hstore_related_field = 'category'
