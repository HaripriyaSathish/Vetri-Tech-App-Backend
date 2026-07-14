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
    

# ============ ABOUT PAGE ============

class AboutIntro(models.Model):
    """Singleton — Hero, Story, Mascot, and CTA sections (each 'one of a kind'
    on the About page, unlike the list-based sections below)."""

    hero_title = models.CharField(
        max_length=255,
        default="About Vetri Training – Online IT Courses with Placement Support",
    )
    hero_subtitle = models.TextField(
        default="Empowering the next generation of IT Professionals with foundational knowledge and industry-ready skills"
    )

    story_heading = models.CharField(max_length=255, default="Our Story – Building Job-Oriented Training Programs")
    story_paragraph1 = models.TextField(
        default="VTS was founded with a simple observation — many learners struggle to enter the IT industry not due to lack of talent, but because they lack practical exposure, confidence, and guided direction."
    )
    story_paragraph2 = models.TextField(
        default="We built Vetri Technology Solutions to bridge this gap through structured training, real-time collaboration, and a strong learning ecosystem."
    )
    story_image = models.ImageField(upload_to="site/about/", blank=True, null=True)

    mascot_image = models.ImageField(upload_to="site/about/", blank=True, null=True)

    cta_title = models.CharField(max_length=255, default="Ready to Start Your Career")
    cta_body = models.TextField(
        default="Direct placement support and interview opportunities at our integrated IT startup ecosystem. Start your career with confidence!"
    )
    cta_avatar = models.ImageField(upload_to="site/about/", blank=True, null=True)

    class Meta:
        verbose_name = "About Intro (Hero/Story/Mascot/CTA)"
        verbose_name_plural = "About Intro (Hero/Story/Mascot/CTA)"

    def __str__(self):
        return "About Intro"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class MissionVisionCard(models.Model):
    icon = models.ImageField(upload_to="site/about/mission_vision/")
    title = models.CharField(max_length=100)  # "Mission" or "Vision"
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class EcosystemCard(models.Model):
    icon = models.ImageField(upload_to="site/about/ecosystem/")
    title = models.CharField(max_length=150)
    # one bullet item per line, same pattern as course BenefitSection
    items_text = models.TextField(help_text="One item per line. Each line becomes one bullet point in the app.")
    site_url = models.URLField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def items(self):
        return [line.strip() for line in self.items_text.splitlines() if line.strip()]


class TrainingApproachCard(models.Model):
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:50]


class SkillItem(models.Model):
    # Ionicons name string (e.g. "chatbox-ellipses-outline") — NOT an image,
    # the app already knows how to render any Ionicons name from a string.
    icon_name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    items_text = models.TextField(help_text="One item per line. Each line becomes one bullet point in the app.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def items(self):
        return [line.strip() for line in self.items_text.splitlines() if line.strip()]


class JourneyStep(models.Model):
    icon = models.ImageField(upload_to="site/about/journey/")
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class EnrollItem(models.Model):
    icon = models.ImageField(upload_to="site/about/enroll/")
    title = models.CharField(max_length=150)
    # hexColor/arcColor stay hardcoded in the app, paired by this 'order' index
    # — they're a fixed design pattern, not editable content.
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ImpactStat(models.Model):
    target = models.FloatField()          # e.g. 8, 5000, 85, 4.8
    suffix = models.CharField(max_length=10, blank=True)   # "+", "%", "/5"
    decimals = models.PositiveIntegerField(default=0)      # 0 normally, 1 for "4.8"
    label = models.CharField(max_length=150)               # "Years of Excellence"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label    
    
from django.conf import settings
from cloudinary_storage.storage import VideoMediaCloudinaryStorage

# ============ HOME PAGE ============

class HomeIntro(models.Model):
    """Singleton — all 'one of a kind' text/image blocks on the Home page
    (Hero, Who We Are, Why Choose Us mascot, section headings, CTA)."""

    hero_title = models.CharField(max_length=255, default="IT Training, Internship & Career Support")
    hero_description = models.TextField(
        default="This platform is designed for learners who want to build practical IT skills through structured training programs. Along with training, learners are informed about available IT services and consultancy support."
    )
    hero_bg_image = models.ImageField(upload_to="site/home/", blank=True, null=True)

    whoweare_image = models.ImageField(upload_to="site/home/", blank=True, null=True)
    established_title = models.CharField(max_length=150, default="Established in 2021")
    established_text = models.TextField(
        default="Specializing in IT training, placement, and custom software development in Surandai."
    )
    whoweare_heading = models.CharField(max_length=255, default="Why Choose Our Training Programs")
    whoweare_description = models.TextField(
        default="We are a training centre that helps students learn IT skills. We also have our own IT startup where real software work is done. Along with training, we provide consultation services to guide students in career and job-related matters."
    )

    whychoose_mascot_image = models.ImageField(upload_to="site/home/", blank=True, null=True)

    howitworks_heading = models.CharField(max_length=255, default="How Our Training Works")
    howitworks_subtext = models.TextField(
        default="Follow our proven 4-step journey to transform from a beginner into an industry-ready tech professional."
    )

    projects_heading = models.CharField(max_length=255, default="Student Projects & Success Stories")
    projects_subtext = models.CharField(max_length=255, default="See what our students have built and achieved")

    stories_heading = models.CharField(max_length=255, default="Students success stories")
    stories_subtext = models.CharField(max_length=255, default="watch our latest students success stories..")

    cta_heading = models.CharField(max_length=255, default="Start your Learning Journey today!")
    cta_subtext = models.TextField(
        default="Get expert guidance, structured training, and real-world skills that prepare you for career success."
    )
    cta_mascot_image = models.ImageField(upload_to="site/home/", blank=True, null=True)

    class Meta:
        verbose_name = "Home Intro (Hero/WhoWeAre/Headings/CTA)"
        verbose_name_plural = "Home Intro (Hero/WhoWeAre/Headings/CTA)"

    def __str__(self):
        return "Home Intro"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HomeBenefit(models.Model):
    # Ionicons name string, e.g. "people", "videocam" — NOT an image
    icon_name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class HomeStep(models.Model):
    # "How Our Training Works" steps — Register, Attend, Practice, Certificate
    icon = models.ImageField(upload_to="site/home/steps/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    # step number badge (1, 2, 3, 4) shown big/faded in the corner — kept as
    # its own field rather than order+1, in case a step is ever inserted
    # without renumbering everything else
    step_number = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class HomeProject(models.Model):
    image = models.ImageField(upload_to="site/home/projects/")
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    tag = models.CharField(max_length=100)
    tall = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class HomeStory(models.Model):
    image = models.ImageField(upload_to="site/home/stories/")
    # IMPORTANT: videos must use VideoMediaCloudinaryStorage, not the default
    # image storage — same class of issue as the PDF/raw-file fix earlier.
    # Using the wrong storage class here would misconfigure the resource
    # type on Cloudinary and could break playback.
    video = models.FileField(
        upload_to="site/home/stories/",
        storage=VideoMediaCloudinaryStorage() if settings.IS_PRODUCTION else None,
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name    