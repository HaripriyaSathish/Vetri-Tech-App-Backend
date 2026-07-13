from django.db import models


class ContactInfo(models.Model):
    """Singleton — only one row will ever exist. Holds the office hours
    and phone numbers shown in the 'We are here for You' section."""
    office_hours_line1 = models.CharField(max_length=100, default="Mon - Sat: 10:00 AM - 5:00 PM")
    office_hours_line2 = models.CharField(max_length=100, default="Sunday Closed")
    phone_1 = models.CharField(max_length=20, default="8438164827")
    phone_2 = models.CharField(max_length=20, default="8438781327")

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