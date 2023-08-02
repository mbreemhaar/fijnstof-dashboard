from django.utils.timezone import now
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_data_timestamp'] = now()
        return context
