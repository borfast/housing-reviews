from django.forms import Form, EmailField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class InvitationKeyForm(Form):
    html5_required = True
    email = EmailField(label="Your friend's email")

    def __init__(self, *args, **kwargs):
        super(InvitationKeyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            'email',
            FormActions(
                Submit('submit', 'Send invitation'),
            )
        )
