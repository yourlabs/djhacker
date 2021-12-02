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

        class Meta:
            app_label = 'auth'

    return TestModel


def test_formfield(model):
    djhacker.formfield(
        model.charfield,
        forms.UUIDField,
        strip=False,
    )

    form = modelform_factory(model, fields='__all__')
    result = form.base_fields['charfield']
    assert isinstance(result, forms.UUIDField)
    assert not result.strip

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
        return forms.ChoiceField, {
            'choices': ((1, 1),),
            **kwargs,
        }

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


def test_esm_django():
    class Widget(forms.TextInput):
        class Media:
            js = ['a/b.js[c=d][e=f]', 'a.js']
    assert Widget().media.render_js() == [
        '<script src="/static/a/b.js%5Bc%3Dd%5D%5Be%3Df%5D"></script>',
        '<script src="/static/a.js"></script>',
    ]
    djhacker.esm_django()
    assert Widget().media.render_js() == [
        '<script src="/static/a/b.js" c="d" e="f"></script>',
        '<script src="/static/a.js"></script>',
    ]
