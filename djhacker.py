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


def formfield(model_field, cls=None, /, **kwargs):
    def _formfield(self, *args, **kw):
        formfield = self.djhacker['django'](*args, **{
            'form_class': self.djhacker['cls'],
            **self.djhacker['kwargs'],
            **kw,
        })
        return formfield

    if not cls:
        cb = registry.get(model_field.field)
        cls, kwargs = cb(model_field, **kwargs)

    current = getattr(model_field.field, 'djhacker', None)
    if current:
        # In case of re-registration
        model_field.field.formfield = model_field.field.djhacker['django']

    model_field.field.djhacker = dict(
        django=model_field.field.formfield,
        cls=cls,
        kwargs=kwargs,
    )
    model_field.field.formfield = types.MethodType(
        _formfield, model_field.field
    )


# That one was nice but we can't use it if we don't want to depend on the regex
# module which seems to have build problems from time to time
# ESM_RE = r'^(?P<path>[^[]+)(\[(?P<key>[^=]+)=(?P<value>[^]]+)\])*$'

ATTRIBUTES = r'\[(?P<key>[^=]+)=(?P<value>[^]]+)\]'


def esm_django():
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
