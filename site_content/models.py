from django.db import models


class ContactInfo(models.Model):
    """Singleton — only one row will ever exist. Holds office hours, phone
    numbers, and footer-related fields (social/network links, copyright)."""

    office_hours_line1 = models.CharField(max_length=100, default="Mon - Sat: 10:00 AM - 5:00 PM")
    office_hours_line2 = models.CharField(max_length=100, default="Sunday Closed")
    phone_1 = models.CharField(max_length=20, default="8438164827")
    phone_2 = models.CharField(max_length=20, default="8438781327")

    # --- footer-specific fields (same phone numbers reused above) ---
    instagram_url = models.URLField(
        max_length=300,
        default="https://www.instagram.com/vetriitsurandai?igsh=MW5mYmhsZnU5N3Y3dQ%3D%3D",
    )
    vts_url = models.URLField(max_length=300, default="https://www.vetritechnologysolutions.in/")
    vis_url = models.URLField(max_length=300, default="https://www.vetriit.com/")
    copyright_text = models.CharField(
        max_length=255,
        default="© 2026 Vetri Technology Solutions | Developed and Maintained by Vetri IT Systems Pvt.",
    )

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return "Contact Info"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton — always overwrite the same row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Branch(models.Model):
    title = models.CharField(max_length=150)
    address = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Achievement(models.Model):
    # shared between the Contact page (first 4 shown) and the
    # /learning-environment page (all shown) — same data source, same order
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="site/achievements/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ContactFaq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.question[:50]


class FooterAddress(models.Model):
    # e.g. "Office Address", "Surandai Branch2", "Tirunelveli Branch"
    title = models.CharField(max_length=100)
    # multi-line, \n preserved exactly as shown in app
    address_text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title