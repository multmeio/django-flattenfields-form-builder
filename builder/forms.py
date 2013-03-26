#!/usr/bin/env python
# encoding: utf-8

from django.forms import *
from hstore_flattenfields.forms import HStoreModelForm

from models import *

SAMPLE_CHOICES = [(x, x) for x in xrange(0, 5)]

class TextFieldsForm(Form):
    text = CharField(
        label=u"Campo Texto"
    )
    integer = IntegerField(
        label=u"Campo Numérico"
    )
    decimal = DecimalField(
        label=u"Campo Decimal",
        help_text=u"Com duas (2) casas decimais"
    )
    date = DateField(
        widget=DateInput(
            format='%d/%m/%Y',
        ),
        label=u"Data",
        help_text=u"formato: (dd/mm/aaaa)"
    )
    datetime = CharField(
        widget=DateTimeInput(
            format='%d/%m/%Y %H:%M:%S'
        ),
        label=u"Tempo",
        help_text=u"formato: (dd/mm/aaaa hh:mm:ss)"
    )
    textarea = CharField(
        widget=Textarea(),
        label=u"Caixa de Texto",
    )

    def __init__(self, *args, **kwargs):
        super(TextFieldsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'data-typeconfig': 'text_fields_configs'
            })


class MultipleChoiceFieldsForm(Form):
    select_multiple = CharField(
        widget=SelectMultiple(
            choices=SAMPLE_CHOICES
        ),
        label=u"Multi-seleções",
    )
    checkbox = ChoiceField(
        widget=CheckboxSelectMultiple(),
        label=u"Multi-seleções",
        choices=SAMPLE_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super(MultipleChoiceFieldsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'data-typeconfig': 'multiple_choice_fields_configs'
            })


class SingleChoiceFieldsForm(Form):
    select = CharField(
        widget=Select(
            choices=SAMPLE_CHOICES
        ),
        label=u"Única Seleção"
    )
    radio = ChoiceField(
        widget=RadioSelect(),
        choices=SAMPLE_CHOICES,
        label=u"Única Seleção"
    )

    def __init__(self, *args, **kwargs):
        super(SingleChoiceFieldsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'data-typeconfig': 'single_choice_fields_configs'
            })


class TextFieldsConfigsForm(ModelForm):
    class Meta:
        model = CustomDynamicField
        exclude = ['choices']


class MultipleChoiceFieldsConfigsForm(ModelForm):
    class Meta:
        model = CustomDynamicField


class SingleChoiceFieldsConfigsForm(ModelForm):
    class Meta:
        model = CustomDynamicField
