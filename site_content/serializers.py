from rest_framework import serializers
from .models import ContactInfo, Branch, Achievement, ContactFaq, FooterAddress
from .models import (
    AboutIntro, MissionVisionCard, EcosystemCard, TrainingApproachCard,
    SkillItem, JourneyStep, EnrollItem, ImpactStat,
)


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
    


class AboutIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutIntro
        fields = [
            "hero_title", "hero_subtitle",
            "story_heading", "story_paragraph1", "story_paragraph2", "story_image",
            "mascot_image",
            "cta_title", "cta_body", "cta_avatar",
        ]


class MissionVisionCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionVisionCard
        fields = ["id", "icon", "title", "description", "order"]


class EcosystemCardSerializer(serializers.ModelSerializer):
    items = serializers.ReadOnlyField()

    class Meta:
        model = EcosystemCard
        fields = ["id", "icon", "title", "items", "site_url", "order"]


class TrainingApproachCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingApproachCard
        fields = ["id", "text", "order"]


class SkillItemSerializer(serializers.ModelSerializer):
    items = serializers.ReadOnlyField()

    class Meta:
        model = SkillItem
        fields = ["id", "icon_name", "title", "items", "order"]


class JourneyStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyStep
        fields = ["id", "icon", "title", "description", "order"]


class EnrollItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollItem
        fields = ["id", "icon", "title", "order"]


class ImpactStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStat
        fields = ["id", "target", "suffix", "decimals", "label", "order"]


class AboutPageSerializer(serializers.Serializer):
    """One combined payload for the whole About page."""

    intro = serializers.SerializerMethodField()
    mission_vision = serializers.SerializerMethodField()
    ecosystem = serializers.SerializerMethodField()
    training_approach = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    journey = serializers.SerializerMethodField()
    enroll = serializers.SerializerMethodField()
    impact = serializers.SerializerMethodField()

    def get_intro(self, obj):
        return AboutIntroSerializer(AboutIntro.load(), context=self.context).data

    def get_mission_vision(self, obj):
        return MissionVisionCardSerializer(MissionVisionCard.objects.all(), many=True, context=self.context).data

    def get_ecosystem(self, obj):
        return EcosystemCardSerializer(EcosystemCard.objects.all(), many=True, context=self.context).data

    def get_training_approach(self, obj):
        return TrainingApproachCardSerializer(TrainingApproachCard.objects.all(), many=True, context=self.context).data

    def get_skills(self, obj):
        return SkillItemSerializer(SkillItem.objects.all(), many=True, context=self.context).data

    def get_journey(self, obj):
        return JourneyStepSerializer(JourneyStep.objects.all(), many=True, context=self.context).data

    def get_enroll(self, obj):
        return EnrollItemSerializer(EnrollItem.objects.all(), many=True, context=self.context).data

    def get_impact(self, obj):
        return ImpactStatSerializer(ImpactStat.objects.all(), many=True, context=self.context).data    
    
from .models import HomeIntro, HomeBenefit, HomeStep, HomeProject, HomeStory, ImpactStat


class HomeIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeIntro
        fields = [
            "hero_title", "hero_description", "hero_bg_image",
            "whoweare_image", "established_title", "established_text",
            "whoweare_heading", "whoweare_description",
            "whychoose_mascot_image",
            "howitworks_heading", "howitworks_subtext",
            "projects_heading", "projects_subtext",
            "stories_heading", "stories_subtext",
            "cta_heading", "cta_subtext", "cta_mascot_image",
        ]


class HomeBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBenefit
        fields = ["id", "icon_name", "title", "description", "order"]


class HomeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStep
        fields = ["id", "icon", "title", "description", "step_number", "order"]


class HomeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeProject
        fields = ["id", "image", "title", "author", "tag", "tall", "order"]


class HomeStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStory
        fields = ["id", "image", "video", "name", "role", "order"]


class HomePageSerializer(serializers.Serializer):
    """One combined payload for the whole Home page.
    Stats reuse the same ImpactStat data already used on the About page —
    single source of truth, edit once in Admin, updates both pages."""

    intro = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    benefits = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    stories = serializers.SerializerMethodField()

    def get_intro(self, obj):
        return HomeIntroSerializer(HomeIntro.load(), context=self.context).data

    def get_stats(self, obj):
        return ImpactStatSerializer(ImpactStat.objects.all(), many=True, context=self.context).data

    def get_benefits(self, obj):
        return HomeBenefitSerializer(HomeBenefit.objects.all(), many=True, context=self.context).data

    def get_steps(self, obj):
        return HomeStepSerializer(HomeStep.objects.all(), many=True, context=self.context).data

    def get_projects(self, obj):
        return HomeProjectSerializer(HomeProject.objects.all(), many=True, context=self.context).data

    def get_stories(self, obj):
        return HomeStorySerializer(HomeStory.objects.all(), many=True, context=self.context).data    
    

from .models import EnquirySubmission, EnrollmentSubmission

class EnquirySubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquirySubmission
        fields = ["full_name", "email", "phone", "course_interest", "message"]


class EnrollmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentSubmission
        fields = [
            "first_name", "last_name", "phone", "email", "gender", "dob",
            "address", "city", "state", "pincode", "course_name", "mode", "message",
        ]    