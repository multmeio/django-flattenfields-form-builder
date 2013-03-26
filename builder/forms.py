from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from django import forms

SAMPLE_CHOICES = [(x, x) for x in xrange(0, 5)]

class TextFieldsForm(forms.Form):
    text = forms.CharField()
    integer = forms.IntegerField()
    decimal = forms.DecimalField()
    date = forms.CharField(widget=forms.DateInput(format='%Y-%m-%d'))
    datetime = forms.CharField(widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'))
    textarea = forms.CharField(widget=forms.Textarea())


class MultipleChoiceFieldsForm(forms.Form):
    select_multiple = forms.CharField(widget=forms.SelectMultiple(choices=SAMPLE_CHOICES))
    checkbox = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=SAMPLE_CHOICES))


class SingleChoiceFieldsForm(forms.Form):
    select = forms.CharField(widget=forms.Select(choices=SAMPLE_CHOICES))
    radio = forms.ChoiceField(widget=forms.RadioSelect, choices=SAMPLE_CHOICES)
