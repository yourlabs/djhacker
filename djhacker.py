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
