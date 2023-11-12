from django.core.exceptions import ObjectDoesNotExist

from common.models import ServicePage


class ServicePageMixin:
    template_name = "common/service_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            page = ServicePage.objects.get(page_type=self.page_type)
        except ObjectDoesNotExist:
            page = None
        context["page"] = page
        return context
