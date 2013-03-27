#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('builder.views',
    url(regex=r'^/?$',
        view='choose_entity',
        name="choose_entity_view"
    ),
    url(regex=r'^create/(?P<entity>[ A-Za-z\d]+)/?$',
        view='create',
        name="create_view"
    ),
)
