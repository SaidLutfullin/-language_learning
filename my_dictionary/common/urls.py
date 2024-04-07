from django.urls import path

from .views import ServicePageView, TextToSpeechAPIView

urlpatterns = [
    path(
        "user_agreement",
        ServicePageView.as_view(),
        {"page_type": "user_agreement"},
        name="user_agreement",
    ),
    path(
        "privacy_policy",
        ServicePageView.as_view(),
        {"page_type": "privacy_policy"},
        name="privacy_policy",
    ),
    path("api/v1/tts", TextToSpeechAPIView.as_view(), name="tts"),
]
