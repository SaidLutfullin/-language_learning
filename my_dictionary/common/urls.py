from django.urls import path

from .views import ServicePageView

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
]
