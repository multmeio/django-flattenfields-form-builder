#!/usr/bin/env python
# encoding: utf-8

from django.forms import *
from django.contrib.contenttypes.models import ContentType
from hstore_flattenfields.forms import HStoreModelForm
from hstore_flattenfields.fields import *

from models import *

SAMPLE_CHOICES = [(x, x) for x in xrange(0, 5)]

FORM_BUILDER_ALLOWED_ENTITIES = [
    'product'
]

FORM_BUILDER_DISABLE_FIELDS = {
    'refer': HiddenInput(),
    'typo': HiddenInput(),
}

TYPECONFIG_MAP = {
    'text_fields_configs': ['Input', 'Integer', 'Float', 'Date', 'DateTime', 'TextArea'],
    'multiple_choice_fields_configs': ['MultSelect', 'CheckBox'],
    'single_choice_fields_configs': ['Select', 'RadioButton'],
}

class ChooseEntityForm(Form):
    entity = CharField(
        widget=Select(
            choices=[
                (ctype.model_class().__name__, ctype.name.title())\
                for ctype in ContentType.objects.filter(
                    name__in=FORM_BUILDER_ALLOWED_ENTITIES
                )
            ]
        ),
        label=u"Entidade"
    )

class TextFieldsForm(Form):
    text = CharField(
        label=u"Campo Texto",
        widget=TextInput(attrs={
            'data-typo': 'Input',
        })
    )
    integer = IntegerField(
        label=u"Campo Numérico",
        widget=TextInput(attrs={
            'data-typo': 'Integer',
        })
    )
    decimal = DecimalField(
        label=u"Campo Decimal",
        help_text=u"Com duas (2) casas decimais",
        widget=TextInput(attrs={
            'data-typo': 'Float',
        })
    )
    date = DateField(
        widget=DateInput(
            format='%d/%m/%Y',
            attrs={'data-typo': 'Date'}
        ),
        label=u"Data",
        help_text=u"formato: (dd/mm/aaaa)"
    )
    datetime = CharField(
        widget=DateTimeInput(
            format='%d/%m/%Y %H:%M:%S',
            attrs={'data-typo': 'DateTime'}
        ),
        label=u"Tempo",
        help_text=u"formato: (dd/mm/aaaa hh:mm:ss)"
    )
    textarea = CharField(
        label=u"Caixa de Texto",
        widget=Textarea(attrs={
            'data-typo': 'TextArea'
        }),
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
            choices=SAMPLE_CHOICES,
            attrs={'data-typo': 'MultSelect'}
        ),
        label=u"Multi-seleções",
    )
    checkbox = ChoiceField(
        widget=CheckboxSelectMultiple(attrs={
            'data-typo': 'CheckBox'
        }),
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
            choices=SAMPLE_CHOICES,
            attrs={'data-typo': 'Select'}
        ),
        label=u"Única Seleção"
    )
    radio = ChoiceField(
        widget=RadioSelect(attrs={'data-typo': 'RadioButton'}),
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
        widgets = FORM_BUILDER_DISABLE_FIELDS


class MultipleChoiceFieldsConfigsForm(ModelForm):
    class Meta:
        model = CustomDynamicField
        widgets = FORM_BUILDER_DISABLE_FIELDS


class SingleChoiceFieldsConfigsForm(ModelForm):
    class Meta:
        model = CustomDynamicField
        widgets = FORM_BUILDER_DISABLE_FIELDS


class CustomDynamicFieldForm(ModelForm):
    class Meta:
        model = CustomDynamicField
    
class OnlyCustomDynamicFieldForm(ModelForm):
    class Meta:
        model = Product

    def __init__(self, *args, **kwargs):
        super(OnlyCustomDynamicFieldForm, self).__init__(*args, **kwargs)
        dfieldnames = self.instance._meta.get_all_dynamic_field_names()
        for field in self.fields:
            if field not in dfieldnames:
                self.fields.pop(field)
        
    
from django.forms.formsets import formset_factory
DynamicFieldFormSet = formset_factory(OnlyCustomDynamicFieldForm)