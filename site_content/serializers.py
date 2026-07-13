from rest_framework import serializers
from .models import ContactInfo, Branch, Achievement, ContactFaq


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ["office_hours_line1", "office_hours_line2", "phone_1", "phone_2"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "title", "address", "order"]


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "name", "image", "order"]


class ContactFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFaq
        fields = ["id", "question", "answer", "order"]


class ContactPageSerializer(serializers.Serializer):
    """One combined payload for the whole Contact page."""
    contact_info = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    faqs = serializers.SerializerMethodField()

    def get_contact_info(self, obj):
        return ContactInfoSerializer(ContactInfo.load(), context=self.context).data

    def get_branches(self, obj):
        return BranchSerializer(Branch.objects.all(), many=True, context=self.context).data

    def get_achievements(self, obj):
        return AchievementSerializer(Achievement.objects.all(), many=True, context=self.context).data

    def get_faqs(self, obj):
        return ContactFaqSerializer(ContactFaq.objects.all(), many=True, context=self.context).data