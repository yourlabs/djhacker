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

Widget Script attributes
========================

Another thing Django is not doing anytime soon is `letting you customize script
tags <https://code.djangoproject.com/ticket/33336>`_. Which means there's no
easy way to combine Widget.Media.js and any of the nice new script tag
attributes, including, but not limited to:

- ``async``, ``defer``: good to control when your script is loaded
- ``type="module"``: to load a script as an EcmaScript Module (ESM) and use
  imports

Let's have this anyway, first patch Django's Media render_js:

.. code-block:: py

    import djhacker
    djhacker.media_script_attributes()

Then, let's customize a script tag:

.. code-block:: python

    class YourWidget(forms.Widget):
        class Media:
            js = [
                'your/script.js[type=module][defer=true]',
            ]

It will render as such:

.. code-block:: html

    <script src="/static/your/script.js" type="module" defer="true"></script>
