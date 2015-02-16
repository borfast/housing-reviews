from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from model_utils.models import TimeStampedModel

from agencies.models import Agency



class Review(TimeStampedModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    review = models.TextField()
    rating = models.PositiveIntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))

    class Meta:
        abstract = True


class AgencyReview(Review):
    agency = models.ForeignKey(Agency)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('reviews:detail', args=[str(self.id)])


class AgencyReviewVote(TimeStampedModel):
    user = models.ForeignKey(User)
    review = models.ForeignKey(AgencyReview)
    vote = models.SmallIntegerField()

    def __unicode__(self):
        return "%s from %s for review '%s'" % (self.vote, self.user.username, self.review.title)

    def save(self, *args, **kwargs):
        """Update the review score after saving."""
        super(AgencyReviewVote, self).save(*args, **kwargs)

        votes = AgencyReviewVote.objects.filter(review=self.review)
        score = votes.aggregate(Sum('vote'))
        (review_score, created) = AgencyReviewScore.objects.get_or_create(
            review=self.review,
            defaults={'score':score['vote__sum'], 'total_votes':votes.count()})

        if not created:
            review_score.score = score['vote__sum']
            review_score.total_votes = votes.count()
            review_score.save()



class AgencyReviewScore(models.Model):
    review = models.ForeignKey(AgencyReview)
    score = models.SmallIntegerField()
    total_votes = models.SmallIntegerField()

    def __unicode__(self):
        return 'Score for agency review "%s": %s' % (self.review.title, self.score)



# class HouseReview(Review):
#     pass
