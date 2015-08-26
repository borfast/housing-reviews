from django.conf import settings
# from django.contrib.auth.models import Group
from django.dispatch import receiver
# from django.views.generic.simple import direct_to_template
from django.views.generic.base import TemplateView

# from allauth.account.utils import setup_user_email
from allauth.account.signals import user_signed_up
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
import mailchimp
import logging

# from invitation.backends import InvitationBackend
from come_in.models import InvitationKey


class WrongInvitationKey(TemplateView):
    template_name = 'come_in/wrong_invitation_key.html'

    def get_context_data(self, **kwargs):
        context = super(WrongInvitationKey, self).get_context_data(**kwargs)
        context['invitation_context'] = self.request.session.get('invitation_context', {})
        return context


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if getattr(settings, 'ALLOW_NEW_REGISTRATIONS', False):
            if getattr(settings, 'INVITE_MODE', False):
                invitation_key = request.session.get('invitation_key', False)
                if invitation_key:
                    if InvitationKey.objects.is_key_valid(invitation_key):
                        invitation_email = request.session.get('invitation_email', False)
                        # print 'account adapter invitation_email: ',invitation_email
                        self.stash_verified_email(request, invitation_email)
                        request.session['invitation_accepted'] = True
                        return True
                    else:
                        del request.session['invitation_accepted']
                        raise ImmediateHttpResponse(WrongInvitationKey.as_view())
            else:
                return True
        return False

    @receiver (user_signed_up)
    def complete_signup(self, **kwargs):
        user = kwargs.pop('user')
        request = kwargs.pop('request')
        # sociallogin = request.session.get('socialaccount_sociallogin', None)

        # Handle user permissions
        # user.groups.add(Group.objects.get(name=settings.DEFAULT_USER_GROUP))
        # user.save()

        # Handle invitation if required
        if 'invitation_key' in request.session.keys():
            invitation_key = request.session.get('invitation_key', False)
            invitation_key = InvitationKey.objects.get_key(invitation_key)
            invitation_key.mark_used(user)
            invited_email = request.session['invitation_email']
            del request.session['invitation_key']
            del request.session['invitation_email']
            if 'invitation_context' in request.session:
                del request.session['invitation_context']

            if 'invitation_accepted' in request.session:
                del request.session['invitation_accepted']

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
                members = m.lists.member_info(list_id, emails=[{'email':invited_email}])
                member_id = members['data'][0]['euid']

                # Move the member to the group
                merge_vars = {'groupings':[{'id': grouping_id, 'groups':['Invitation accepted, account created']}]}
                m.lists.update_member(list_id, email={'euid':member_id}, merge_vars=merge_vars)

            except mailchimp.Error, e:
                logger = logging.getLogger()
                logger.error('There was an error updating mailchimp after a signup', exc_info=True, extra={
                    'exception': e, 'email_address': invited_email
                })
                # messages.error(request,  "Invalid API key")
            # Finish moving the email address in mailchimp
            ################################################
        # print(user.username, ": has signed up!")


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        # add sociallogin to session, because sometimes it's not there...
        request.session['socialaccount_sociallogin'] = sociallogin
