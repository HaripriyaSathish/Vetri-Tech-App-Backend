from rest_framework import serializers
from .models import Course, Tool, BenefitSection, Faq


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ["name", "icon"]


class BenefitSectionSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = BenefitSection
        fields = ["title", "items"]


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ["question", "answer"]


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight — used for the courses.tsx list/browse page (CourseCard)."""

    class Meta:
        model = Course
        fields = [
            "id",
            "image",
            "title",
            "duration",
            "highlight",
            "description",
            "category",
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Full nested payload — used for app/courses/[id].tsx (course detail page)."""

    tools = ToolSerializer(many=True, read_only=True)
    benefits = BenefitSectionSerializer(many=True, read_only=True)
    faqs = FaqSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "image",
            "title",
            "duration",
            "highlight",
            "description",
            "overview",
            "category",
            "brochure_file",
            "tools",
            "benefits",
            "faqs",
        ]