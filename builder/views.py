#!/usr/bin/env python
# encoding: utf-8

from django.template import RequestContext
from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    redirect
)

from forms import *

def choose_entity(request):
    choose_entity_form = ChooseEntityForm(request.POST or None)

    if choose_entity_form.is_valid():
        entity = choose_entity_form.cleaned_data['entity']
        return redirect('create_view', entity=entity)

    data = {
        'choose_entity_form': choose_entity_form
    }
    return render_to_response('choose_entity.html', data,
        context_instance=RequestContext(request))

def create(request, entity):
    initial_entity = {
        'refer': entity
    }
    data = {
        'text_fields_form': TextFieldsForm(),
        'multiple_choice_fields_form': MultipleChoiceFieldsForm(),
        'single_choice_fields_form': SingleChoiceFieldsForm(),
        'text_fields_configs_form': TextFieldsConfigsForm(initial=initial_entity),
        'multiple_choice_fields_configs_form': MultipleChoiceFieldsConfigsForm(initial=initial_entity),
        'single_choice_fields_configs_form': SingleChoiceFieldsConfigsForm(initial=initial_entity),
    }
    return render_to_response('create.html', data,
        context_instance=RequestContext(request))
