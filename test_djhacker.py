import pytest

from django.db import models
from django import forms
from django.forms.models import modelform_factory

import djhacker


@pytest.fixture
def model():
    class TestModel(models.Model):
        charfield = models.CharField(max_length=200)
        intfield = models.IntegerField()
        fk = models.ForeignKey('self', on_delete=models.CASCADE)

        class Meta:
            app_label = 'auth'

    return TestModel


def test_formfield_noclass(model):
    # test not passing a class
    djhacker.formfield(
        model.charfield,
        min_length=99,
    )

    # create a django modelform
    form = modelform_factory(model, fields='__all__')

    # test min_length override
    charfield = form.base_fields['charfield']
    assert isinstance(charfield, forms.CharField)
    assert charfield.min_length == 99


def test_formfield_class(model):
    # test fk with class
    class MyChoiceField(forms.ModelChoiceField):
        pass

    djhacker.formfield(
        model.fk,
        MyChoiceField,
        empty_label='TEST',
    )

    # create a django modelform
    form = modelform_factory(model, fields='__all__')

    # test fk with class
    fk = form.base_fields['fk']
    assert isinstance(fk, MyChoiceField)
    assert fk.empty_label == 'TEST'


def test_formfield_sideeffect(model):
    # test not passing a class
    djhacker.formfield(
        model.charfield,
        min_length=99,
    )

    # create a django modelform
    form = modelform_factory(model, fields='__all__')

    # test against unwanted side effect
    assert not isinstance(form.base_fields['intfield'], forms.UUIDField)


def test_registry(model):
    def cb():
        pass
    djhacker.registry.register(models.BooleanField, cb)
    assert djhacker.registry.get(models.BooleanField) == cb
    assert djhacker.registry.get(models.BooleanField()) == cb


def test_register(model):
    @djhacker.register(models.IntegerField)
    def custom_fk_formfield(field, **kwargs):
        kwargs['form_class'] = forms.ChoiceField
        kwargs['choices'] = ((1, 1),)
        return kwargs

    # you don't need to pass extra arguments anymore for ForeignKey fields:
    djhacker.formfield(model.intfield)
    form = modelform_factory(model, fields='__all__')
    result = form.base_fields['intfield']
    assert isinstance(result, forms.ChoiceField)

    # test re-registration as well as kwargs passthrough
    djhacker.formfield(model.intfield, choices=((2, 2),))
    form = modelform_factory(model, fields='__all__')
    result = form.base_fields['intfield']
    assert isinstance(result, forms.ChoiceField)
    assert result.choices == [(2, 2)]


def test_media_script_attributes():
    class Widget(forms.TextInput):
        class Media:
            js = ['a/b.js[c=d][e=f]', 'a.js']
    assert Widget().media.render_js() == [
        '<script src="/static/a/b.js%5Bc%3Dd%5D%5Be%3Df%5D"></script>',
        '<script src="/static/a.js"></script>',
    ]
    djhacker.media_script_attributes()
    assert Widget().media.render_js() == [
        '<script src="/static/a/b.js" c="d" e="f"></script>',
        '<script src="/static/a.js"></script>',
    ]
