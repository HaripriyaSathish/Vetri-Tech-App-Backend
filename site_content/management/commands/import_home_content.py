"""
One-time import of the existing hardcoded Home page content into the DB.
Run after migrate:  python manage.py import_home_content

IMAGES: copy source files into import_assets/home/... (paths below).
VIDEOS: copy the 5 compressed .mp4 files into import_assets/videos/.
Missing files are skipped with a warning — upload manually via Django Admin.
"""

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from site_content.models import HomeIntro, HomeBenefit, HomeStep, HomeProject, HomeStory

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


BENEFITS = [
    ("people", "Industry-Experienced Trainers", "Learn from professionals with 10+ years of real-world industry experience."),
    ("videocam", "Live Interactive Classes", "Engage in real-time discussions and get instant doubt resolution."),
    ("bulb", "Practical Learning Approach", "Work on real projects and build a strong portfolio while you learn."),
    ("trending-up", "Career-Focused Training", "Course content aligned with current industry requirements and trends."),
    ("heart", "Mentorship & Support", "Personalized guidance and continuous support throughout your journey."),
    ("ribbon", "Industry Certification", "Receive recognized certifications to boost your career prospects."),
]

STEPS = [
    ("home/icon-register.png", "Register", "Choose your desired course and sign up easily online.", 1),
    ("home/icon-attend.png", "Attend", "Join live interactive training sessions with experts.", 2),
    ("home/icon-practice.png", "Practice", "Complete real-world tasks and build your portfolio.", 3),
    ("home/icon-certificate.png", "Certificate", "Get officially certified and ready for the industry.", 4),
]

PROJECTS = [
    ("home/project-trustpay.png", "Trust Pay", "Sakthi Priyanka", "AI UI/UX", False),
    ("home/project-coffeeshop.png", "Coffee Shop App", "Chitra", "AI UIUX", True),
    ("home/project-wanderluxe.png", "Wanderluxe", "Nandhini", "AI UI/UX", False),
]

STORIES = [
    ("home/story-deepa.png", "videos/video-deepa.mp4", "Deepa", "UI/UX Designing"),
    ("home/story-nivashini.png", "videos/video-nivashini.mp4", "Nivashini", "Python Fullstack"),
    ("home/story-monisha.png", "videos/video-monisha.mp4", "Monisha", "Python Fullstack"),
    ("home/story-swetha.png", "videos/video-swetha.mp4", "Swetha", "Data Analysis"),
    ("home/story-vidhya.png", "videos/video-vidhya.mp4", "Vidhya", "Python Fullstack"),
]


class Command(BaseCommand):
    help = "Imports existing Home page content into the database."

    def handle(self, *args, **options):
        # --- Intro ---
        intro = HomeIntro.load()
        intro.hero_title = "IT Training, Internship & Career Support"
        intro.hero_description = "This platform is designed for learners who want to build practical IT skills through structured training programs. Along with training, learners are informed about available IT services and consultancy support."
        intro.established_title = "Established in 2021"
        intro.established_text = "Specializing in IT training, placement, and custom software development in Surandai."
        intro.whoweare_heading = "Why Choose Our Training Programs"
        intro.whoweare_description = "We are a training centre that helps students learn IT skills. We also have our own IT startup where real software work is done. Along with training, we provide consultation services to guide students in career and job-related matters."
        intro.howitworks_heading = "How Our Training Works"
        intro.howitworks_subtext = "Follow our proven 4-step journey to transform from a beginner into an industry-ready tech professional."
        intro.projects_heading = "Student Projects & Success Stories"
        intro.projects_subtext = "See what our students have built and achieved"
        intro.stories_heading = "Students success stories"
        intro.stories_subtext = "watch our latest students success stories.."
        intro.cta_heading = "Start your Learning Journey today!"
        intro.cta_subtext = "Get expert guidance, structured training, and real-world skills that prepare you for career success."
        intro.save()

        if not intro.hero_bg_image:
            if not attach_file(intro, "hero_bg_image", "home/hero-bg.png"):
                self.stdout.write(self.style.WARNING("  Hero bg image not found — upload manually."))
        if not intro.whoweare_image:
            if not attach_file(intro, "whoweare_image", "home/who-we-are.jpg"):
                self.stdout.write(self.style.WARNING("  Who We Are image not found — upload manually."))
        if not intro.whychoose_mascot_image:
            if not attach_file(intro, "whychoose_mascot_image", "home/mascot.png"):
                self.stdout.write(self.style.WARNING("  Mascot image not found — upload manually."))
        if not intro.cta_mascot_image:
            if not attach_file(intro, "cta_mascot_image", "home/mascot-cta.png"):
                self.stdout.write(self.style.WARNING("  CTA mascot image not found — upload manually."))
        self.stdout.write(self.style.SUCCESS("Home Intro saved."))

        # --- Benefits ---
        if not HomeBenefit.objects.exists():
            for order, (icon_name, title, desc) in enumerate(BENEFITS):
                HomeBenefit.objects.create(icon_name=icon_name, title=title, description=desc, order=order)
            self.stdout.write(self.style.SUCCESS(f"Imported {len(BENEFITS)} benefits."))
        else:
            self.stdout.write(self.style.WARNING("Benefits already exist — skipping."))

        # --- Steps ---
        if not HomeStep.objects.exists():
            for order, (icon_path, title, desc, num) in enumerate(STEPS):
                step = HomeStep.objects.create(title=title, description=desc, step_number=num, order=order)
                if not attach_file(step, "icon", icon_path):
                    self.stdout.write(self.style.WARNING(f"  Icon not found for '{title}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(STEPS)} steps."))
        else:
            self.stdout.write(self.style.WARNING("Steps already exist — skipping."))

        # --- Projects ---
        if not HomeProject.objects.exists():
            for order, (image_path, title, author, tag, tall) in enumerate(PROJECTS):
                project = HomeProject.objects.create(title=title, author=author, tag=tag, tall=tall, order=order)
                if not attach_file(project, "image", image_path):
                    self.stdout.write(self.style.WARNING(f"  Image not found for '{title}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(PROJECTS)} projects."))
        else:
            self.stdout.write(self.style.WARNING("Projects already exist — skipping."))

        # --- Stories (image + video) ---
        if not HomeStory.objects.exists():
            for order, (image_path, video_path, name, role) in enumerate(STORIES):
                story = HomeStory.objects.create(name=name, role=role, order=order)
                if not attach_file(story, "image", image_path):
                    self.stdout.write(self.style.WARNING(f"  Image not found for '{name}' — upload manually."))
                if not attach_file(story, "video", video_path):
                    self.stdout.write(self.style.WARNING(f"  Video not found for '{name}' — upload manually."))
            self.stdout.write(self.style.SUCCESS(f"Imported {len(STORIES)} stories."))
        else:
            self.stdout.write(self.style.WARNING("Stories already exist — skipping."))

        self.stdout.write(self.style.SUCCESS("Done."))