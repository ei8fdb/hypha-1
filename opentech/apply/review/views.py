from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy

from opentech.apply.funds.models import ApplicationSubmission
from .forms import ConceptReviewForm
from .models import Review


class ReviewCreateView(CreateView):
    model = Review
    form_class = ConceptReviewForm

    def get_context_data(self, **kwargs):
        submission = get_object_or_404(ApplicationSubmission, id=self.kwargs['submission_pk'])
        has_submitted_review = Review.objects.filter(submission=submission, author=self.request.user).count() > 0

        return super().get_context_data(
            submission=submission,
            has_submitted_review=has_submitted_review,
            **kwargs
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['submission'] = get_object_or_404(ApplicationSubmission, id=self.kwargs['submission_pk'])
        return kwargs

    def get_success_url(self):
        return reverse_lazy('apply:submission', args=(self.kwargs['submission_pk'],))
