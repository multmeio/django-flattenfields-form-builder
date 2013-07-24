#!/usr/bin/env python
# encoding: utf-8

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson as json
from django.core.serializers.python import Serializer
from django.db.models.fields import FieldDoesNotExist
from StringIO import StringIO

from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    redirect
)

from simplejson import dumps
def write(obj, **kw):
    return dumps(obj, encoding='utf-8', **kw)

from forms import *
from models import *


class InheritanceSerializer(Serializer):
    """
    Supports serialization of fields on the model that are inherited (ie. non-local fields).
    """

    # Copied from django.core.serializers.base
    # Unfortunately, django's serializer only serializes local fields
    def serialize(self, queryset, fields=None, **options):
        """
        Serialize a queryset.
        """
        self.options = options

        self.stream = options.pop("stream", StringIO())
        self.selected_fields = fields or queryset.model._meta.get_all_field_names()
        self.use_natural_keys = options.pop("use_natural_keys", False)

        self.start_serialization()

        for obj in queryset:
            self.start_object(obj)
            for field_name in self.selected_fields:
                try:
                    field = obj._meta.get_field(field_name)
                except FieldDoesNotExist:
                    continue

                if field in obj._meta.many_to_many:
                    self.handle_m2m_field(obj, field)
                elif field.rel is not None:
                    self.handle_fk_field(obj, field)
                else:
                    self.handle_field(obj, field)
            self.end_object(obj)

        self.end_serialization()
        return self.getvalue()

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
        'refer': entity,
        'dynamic_fields': DynamicFieldFormSet(),
        'text_fields_form': TextFieldsForm(),
        'multiple_choice_fields_form': MultipleChoiceFieldsForm(),
        'single_choice_fields_form': SingleChoiceFieldsForm(),
        'text_fields_configs_form': TextFieldsConfigsForm(initial=initial_entity),
        'multiple_choice_fields_configs_form': MultipleChoiceFieldsConfigsForm(initial=initial_entity),
        'single_choice_fields_configs_form': SingleChoiceFieldsConfigsForm(initial=initial_entity),
    }
    return render_to_response('create.html', data,
        context_instance=RequestContext(request))

def _parse_serialize(queryset):
    serialized = [
        x['fields'] 
        for x in InheritanceSerializer().serialize(
            queryset
        )
    ]
    for x in serialized:
        x['pk'] = x['id']
        for typeconfig in TYPECONFIG_MAP.iteritems():
            if x['typo'] in typeconfig[1]:
                x['typeconfig'] = typeconfig[0]
    return serialized

def create_dynamic_field(request):
    dynamic_field_form = CustomDynamicFieldForm(
        request.POST or None
    )
    if dynamic_field_form.is_valid():
        dynamic_field = dynamic_field_form.save()
        return redirect('create_view', dynamic_field.refer)
    return HttpResponseRedirect(redirect_to=request.path)

def get_dynamic_field(request, dfield_name):
    try:
        data = _parse_serialize(
            CustomDynamicField.objects.filter(name=dfield_name)
        )[0]
    except:
        data = {}
    return HttpResponse(
        json.dumps(data), 
        mimetype="application/json"
    )

def update_dynamic_field(request, dfield_name):
    try:
        dynamic_field = CustomDynamicField.objects.get(
            name=dfield_name
        )
    except CustomDynamicField.DoesNotExist:
        pass
    else:
        dynamic_field_form = CustomDynamicFieldForm(
            data=request.POST or None,
            instance=dynamic_field
        )
        if dynamic_field_form.is_valid():
            dynamic_field_form.save()
            return redirect('create_view', dynamic_field.refer)
    return HttpResponseRedirect(redirect_to=request.path)

def delete_dynamic_field(request, dfield_name):
    try:
        dynamic_field = CustomDynamicField.objects.get(
            name=dfield_name
        )
        dynamic_field.delete()
        return HttpResponse(json.dumps({}), mimetype="application/json")
    except:
        return HttpResponseRedirect(redirect_to=request.path)
    