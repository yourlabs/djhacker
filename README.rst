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

Custom formfield callback
=========================

You can register custom form field for model field types:

.. code-block:: py

    @djhacker.register(models.ForeignKey)
    def custom_fk_formfield(model_field, **kwargs):
        return YourFormField, {
            'custom_form_field_kwarg': 'something',
            **kwargs,
        )

    # you don't need to pass extra arguments anymore for ForeignKey fields:
    djhacker.formfield(YourModel.some_fk, queryset=Some.objects.all())

ESM Modules in widget Media
===========================

Another feature that won't be implemented in Django is `EcmaScript Modules support
<https://code.djangoproject.com/ticket/33336>`_. Let's have this anyway, first
patch Django's Media render_js:

.. code-block:: py

    import djhacker
    djhacker.esm_django()

This will let you add script attributes to Media JS, import a module as such:

.. code-block:: python

    class YourWidget(forms.Widget):
        class Media:
            js = [
                'your/script.js[type=module]',
            ]

It will render as such:

.. code-block:: html

    <script src="/static/your/script.js" type="module"></script>
