#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('builder.views',
    url(r'^/?$', view='create', name="create_form"),
)
