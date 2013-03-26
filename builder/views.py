#!/usr/bin/env python
# encoding: utf-8

from django.template import RequestContext
from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    redirect
)

from forms import *

def create(request):
    data = {
        'text_fields_form': TextFieldsForm(),
        'multiple_choice_fields_form': MultipleChoiceFieldsForm(),
        'single_choice_fields_form': SingleChoiceFieldsForm(),
        'text_fields_configs_form': TextFieldsConfigsForm(),
        'multiple_choice_fields_configs_form': MultipleChoiceFieldsConfigsForm(),
        'single_choice_fields_configs_form': SingleChoiceFieldsConfigsForm(),
    }
    return render_to_response('create.html', data,
        context_instance=RequestContext(request))
