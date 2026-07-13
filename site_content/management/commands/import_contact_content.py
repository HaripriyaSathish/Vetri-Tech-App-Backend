"""
One-time import of the existing hardcoded Contact page content into the DB.
Run after migrate:  python manage.py import_contact_content
"""

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from site_content.models import ContactInfo, Branch, Achievement, ContactFaq

ASSETS_DIR = os.path.join(settings.BASE_DIR, "import_assets")


def resolve_asset(relative_path):
    full_path = os.path.join(ASSETS_DIR, relative_path)
    return full_path if os.path.isfile(full_path) else None


def attach_file(instance, field_name, relative_path):
    path = resolve_asset(relative_path)
    if not path:
        return False
    try:
        with open(path, "rb") as f:
            getattr(instance, field_name).save(os.path.basename(path), File(f), save=True)
        return True
    except Exception as e:
        print(f"    WARNING: could not upload '{relative_path}': {e}")
        return False


BRANCHES = [
    ("Surandai_April's Complex", "April's Complex, Bus stand backside, Surandai-627859"),
    ("Surandai-Shanthi's Complex", "Shanthi's Complex- Surandai Old Market, Near Bus Stand, Surandai- 627859"),
    ("Tirunelveli", "Murali's Tower, Second Floor, VOC Ground Opposite, Palayamkottai, Tirunelveli - 627002"),
]

# relative to import_assets/ — copy the 5 jpegs here from the mobile app
ACHIEVEMENTS = [
    ("Best Emerging IT Startup", "achievements/achievement-1.jpeg"),
    ("Best IT Startup", "achievements/achievement-2.jpeg"),
    ("Emerging Achiever of the year", "achievements/achievement-3.jpeg"),
    ("Welcome Kit", "achievements/achievement-4.jpeg"),
    ("Best IT Startup", "achievements/achievement-5.jpeg"),
]

FAQS = [
    ("What are the course timings?",
     "The batch Timings are Morning 10.00 AM to Evening 06.00 PM - Only Monday to Friday."),
    ("Do you offer placement assistance?",
     "Yes! VCS provides comprehensive placement support including resume building, interview preparation and job referrals."),
    ("what is the batch size?",
     "We maintain small batch sizes of to ensure personalized attention and effective learning."),
]


class Command(BaseCommand):
    help = "Imports existing Contact page content into the database."

    def handle(self, *args, **options):
        info = ContactInfo.load()
        info.office_hours_line1 = "Mon - Sat: 10:00 AM - 5:00 PM"
        info.office_hours_line2 = "Sunday Closed"
        info.phone_1 = "8438164827"
        info.phone_2 = "8438781327"
        info.save()
        self.stdout.write(self.style.SUCCESS("Contact Info saved."))

        if not Branch.objects.exists():
            for order, (title, address) in enumerate(BRANCHES):
                Branch.objects.create(title=title, address=address, order=order)
            self.stdout.write(self.style.SUCCESS(f"Imported {len(BRANCHES)} branches."))
        else:
            self.stdout.write(self.style.WARNING("Branches already exist — skipping."))

        if not Achievement.objects.exists():
            for order, (name, image_path) in enumerate(ACHIEVEMENTS):
                achievement = Achievement.objects.create(name=name, order=order)
                if not attach_file(achievement, "image", image_path):
                    self.stdout.write(self.style.WARNING(f"  Image not found for '{name}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(ACHIEVEMENTS)} achievements."))
        else:
            self.stdout.write(self.style.WARNING("Achievements already exist — skipping."))

        if not ContactFaq.objects.exists():
            for order, (question, answer) in enumerate(FAQS):
                ContactFaq.objects.create(question=question, answer=answer, order=order)
            self.stdout.write(self.style.SUCCESS(f"Imported {len(FAQS)} FAQs."))
        else:
            self.stdout.write(self.style.WARNING("FAQs already exist — skipping."))

        self.stdout.write(self.style.SUCCESS("Done."))