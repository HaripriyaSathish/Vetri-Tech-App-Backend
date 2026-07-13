from django.contrib import admin
from .models import Course, Tool, BenefitSection, Faq


class ToolInline(admin.TabularInline):
    model = Tool
    extra = 1


class BenefitSectionInline(admin.StackedInline):
    model = BenefitSection
    extra = 1
    fields = ["title", "items_text", "order"]


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "category", "duration", "order"]
    list_filter = ["category"]
    search_fields = ["title", "id"]
    prepopulated_fields = {"id": ("title",)}  # auto-suggests a slug from the title when adding
    inlines = [ToolInline, BenefitSectionInline, FaqInline]