from django.urls import path
from .views import ContactPageView, FooterView
from .views import AboutPageView
from .views import HomePageView
from .views import EnquirySubmissionView, EnrollmentSubmissionView

urlpatterns = [
    path("contact/", ContactPageView.as_view(), name="contact-page"),
    path("footer/", FooterView.as_view(), name="footer"),
    path("about/", AboutPageView.as_view(), name="about-page"),
    path("home/", HomePageView.as_view(), name="home-page"),
    path("enquiries/", EnquirySubmissionView.as_view(), name="enquiry-submit"),
    path("enrollments/", EnrollmentSubmissionView.as_view(), name="enrollment-submit"),
]