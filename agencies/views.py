from django.views.generic import ListView, DetailView

from braces.views import LoginRequiredMixin

from .models import Agency


class AgenciesListView(ListView):
    # template_name = 'agencies_list.html'
    model = Agency
    context_object_name = 'agencies'
    queryset = Agency.objects.order_by('name')

    # def get(self, request):
    #   return 'blah'


class AgencyDetailView(LoginRequiredMixin, DetailView):
    model = Agency
