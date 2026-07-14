"""
One-time import of the existing hardcoded About page content into the DB.
Run after migrate:  python manage.py import_about_content

IMAGES: copy the source files into import_assets/about/... (paths below)
before running this. Missing files are skipped with a warning — you can
upload them manually via Django Admin afterward.
"""

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from site_content.models import (
    AboutIntro, MissionVisionCard, EcosystemCard, TrainingApproachCard,
    SkillItem, JourneyStep, EnrollItem, ImpactStat,
)

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


MISSION_VISION = [
    ("about/mission.jpg", "Mission",
     "To provide IT training that helps learners develop technical skills, confidence, and readiness for real-world career opportunities."),
    ("about/vision.png", "Vision",
     "To create a learning platform that supports students and beginners in building strong IT knowledge and growing towards successful professional careers."),
]

ECOSYSTEM = [
    ("about/vts-logo.jpg", "Vetri Technology Solution (VTS)",
     ["Provides IT training programs", "Focus on practical skill development"],
     "https://vetritechnologysolutions.in"),
    ("about/vis-logo.webp", "Vetri IT System (VIS)",
     ["Provide internship opportunities", "Real industry exposure"],
     "https://vetriitsystems.in"),
    ("about/vcs-logo.jpg", "Vetri Consultancy Services (VCS)",
     ["Provide career guidance", "Support job-related consultation"],
     "https://vetriconsultancyservices.in"),
]

TRAINING_APPROACH = [
    "At VTS, we believe quality education should be accessible without compromise. Our programs are thoughtfully structured to support learners from diverse backgrounds, including those with career gaps. We focus on skills, growth, and readiness — not on past timelines.",
    "Our training fees remain affordable because we operate as part of a strong ecosystem, not as a standalone institute. We never compromise on quality, mentorship, or learning outcomes.",
]

SKILLS = [
    ("chatbox-ellipses-outline", "About the Training Platform",
     ["Student - focused IT training", "Practical skill development", "Structured learning support"]),
    ("school-outline", "Our Learning Approach",
     ["Step-by-step teaching", "Hand-on practice", "Daily Task", "Projects"]),
    ("clipboard-outline", "Industry Connection",
     ["Linked with real IT startup", "Awareness of industry practices", "Career-oriented learning"]),
]

JOURNEY = [
    ("journey/entry-counseling.png", "Entry & Counseling", "Get guidance to choose the right career."),
    ("journey/joining.webp", "Joining", "Enroll and receive course access and schedule."),
    ("journey/training-phase.png", "Training Phase", "Learn through practical sessions and real projects."),
    ("journey/completion-certification.png", "Completion & Certification", "Finish the course and earn your certificate."),
    ("journey/best-performer.png", "Best Performer Opportunity", "Top performers get hands-on internship experience."),
    ("journey/job-opportunity.webp", "Job Opportunity", "Outstanding students may receive job opportunities."),
]

ENROLL = [
    ("enroll/students.png", "Students"),
    ("enroll/fresher-graduates.png", "Fresher Graduates"),
    ("enroll/working-professionals.png", "Working Professionals"),
    ("enroll/career-break-learners.png", "Career Break Learners"),
    ("enroll/career-switchers.png", "Career Switchers"),
]

IMPACT = [
    (8, "+", 0, "Years of Excellence"),
    (5000, "+", 0, "Students Trained"),
    (85, "%", 0, "Placement Rate"),
    (4.8, "/5", 1, "Student Satisfaction"),
]


