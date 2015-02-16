from django.conf import settings
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from braces.views import LoginRequiredMixin
import mailchimp
import logging

# from registration.views import register as registration_register
# from registration.forms import RegistrationForm
# from registration.backends import default as registration_backend

from .models import InvitationKey
from .forms import InvitationKeyForm
# from .backends import InvitationBackend

from django.conf import settings

is_key_valid = InvitationKey.objects.is_key_valid
remaining_invitations_for_user = InvitationKey.objects.remaining_invitations_for_user
get_invitation_key = InvitationKey.objects.get_key

class CreateInvitationKeyView(LoginRequiredMixin, FormView):
    template_name = 'come_in/invitation_form.html'
    form_class = InvitationKeyForm
    # model = InvitationKey

    def get_context_data(self, **kwargs):
        context = super(CreateInvitationKeyView, self).get_context_data(**kwargs)
        context['remaining_invitations'] = remaining_invitations_for_user(self.request.user)
        return context


    def form_valid(self, form):
        remaining_invitations = remaining_invitations_for_user(self.request.user)
        if remaining_invitations > 0 and form.is_valid():
            email = form.cleaned_data['email']
            invitation = InvitationKey.objects.create_invitation(self.request.user, email)
            invitation.send_to(email)

            messages.success(self.request, 'Invitation sent to %s.' % email)

            ##############################################################
            # Move the email address to the "Invited" group in mailchimp
            # TODO: This should go somewhere else!
            api_key = getattr(settings, 'MAILCHIMP_API_KEY')
            list_id = getattr(settings, 'MAILCHIMP_INVITED_LIST_ID')
            try:
                m = mailchimp.Mailchimp(api_key)

                # Get the group ID
                groupings = m.lists.interest_groupings(list_id)
                grouping_id = groupings[0]['id']

                # Get the member ID
                members = m.lists.member_info(list_id, emails=[{'email':email}])
                member_id = members['data'][0]['euid']

                # Move the member to the group
                merge_vars = {'groupings':[{'id': grouping_id, 'groups':['Invitation sent']}]}
                m.lists.update_member(list_id, email={'euid':member_id}, merge_vars=merge_vars)

            except mailchimp.Error, e:
                logger = logging.getLogger()
                logger.error('There was an error updating mailchimp', exc_info=True, extra={
                    'exception': e, 'email_address': email
                })
                # messages.error(request,  "Invalid API key")
            ### Finish moving the email address in mailchimp
            ################################################




            return HttpResponseRedirect(reverse('invitation_invite'))
            # return super(CreateInvitationKeyView, self).form_valid(form)


class InvitationAccepted(TemplateView):
    template_name = 'come_in/invited.html'

    def get_context_data(self, **kwargs):
        context = super(InvitationAccepted, self).get_context_data(**kwargs)
        context['invitation_key'] = self.kwargs['invitation_key']
        return context

    def get(self, request, *args, **kwargs):
        invitation_key = self.kwargs['invitation_key']
        if getattr(settings, 'INVITE_MODE', False):
            if invitation_key and is_key_valid(invitation_key):
                self.template_name = 'come_in/invited.html'
                # invitation_key = get_invitation_key(invitation_key)
                request.session['invitation_key'] = invitation_key
                request.session['invitation_email'] = get_invitation_key(invitation_key).email
                redirect_url = reverse('account_signup')
                return HttpResponseRedirect(redirect_url)
            else:
                self.template_name = 'come_in/wrong_invitation_key.html'
                return super(InvitationAccepted, self).get(self, kwargs)

        else:
            return HttpResponseRedirect(reverse('account_signup'))




# def register(request, backend, success_url=None,
#             form_class=RegistrationForm,
#             disallowed_url='registration_disallowed',
#             post_registration_redirect=None,
#             template_name='registration/registration_form.html',
#             wrong_template_name='invitation/wrong_invitation_key.html',
#             extra_context=None):
#     extra_context = extra_context is not None and extra_context.copy() or {}
#     if getattr(settings, 'INVITE_MODE', False):
#         invitation_key = request.REQUEST.get('invitation_key', False)
#         if invitation_key:
#             extra_context.update({'invitation_key': invitation_key})
#             if is_key_valid(invitation_key):
#                 return registration_register(request, backend, success_url,
#                                             form_class, disallowed_url,
#                                             template_name, extra_context)
#             else:
#                 extra_context.update({'invalid_key': True})
#         else:
#             extra_context.update({'no_key': True})
#         return direct_to_template(request, wrong_template_name, extra_context)
#     else:
#         return registration_register(request, backend, success_url, form_class,
#                                      disallowed_url, template_name, extra_context)


