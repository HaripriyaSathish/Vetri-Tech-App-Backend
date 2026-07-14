import os
import resend
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from .serializers import (
    ContactPageSerializer,
    FooterSerializer,
    AboutPageSerializer,
    HomePageSerializer,
    EnquirySubmissionSerializer,
    EnrollmentSubmissionSerializer,
)

resend.api_key = os.environ.get("RESEND_API_KEY")


class ContactPageView(APIView):
    def get(self, request):
        serializer = ContactPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)


class FooterView(APIView):
    def get(self, request):
        serializer = FooterSerializer(instance={}, context={"request": request})
        return Response(serializer.data)


class AboutPageView(APIView):
    def get(self, request):
        serializer = AboutPageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)


class HomePageView(APIView):
    def get(self, request):
        serializer = HomePageSerializer(instance={}, context={"request": request})
        return Response(serializer.data)


class EnquirySubmissionView(APIView):
    def post(self, request):
        serializer = EnquirySubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()
            try:
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": [settings.NOTIFY_EMAIL_TO],
                    "subject": f"New Enquiry: {submission.full_name or 'Unknown'}",
                    "text": (
                        f"Name: {submission.full_name}\n"
                        f"Email: {submission.email}\n"
                        f"Phone: {submission.phone}\n"
                        f"Course Interest: {submission.course_interest}\n"
                        f"Message: {submission.message}"
                    ),
                })
            except Exception as e:
                # Never let an email failure break the actual submission —
                # the enquiry is already saved to the database regardless.
                print(f"Email send failed (Enquiry): {e}")
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentSubmissionView(APIView):
    def post(self, request):
        serializer = EnrollmentSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()
            try:
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": [settings.NOTIFY_EMAIL_TO],
                    "subject": f"New Enrollment: {submission.first_name} {submission.last_name} — {submission.course_name}",
                    "text": (
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
                })
            except Exception as e:
                print(f"Email send failed (Enrollment): {e}")
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)