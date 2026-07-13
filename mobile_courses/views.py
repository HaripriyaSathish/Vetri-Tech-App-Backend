from rest_framework import generics
from .models import Course
from .serializers import CourseListSerializer, CourseDetailSerializer


class CourseListView(generics.ListAPIView):
    """GET /api/courses/ — mirrors `courses` array import in courses.tsx"""

    queryset = Course.objects.prefetch_related("tools", "benefits", "faqs")
    serializer_class = CourseListSerializer


class CourseDetailView(generics.RetrieveAPIView):
    """GET /api/courses/<id>/ — mirrors courses.find(c => c.id === id) in [id].tsx"""

    queryset = Course.objects.prefetch_related("tools", "benefits", "faqs")
    serializer_class = CourseDetailSerializer
    lookup_field = "id"