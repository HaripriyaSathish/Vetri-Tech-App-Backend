from rest_framework import serializers
from .models import ContactInfo, Branch, Achievement, ContactFaq, FooterAddress


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            "office_hours_line1",
            "office_hours_line2",
            "phone_1",
            "phone_2",
            "instagram_url",
            "vts_url",
            "vis_url",
            "copyright_text",
        ]


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


class FooterAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterAddress
        fields = ["id", "title", "address_text", "order"]


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


class FooterSerializer(serializers.Serializer):
    """One combined payload for the site-wide footer."""

    contact_info = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()

    def get_contact_info(self, obj):
        return ContactInfoSerializer(ContactInfo.load(), context=self.context).data

    def get_addresses(self, obj):
        return FooterAddressSerializer(FooterAddress.objects.all(), many=True, context=self.context).data