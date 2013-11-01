from plone.dexterity.browser.edit import DefaultEditForm
from plone.z3cform import layout
import itertools

class EditForm(DefaultEditForm):

    default_fieldset_label = 'Saved general info'

    def render(self, *args, **kwargs):
        if len(self.groups):
            self.request['fieldset.current'] = '#fieldset-0'
        for widget in itertools.chain(self.widgets.values(), 
                *[group.widgets.values() for group in self.groups]):
            if widget.field.__name__ in ['ilo_reviewer',
                                        'external_reviewer',
                                        'editor_name',
                                        'external_editor_name',
                                        'ilo_reviewers']:
                widget.size = 120 
        return super(EditForm, self).render(*args, **kwargs)

EditView = layout.wrap_form(EditForm)

