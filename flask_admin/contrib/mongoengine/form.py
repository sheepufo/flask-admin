from mongoengine import ReferenceField, EmbeddedDocumentField

from flask.ext.mongoengine.wtf import orm, fields

from flask.ext.admin import form
from flask.ext.admin.model.fields import InlineFieldList


class CustomModelConverter(orm.ModelConverter):
    @orm.converts('DateTimeField')
    def conv_DateTime(self, model, field, kwargs):
        kwargs['widget'] = form.DateTimePickerWidget()
        return orm.ModelConverter.conv_DateTime(self, model, field, kwargs)

    @orm.converts('ListField')
    def conv_List(self, model, field, kwargs):
        if isinstance(field.field, ReferenceField):
            kwargs['widget'] = form.Select2Widget(multiple=True)

            doc_type = field.field.document_type
            return fields.ModelSelectMultipleField(model=doc_type, **kwargs)
        if field.field.choices:
            kwargs['multiple'] = True
            return self.convert(model, field.field, kwargs)

        unbound_field = self.convert(model, field.field, {})
        kwargs = {
            'validators': [],
            'filters': [],
        }
        return InlineFieldList(unbound_field, min_entries=0, **kwargs)

    @orm.converts('ReferenceField')
    def conv_Reference(self, model, field, kwargs):
        kwargs['widget'] = form.Select2Widget()
        return orm.ModelConverter.conv_Reference(self, model, field, kwargs)


def model_form(model, base_class=form.BaseForm, only=None, exclude=None,
               field_args=None, converter=None):
    return orm.model_form(model, base_class=base_class, only=only,
                          exclude=exclude, field_args=field_args,
                          converter=converter)