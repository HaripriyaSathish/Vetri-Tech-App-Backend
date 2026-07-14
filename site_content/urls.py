from django.urls import path
from .views import ContactPageView, FooterView
from .views import AboutPageView

urlpatterns = [
    path("contact/", ContactPageView.as_view(), name="contact-page"),
    path("footer/", FooterView.as_view(), name="footer"),
    path("about/", AboutPageView.as_view(), name="about-page"),
]