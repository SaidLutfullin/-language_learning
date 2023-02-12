from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import ServicePage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from loguru import logger


class ServicePageView(LoginRequiredMixin, TemplateView):
    model = ServicePage

    template_name = 'common/service_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            page = self.model.objects.get(page_type=self.kwargs.get('page_type'))
        except ObjectDoesNotExist:
            page = None
        context['page'] = page
        return context


def page_not_found_view(request, exception):
    return render(request, 'common/404.html', status=404)


def server_error(request, *args, **kwargs):
    return render(request, 'common/500.html', status=500)
