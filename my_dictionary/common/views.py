from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from gtts import gTTS
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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


# API
class TextToSpeechAPIView(LoginRequiredMixin, APIView):
    def get(self, request):
        text = request.query_params.get("text")
        lang = request.query_params.get("lang")

        if not text or not lang:
            return Response(
                {"error": "Both 'text' and 'lang' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            tts = gTTS(text, lang=lang)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            response = HttpResponse(audio_buffer.read(), content_type="audio/mpeg")
            response["Content-Disposition"] = 'attachment; filename="audio_output.mp3"'
            return response
        except Exception as e:
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
