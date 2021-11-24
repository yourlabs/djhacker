Django-Hacker: customize default django forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic usage
===========

Install with ``pip install djhacker`` and then:

.. code-block:: py

    import djhacker

    djhacker.formfield(
        YourModel.your_field,
        YourFormField,
        custom_form_field_kwarg='something',
    )

This will make any Django ModelForm render a
``YourFormField(custom_form_field_kwarg='something')`` by default, plus
whatever other kwargs it wants to add, you won't have to use any specific model
form, this will work natively in the admin for instance.

Registry
========

You can register custom form field for model field types:

.. code-block:: py

    @djhacker.register(models.ForeignKey)
    def custom_fk_formfield(model_field):
        return YourFormField, dict(
            custom_form_field_kwarg='something',
        )

    # you don't need to pass extra arguments anymore for ForeignKey fields:
    djhacker.formfield(YourModel.some_fk)
