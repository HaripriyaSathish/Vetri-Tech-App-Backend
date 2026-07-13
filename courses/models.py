from django.db import models


CATEGORY_CHOICES = [
    ("Data", "Data"),
    ("Design", "Design"),
    ("Development", "Development"),
    ("Emerging Tech", "Emerging Tech"),
]


class Course(models.Model):
    # matches the "id" used as the route param in app/courses/[id].tsx,
    # e.g. "data-analysis", "python-fullstack" — kept as a slug, not an auto PK,
    # so existing app links / deep links keep working unchanged.
    id = models.SlugField(primary_key=True, max_length=80)

    image = models.ImageField(upload_to="courses/covers/")
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    highlight = models.CharField(max_length=255)
    description = models.TextField()
    overview = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brochure_file = models.FileField(upload_to="courses/brochures/", blank=True, null=True)

    # controls display order on the courses list page
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Tool(models.Model):
    course = models.ForeignKey(Course, related_name="tools", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="courses/tool_icons/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course_id} — {self.name}"


class BenefitSection(models.Model):
    course = models.ForeignKey(Course, related_name="benefits", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # one bullet item per line — kept as a plain textarea in admin instead of a
    # separate child model, since these items have no fields of their own
    # (avoids needing nested inlines just for a list of strings).
    items_text = models.TextField(
        help_text="One item per line. Each line becomes one bullet point in the app."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course_id} — {self.title}"

    @property
    def items(self):
        return [line.strip() for line in self.items_text.splitlines() if line.strip()]


class Faq(models.Model):
    course = models.ForeignKey(Course, related_name="faqs", on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course_id} — {self.question[:50]}"