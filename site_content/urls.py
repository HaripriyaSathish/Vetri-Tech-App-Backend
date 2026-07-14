from django.urls import path
from .views import ContactPageView, FooterView

urlpatterns = [
    path("contact/", ContactPageView.as_view(), name="contact-page"),
    path("footer/", FooterView.as_view(), name="footer"),
]