from django.views.generic import ListView, DetailView, CreateView, View
from django.core.exceptions import ObjectDoesNotExist

from braces.views import LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin

from .forms import AgencyReviewForm
from .models import AgencyReview, AgencyReviewVote, AgencyReviewScore
from agencies.models import Agency


class ReviewsListView(LoginRequiredMixin, ListView):
    template_name = 'reviews/user_review_list.html'
    model = AgencyReview
    context_object_name = 'reviews'

    class Meta:
        ordering = ["-created"]

    def get_queryset(self):
        agency_id = self.request.GET.get('agency_id')
        if agency_id:
            return AgencyReview.objects.filter(agency_id=agency_id)
        else:
            return super(ReviewsListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ReviewsListView, self).get_context_data(**kwargs)

        # Add the several agencies to the context
        agencies = Agency.objects.all()
        context['agencies'] = agencies
        agency_id = self.request.GET.get('agency_id')
        if agency_id:
            context['filter'] = int(self.request.GET.get('agency_id')) or False

        return context


class AgencyReviewDetailView(LoginRequiredMixin, DetailView):
    model = AgencyReview
    context_object_name = 'review'
    template_name = 'reviews/agency_review_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AgencyReviewDetailView, self).get_context_data(**kwargs)
        # Add in the votes for this review
        (review_score, ignore) = AgencyReviewScore.objects.get_or_create(review=self.object,
            defaults={'score':0, 'total_votes':0})
        if review_score.score < 0:
            review_score.score = 0

        try:
            vote = AgencyReviewVote.objects.get(review=self.object, user=self.request.user)
            user_has_voted = True
            context['user_vote'] = vote.vote
        except ObjectDoesNotExist:
            user_has_voted = False

        context['review_score'] = review_score
        context['user_has_voted'] = user_has_voted
        return context

    # def get_queryset(self):
    #     self.agency = Agency.objects.get(pk=self.kwargs['agency_id'])
    #     return ReviewedItem.objects.filter(agency=self.agency)


class AgencyReviewCreateView(LoginRequiredMixin, CreateView):
    model = AgencyReview
    form_class = AgencyReviewForm
    template_name = 'reviews/agency_review_form.html'

    def form_valid(self, form):
        """Save the rating and the user who wrote the review."""
        agency = form.instance.agency
        agency.rating.add(score=form.instance.rating, user=self.request.user, ip_address=self.request.META['REMOTE_ADDR'])

        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(AgencyReviewCreateView, self).form_valid(form)


class AgencyReviewVoteView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin, View):
    json_dumps_kwargs = {'indent': 2}

    def post_ajax(self, request, *args, **kwargs):
        # Did the user vote up or down?
        if self.kwargs['vote'] == 'up':
            vote = 1
        else:
            vote = -1

        # If the user hasn't voted, allow the vote
        (review_vote, created) = AgencyReviewVote.objects.get_or_create(review_id=self.kwargs['review_id'],
            user=request.user, defaults={'vote':vote})

        # Allow updating an existing vote
        if not created:
            review_vote.vote = vote
            review_vote.save()

        # Retrieve data to return in the AJAX response
        review_score = AgencyReviewScore.objects.get(review_id=self.kwargs['review_id'])
        show_score = review_score.score
        if review_score.score < 0:
            show_score = 0

        json_dict = {
            'vote': vote,
            'created': created,
            'show_score': show_score,
            'total_votes': review_score.total_votes
        }

        return self.render_json_response(json_dict)
