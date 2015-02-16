from django.forms import ModelForm #, HiddenInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field

from .models import AgencyReview


class AgencyReviewForm(ModelForm):
    html5_required = True

    def __init__(self, *args, **kwargs):
        super(AgencyReviewForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            'agency',
            'rating',
            Div(css_id="ratystars"),
            Field('title', size=56),
            Field('review', cols=56),
            Submit('submit', 'Submit')
        )

    class Meta:
        model = AgencyReview
        fields = ('agency', 'rating', 'title', 'review')
        # widgets = {
        #     'rating': HiddenInput(),
        # }
