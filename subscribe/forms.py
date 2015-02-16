from django.conf import settings
from django.forms import ModelForm
from django.template.loader import render_to_string

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from postmonkey import PostMonkey, MailChimpException

import mandrill
import logging

from .models import Interested


class InterestedForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms text-center'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))

        super(InterestedForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Interested


    def subscribe(self):
        api_key = getattr(settings, 'MAILCHIMP_API_KEY')
        list_id = getattr(settings, 'MAILCHIMP_INVITED_LIST_ID')
        pm = PostMonkey(api_key)

        email_address = self.cleaned_data['email']

        try:
            pm.listSubscribe(id=list_id, email_address=email_address)
        except MailChimpException, e:
            logger = logging.getLogger()
            logger.error('There was some crazy error', exc_info=True, extra={
                'exception': e, 'email_address': email_address
            })
            print e.code  # 200
            print e.error  # u'Invalid MailChimp List ID: 42'



    def send_emails(self):
        #Use this: https://www.dailycred.com/admin/app/e0afa0c5-00ac-47e3-910a-6999a3352234?tab=details

        # First send the email to the user
        email = render_to_string('subscribe/subscribed_email.html', {'email': self.cleaned_data['email']})

        message = {
            'subject': 'St Andrews Housing Reviews',
            'from_email': 'hello@standrews-housing-reviews.com',
            'from_name': 'St Andrews Housing Reviews',
            'to': [{'email': self.cleaned_data['email']}],
            'text': email,
        }

        key = 'NyG2nVjq1Gxan-102NInGw'
        m = mandrill.Mandrill(key)
        m.messages.send(message)

        # Now send another email to me
        message = {
            'subject': 'St Andrews Housing Reviews registration',
            'from_email': 'hello@standrews-housing-reviews.com',
            'from_name': 'St Andrews Housing Reviews',
            'to': [{'email': 'borfast@gmail.com'}],
            'text': self.cleaned_data['email'],
        }
        m.messages.send(message)
