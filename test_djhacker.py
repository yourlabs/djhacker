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

    TestForm = modelform_factory(model, fields='__all__')
    result = TestForm.base_fields['charfield']
    assert isinstance(result, forms.UUIDField)
    assert not result.strip

    # test against unwanted side effect
    assert not isinstance(TestForm.base_fields['intfield'], forms.UUIDField)


def test_registry(model):
    def cb():
        pass
    djhacker.registry.register(models.BooleanField, cb)
    assert djhacker.registry.get(models.BooleanField) == cb
    assert djhacker.registry.get(models.BooleanField()) == cb


def test_register(model):
    @djhacker.register(models.IntegerField)
    def custom_fk_formfield(field):
        return forms.ChoiceField, dict(
            choices=((1, 1), (2, 2)),
        )

    # you don't need to pass extra arguments anymore for ForeignKey fields:
    djhacker.formfield(model.intfield)
    TestForm = modelform_factory(model, fields='__all__')
    result = TestForm.base_fields['intfield']
    assert isinstance(result, forms.ChoiceField)