class Command(BaseCommand):
    help = "Imports existing About page content into the database."

    def handle(self, *args, **options):
        # --- Intro (Hero/Story/Mascot/CTA) ---
        intro = AboutIntro.load()
        intro.hero_title = "About Vetri Training – Online IT Courses with Placement Support"
        intro.hero_subtitle = "Empowering the next generation of IT Professionals with foundational knowledge and industry-ready skills"
        intro.story_heading = "Our Story – Building Job-Oriented Training Programs"
        intro.story_paragraph1 = "VTS was founded with a simple observation — many learners struggle to enter the IT industry not due to lack of talent, but because they lack practical exposure, confidence, and guided direction."
        intro.story_paragraph2 = "We built Vetri Technology Solutions to bridge this gap through structured training, real-time collaboration, and a strong learning ecosystem."
        intro.cta_title = "Ready to Start Your Career"
        intro.cta_body = "Direct placement support and interview opportunities at our integrated IT startup ecosystem. Start your career with confidence!"
        intro.save()

        if not intro.story_image:
            if not attach_file(intro, "story_image", "about/about-our-story.png"):
                self.stdout.write(self.style.WARNING("  Story image not found — upload manually."))
        if not intro.mascot_image:
            if not attach_file(intro, "mascot_image", "about/mascot.png"):
                self.stdout.write(self.style.WARNING("  Mascot image not found — upload manually."))
        if not intro.cta_avatar:
            if not attach_file(intro, "cta_avatar", "about/consultant-avatar.png"):
                self.stdout.write(self.style.WARNING("  CTA avatar not found — upload manually."))
        self.stdout.write(self.style.SUCCESS("About Intro saved."))

        # --- Mission/Vision ---
        if not MissionVisionCard.objects.exists():
            for order, (icon_path, title, desc) in enumerate(MISSION_VISION):
                card = MissionVisionCard.objects.create(title=title, description=desc, order=order)
                if not attach_file(card, "icon", icon_path):
                    self.stdout.write(self.style.WARNING(f"  Icon not found for '{title}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(MISSION_VISION)} mission/vision cards."))
        else:
            self.stdout.write(self.style.WARNING("Mission/Vision cards already exist — skipping."))

        # --- Ecosystem ---
        if not EcosystemCard.objects.exists():
            for order, (icon_path, title, items, url) in enumerate(ECOSYSTEM):
                card = EcosystemCard.objects.create(
                    title=title, items_text="\n".join(items), site_url=url, order=order
                )
                if not attach_file(card, "icon", icon_path):
                    self.stdout.write(self.style.WARNING(f"  Icon not found for '{title}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(ECOSYSTEM)} ecosystem cards."))
        else:
            self.stdout.write(self.style.WARNING("Ecosystem cards already exist — skipping."))

        # --- Training Approach ---
        if not TrainingApproachCard.objects.exists():
            for order, text in enumerate(TRAINING_APPROACH):
                TrainingApproachCard.objects.create(text=text, order=order)
            self.stdout.write(self.style.SUCCESS(f"Imported {len(TRAINING_APPROACH)} training approach cards."))
        else:
            self.stdout.write(self.style.WARNING("Training approach cards already exist — skipping."))

        # --- Skills ---
        if not SkillItem.objects.exists():
            for order, (icon_name, title, items) in enumerate(SKILLS):
                SkillItem.objects.create(
                    icon_name=icon_name, title=title, items_text="\n".join(items), order=order
                )
            self.stdout.write(self.style.SUCCESS(f"Imported {len(SKILLS)} skill items."))
        else:
            self.stdout.write(self.style.WARNING("Skill items already exist — skipping."))

        # --- Journey ---
        if not JourneyStep.objects.exists():
            for order, (icon_path, title, desc) in enumerate(JOURNEY):
                step = JourneyStep.objects.create(title=title, description=desc, order=order)
                if not attach_file(step, "icon", icon_path):
                    self.stdout.write(self.style.WARNING(f"  Icon not found for '{title}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(JOURNEY)} journey steps."))
        else:
            self.stdout.write(self.style.WARNING("Journey steps already exist — skipping."))

        # --- Enroll ---
        if not EnrollItem.objects.exists():
            for order, (icon_path, title) in enumerate(ENROLL):
                item = EnrollItem.objects.create(title=title, order=order)
                if not attach_file(item, "icon", icon_path):
                    self.stdout.write(self.style.WARNING(f"  Icon not found for '{title}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(ENROLL)} enroll items."))
        else:
            self.stdout.write(self.style.WARNING("Enroll items already exist — skipping."))

        # --- Impact ---
        if not ImpactStat.objects.exists():
            for order, (target, suffix, decimals, label) in enumerate(IMPACT):
                ImpactStat.objects.create(target=target, suffix=suffix, decimals=decimals, label=label, order=order)
            self.stdout.write(self.style.SUCCESS(f"Imported {len(IMPACT)} impact stats."))
        else:
            self.stdout.write(self.style.WARNING("Impact stats already exist — skipping."))

        self.stdout.write(self.style.SUCCESS("Done."))