#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns('builder.views',
    url(regex=r'^/?$',
        view='choose_entity',
        name="choose_entity_view"
    ),
    url(regex=r'^create/(?P<entity>[ A-Za-z\d]+)/fields/?$',
        view='create',
        name="create_view"
    ),

    url(regex=r'^create/dynamic/field/?$',
        view='create_dynamic_field',
        name="create_dynamic_field"
    ),
	url(regex=r'^update/dynamic/field/(?P<dfield_name>[A-Za-z\d]+)/?$',
        view='update_dynamic_field',
        name="update_dynamic_field"
    ),
    url(regex=r'^get/dynamic/field/(?P<dfield_name>[A-Za-z\d]+)/?$',
        view='get_dynamic_field',
        name="get_dynamic_field"
    ),
	url(regex=r'^delete/dynamic/field/(?P<dfield_name>[A-Za-z\d]+)/?$',
        view='delete_dynamic_field',
        name="delete_dynamic_field"
    ),
)
