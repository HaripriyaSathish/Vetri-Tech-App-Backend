from django.contrib import admin
from .models import ContactInfo, Branch, Achievement, ContactFaq, FooterAddress
from .models import (
    AboutIntro, MissionVisionCard, EcosystemCard, TrainingApproachCard,
    SkillItem, JourneyStep, EnrollItem, ImpactStat,
)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # prevents creating a second row — this is a singleton
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    ordering = ["order"]


@admin.register(ContactFaq)
class ContactFaqAdmin(admin.ModelAdmin):
    list_display = ["question", "order"]
    ordering = ["order"]


@admin.register(FooterAddress)
class FooterAddressAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]

@admin.register(AboutIntro)
class AboutIntroAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutIntro.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MissionVisionCard)
class MissionVisionCardAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]


@admin.register(EcosystemCard)
class EcosystemCardAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]


@admin.register(TrainingApproachCard)
class TrainingApproachCardAdmin(admin.ModelAdmin):
    list_display = ["order"]
    ordering = ["order"]


@admin.register(SkillItem)
class SkillItemAdmin(admin.ModelAdmin):
    list_display = ["title", "icon_name", "order"]
    ordering = ["order"]


@admin.register(JourneyStep)
class JourneyStepAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]


@admin.register(EnrollItem)
class EnrollItemAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ["label", "target", "order"]
    ordering = ["order"]    