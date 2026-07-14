from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactPageSerializer, FooterSerializer


class ContactPageView(APIView):
    def get(self, request):
        serializer = ContactPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)


class FooterView(APIView):
    def get(self, request):
        serializer = FooterSerializer(instance={}, context={"request": request})
        return Response(serializer.data)
    

from .serializers import AboutPageSerializer

class AboutPageView(APIView):
    def get(self, request):
        serializer = AboutPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)    
    

from .serializers import HomePageSerializer

class HomePageView(APIView):
    def get(self, request):
        serializer = HomePageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)    
    

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from .serializers import EnquirySubmissionSerializer, EnrollmentSubmissionSerializer


class EnquirySubmissionView(APIView):
    def post(self, request):
        serializer = EnquirySubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()
            try:
                send_mail(
                    subject=f"New Enquiry: {submission.full_name or 'Unknown'}",
                    message=(
                        f"Name: {submission.full_name}\n"
                        f"Email: {submission.email}\n"
                        f"Phone: {submission.phone}\n"
                        f"Course Interest: {submission.course_interest}\n"
                        f"Message: {submission.message}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.NOTIFY_EMAIL_TO],
                    fail_silently=True,  # never let email failure break the actual submission
                )
            except Exception:
                pass
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentSubmissionView(APIView):
    def post(self, request):
        serializer = EnrollmentSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()
            try:
                send_mail(
                    subject=f"New Enrollment: {submission.first_name} {submission.last_name} — {submission.course_name}",
                    message=(
                        f"Name: {submission.first_name} {submission.last_name}\n"
                        f"Phone: {submission.phone}\n"
                        f"Email: {submission.email}\n"
                        f"Gender: {submission.gender}\n"
                        f"DOB: {submission.dob}\n"
                        f"Address: {submission.address}, {submission.city}, {submission.state} - {submission.pincode}\n"
                        f"Course: {submission.course_name}\n"
                        f"Mode: {submission.mode}\n"
                        f"Message: {submission.message}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.NOTIFY_EMAIL_TO],
                    fail_silently=True,
                )
            except Exception:
                pass
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    