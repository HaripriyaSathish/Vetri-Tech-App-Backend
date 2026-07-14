from django.contrib import admin
from .models import ContactInfo, Branch, Achievement, ContactFaq, FooterAddress


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