from wtforms.validators import StopValidation


class ListFieldInputRequired(object):
    """ Validates that at least one item was provided for a ListField to match """

    field_flags = ('required',)

    def __call__(self, form, field):
        if len(field.entries) == 0:
            field.errors[:] = []
            raise StopValidation('This field requires at least one item')
