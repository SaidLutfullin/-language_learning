from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import TemplateView
from loguru import logger

from .models import ServicePage


class ServicePageView(TemplateView):
    model = ServicePage
    template_name = "common/service_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            page = self.model.objects.get(page_type=self.kwargs.get("page_type"))
        except ObjectDoesNotExist:
            page = None
        context["page"] = page
        return context


def page_not_found_view(request, exception):
    logger.error("page")
    page = ServicePage.objects.filter(page_type="404").first()
    return render(
        request, "common/service_page.html", status=404, context={"page": page}
    )


def server_error(request, *args, **kwargs):
    page = ServicePage.objects.filter(page_type="500").first()
    return render(
        request, "common/service_page.html", status=500, context={"page": page}
    )
