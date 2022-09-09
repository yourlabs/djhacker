import re
import types


class Registry(dict):
    def register(self, field_class, callback):
        self[field_class] = callback

    def get(self, field_or_class, *args):
        if field_or_class in self:
            return super().get(field_or_class, *args)
        return super().get(type(field_or_class), *args)


registry = Registry()


def register(field_class):
    def _register(callback):
        return registry.register(field_class, callback)
    return _register


def formfield(model_field, form_class=None, /, **kwargs):
    # Syntactic sugar of making form_class an ordered argument
    if form_class and 'form_class' not in kwargs:
        kwargs['form_class'] = form_class

    # In case of re-registration: first un-patch ModelField.formfield()
    current = getattr(model_field.field, 'djhacker', None)
    if current:
        model_field.field.formfield = model_field.field.djhacker['django']

    # Call registered callback if any to get more default kwargs
    if not form_class:
        cb = registry.get(model_field.field)
        kwargs = {**cb(model_field, **kwargs), **kwargs}

    # This function will be set onto .formfield()
    def _formfield(self, *args, **kw):
        # Add passed kwargs on top of registered kwargs
        kwargs = {**self.djhacker['kwargs'], **kw}

        # Call django's original formfield method with those kwargs
        return self.djhacker['django'](*args, **kwargs)

    # Save the original Django formfield() method and store kwargs on field
    model_field.field.djhacker = dict(
        django=model_field.field.formfield,
        kwargs=kwargs,
    )

    # Patch Django's formfield() method with _formfield
    model_field.field.formfield = types.MethodType(
        _formfield, model_field.field
    )


# That one was nice but we can't use it if we don't want to depend on the regex
# module which seems to have build problems from time to time
# ESM_RE = r'^(?P<path>[^[]+)(\[(?P<key>[^=]+)=(?P<value>[^]]+)\])*$'

ATTRIBUTES = r'\[(?P<key>[^=]+)=(?P<value>[^]]+)\]'


def media_script_attributes():
    from django.forms.widgets import Media
    from django.utils.html import format_html

    def _render_js(self):
        result = []
        for spec in self._js:
            out = '<script src="{}"'
            args = [self.absolute_path(spec.partition('[')[0])]

            for key, value in re.findall(ATTRIBUTES, spec):
                out += ' ' + key + '="{}"'
                args.append(value)
            out += '></script>'
            result.append(format_html(out, *args))
        return result
    Media.django_render_js = Media.render_js
    Media.render_js = _render_js
