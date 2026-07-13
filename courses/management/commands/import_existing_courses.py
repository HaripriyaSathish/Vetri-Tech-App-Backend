"""
One-time import of your existing coursesData.ts content into the database.

Run this AFTER `python manage.py migrate`, and only once (it uses
get_or_create so re-running is safe, but there's no reason to).

    python manage.py import_existing_courses

IMAGES: this script will try to find and upload the actual image files
(course covers, tool icons, brochure PDFs) IF you set ASSETS_DIR below to
point at your React Native app's `assets` folder on this machine. If it
can't find a file, it just skips it and prints a warning — you can then
upload that one image manually through Django Admin afterward. Text data
(titles, descriptions, tools, benefits, FAQs) is always imported fully
regardless of whether images are found.
"""

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from courses.models import Course, Tool, BenefitSection, Faq

# Point this at the `assets` folder inside your Vetri Tech mobile app project,
# e.g. r"C:\Users\you\vetri-tech-app\assets" or "/Users/you/vetri-tech-app/assets"
# Leave as None to skip all image uploads and just import text data.
ASSETS_DIR = r"C:\Vetri Tech Mobile App\vetri-tech-app\assets"


def resolve_asset(relative_path):
    """relative_path like 'images/course-data-analysis.png' or 'icons/tools/python.jpg'"""
    if not ASSETS_DIR:
        return None
    full_path = os.path.join(ASSETS_DIR, relative_path)
    if os.path.isfile(full_path):
        return full_path
    return None


def attach_file(model_instance, field_name, relative_path):
    path = resolve_asset(relative_path)
    if not path:
        return False
    with open(path, "rb") as f:
        getattr(model_instance, field_name).save(
            os.path.basename(path), File(f), save=True
        )
    return True


COURSES_DATA = [
    {
        "id": "data-analysis",
        "image_path": "images/course-data-analysis.png",
        "title": "Gen AI Data Analysis Training",
        "duration": "3 Months",
        "highlight": "Hands-on Data Analytics Training with AI Tools",
        "description": "Learn Gen AI Data Analysis using Python, SQL, and visualization tools with real-world datasets.",
        "overview": "This GEN AI Data Analysis Training focuses on transforming raw data into meaningful insights using Python, SQL, and visualization tools. Learn data cleaning, analysis, and visualization using real-world datasets. Gain exposure to machine learning concepts used in business decision-making.",
        "category": "Data",
        "brochure_path": "brochures/data-analysis.pdf",
        "order": 1,
        "tools": [
            ("Python", "icons/tools/python.jpg"),
            ("SQL", "icons/tools/sql.png"),
            ("Azure SQL", "icons/tools/azure-sql.jpg"),
            ("Snowflake", "icons/tools/snowflake.png"),
            ("Databricks", "icons/tools/databricks.png"),
            ("Qlik", "icons/tools/qlik.png"),
            ("Excel", "icons/tools/excel.jpg"),
            ("Power BI", "icons/tools/power-bi.png"),
            ("Tableau", "icons/tools/tableau.png"),
            ("Knime Analytics", "icons/tools/knime-analytics.png"),
            ("ChatGPT", "icons/tools/chatgpt.png"),
            ("Gemini", "icons/tools/gemini.png"),
            ("Julius", "icons/tools/julius.jpg"),
            ("Chat2DB", "icons/tools/chat2db.png"),
            ("Vanna.AI", "icons/tools/vanna-ai.png"),
            ("Text2Sql", "icons/tools/text2sql.png"),
            ("Google Collab AI", "icons/tools/google-collab-ai.jpg"),
            ("Pandas", "icons/tools/pandas.png"),
            ("Ydata Profiling", "icons/tools/ydata-profiling.png"),
            ("Visuals Microsoft Clarity", "icons/tools/visuals-microsoft-clarity.jpg"),
            ("Claude", "icons/tools/claude.jpg"),
            ("Databrick Assistant", "icons/tools/databrick-assistant.jpg"),
            ("Copilot", "icons/tools/copilot.jpg"),
            ("Dbeaverai", "icons/tools/dbeaverai.jpg"),
            ("H2o.ai", "icons/tools/h2o-ai.png"),
        ],
        "benefits": [
            ("Skills You Will Gain in AI Data Analysis", [
                "Master data cleaning and preprocessing techniques",
                "Perform Exploratory Data Analysis (EDA) on real datasets",
                "Create powerful visualizations using charts and dashboards",
                "Write SQL queries to extract and manage data",
                "Work with Python libraries like Pandas and NumPy",
                "Understand machine learning basics for data-driven decisions",
                "Analyze business problems using real-world data",
            ]),
            ("Key Benefits of AI Data Analysis Course", [
                "Gain hands-on experience with real-world datasets",
                "Build a job-ready portfolio with industry-level projects",
                "Learn tools and techniques used by data professionals",
                "Develop strong analytical and problem-solving skills",
                "Understand how data is used in real business scenarios",
            ]),
            ("Career Opportunities in Full Stack Development", [
                "Data Analyst", "Business Analyst", "Junior Data Scientist",
            ]),
            ("Who Can Join This Course", [
                "Students and freshers", "Non-IT learners", "Career switchers",
            ]),
            ("Why Choose Vetri Technology Solutions", [
                "90% practical training with real-time implementation",
                "7+ industry-level projects for hands-on experience",
                "Integrated internship for real-world exposure",
                "One-on-one mentorship for personalized guidance",
                "3+ mock interviews for job preparation",
                "Free Internship Certificate & Free Premium Job Portal Access",
                "Resume building and interview support",
                "Certification upon course completion",
            ]),
        ],
        "faqs": [
            ("Do I need Prior Coding knowledge?", "No, this AI Data Analysis course is beginner friendly. you can start without prior Coding/Analysis experience."),
            ("I am an NON IT Candidate, Can I Join this Training ?", "Yes, any Non IT and IT Background candidates can Join this Program."),
            ("Is internship included in this Training Program?", "Yes, 2 Months of Free WFH Integrated Internship is Included for all the Candidates in the Batch."),
            ("Any Additional Fees to be Paid for the 2 Months WFH Internship?", "No, The Internship is Free of Cost from our Own IT Startup VETRI IT SYSTEMS Private Limited worth of ₹6,000."),
            ("Do I learn Gen AI Tools?", "Yes, you will learn Gen AI Tools in this Training."),
            ("Is it Live Classes or Recorded Sessions?", "All the Trainings will happen Daily Live Online via Microsoft Teams (Monday to Friday), The recordings will also be provided post daily Live Session."),
            ("Do I get Course Completion & Internship Certificate ?", "Yes, Successfully completing the Candidates will get Both Course Completion Certificate & Internship Certificate."),
            ("Any Additional Fees to be Paid for the Placement Support ?", "No, The Placement Guidance is Completely free!!! It will be Provided by our Own Consultancy - Vetri Consultancy Services. A Vetri Job Portal Premium Access worth of ₹5,000 also will also be Provided for the Free of Cost only for VTS Trainees."),
            ("What is the Eligibility to Join the Training Programs ?", "Any Degree Candidates below 40 age Females are Eligible. You need to Share your resume - A First Level of Interview will be conducted - Based on your Performance you will get the seat for this Program."),
            ("Can I visit the Office Directly ? Where is the Office Located ?", "Yes, the Office is located in Two Places 1.VTS & VIS,April's Complex, Shanthi Complex, Surandai - 627859, Tenkasi District 2.VTS & VIS, Murali's Tower, Opposite VOC Stadium, Palyamkottai, Tirunelveli-627002 Office Timings - 10.00 AM to 05.00 PM (Monday to Saturday - Excluding Public Holidays)"),
        ],
    },
    {
        "id": "python-fullstack",
        "image_path": "images/course-python-fullstack.png",
        "title": "Gen AI Python FullStack Development & AI Mobile App Development Training with Internship",
        "duration": "3 Months",
        "highlight": "Build Real Web Applications with AI",
        "description": "Learn AI Python FullStack Development with hands-on training in frontend and backend technologies. Build real-world web applications using Python, Django, and modern tools with practical project experience.",
        "overview": "This Gen AI Python FullStack Training focuses on building complete Web & Mobile Applications from frontend to backend. Learn UI development, backend logic using Django, and database integration through real-time projects and practical implementation.",
        "category": "Development",
        "brochure_path": "brochures/python-fullstack.pdf",
        "order": 2,
        "tools": [
            ("HTML", "icons/tools/html.png"),
            ("CSS", "icons/tools/css.png"),
            ("JavaScript", "icons/tools/javascript.png"),
            ("Python", "icons/tools/python.jpg"),
            ("Django", "icons/tools/django.png"),
            ("ReactJS", "icons/tools/reactjs.png"),
            ("React Native", "icons/tools/react-native.png"),
            ("MySQL", "icons/tools/mysql.png"),
            ("PostgreSQL", "icons/tools/postgresql.png"),
            ("MongoDB", "icons/tools/mongodb.png"),
            ("Bootstrap", "icons/tools/bootstrap.png"),
            ("Git", "icons/tools/git.png"),
            ("Django REST Framework", "icons/tools/django-rest-framework.png"),
            ("Postman", "icons/tools/postman.png"),
            ("NumPy", "icons/tools/numpy.png"),
            ("Pandas", "icons/tools/pandas.png"),
            ("Scikit-learn", "icons/tools/scikit-learn.png"),
            ("TensorFlow", "icons/tools/tensorflow.png"),
            ("Hugging Face", "icons/tools/hugging-face.png"),
            ("FAISS", "icons/tools/faiss.png"),
            ("ChromaDB", "icons/tools/chromadb.png"),
            ("Docker", "icons/tools/docker.png"),
            ("Linux", "icons/tools/linux.png"),
            ("AWS EC2", "icons/tools/aws-ec2.png"),
            ("Cursor AI", "icons/tools/cursor-ai.png"),
            ("GitHub Copilot", "icons/tools/copilot.jpg"),
            ("v0.dev", "icons/tools/v0-dev.png"),
            ("Expo AI", "icons/tools/expo-ai.png"),
            ("Android Studio", "icons/tools/android-studio.png"),
            ("Gemini", "icons/tools/gemini.png"),
            ("Amazon Q Developer", "icons/tools/amazon-q-developer.png"),
            ("Prisma AI", "icons/tools/prisma-ai.png"),
            ("MongoDB Atlas AI", "icons/tools/mongodb-atlas-ai.png"),
            ("Swagger AI", "icons/tools/swagger-ai.png"),
            ("TensorFlow Google Colab", "icons/tools/tensorflow-google-colab.png"),
            ("Kaggle", "icons/tools/kaggle.png"),
            ("OpenAI", "icons/tools/openai.png"),
            ("Claude", "icons/tools/claude.jpg"),
            ("LangChain", "icons/tools/langchain.png"),
            ("LangGraph", "icons/tools/langgraph.png"),
            ("LlamaIndex", "icons/tools/llamaindex.png"),
            ("CrewAI", "icons/tools/crewai.png"),
            ("OpenAI Agents SDK", "icons/tools/openai-agents-sdk.png"),
            ("Tavily", "icons/tools/tavily.png"),
            ("Google Vertex AI", "icons/tools/google-vertex-ai.png"),
        ],
        "benefits": [
            ("Skills You Will Gain in Gen AI Python FullStack Development", [
                "Build responsive web pages using HTML, CSS, and JavaScript",
                "Develop backend applications using Python and Django",
                "Work with databases and perform CRUD operations",
                "Understand REST APIs and application integration",
                "Use Git for version control and project management",
                "Deploy applications and understand hosting basics",
                "Build Mobile Apps with AI Tools",
                "Build Real World AI Tools",
            ]),
            ("Key Benefits of Python FullStack Development Course", [
                "Gain Hands-On Experience in FullStack Development",
                "Build Real-World Web & Mobile Applications for your Portfolio",
                "Learn Both Frontend,Backend Technologies, Mobile App Development & Buiiing AI Tools in one Training",
                "Understand Real Development Workflows and AI Tools",
                "Improve Coding and Problem-Solving Skills",
            ]),
            ("Career Opportunities in Python FullStack Development", [
                "Full Stack Developer", "Python Developer", "Backend Developer",
                "Web Application Developer", "Gen AI Developer", "AI Mobile App Developer",
            ]),
            ("Who Can Join This Training & Internship Program", [
                "Students and Freshers interested in AI & Web Development",
                "Beginners with No Coding Experience",
                "Career switchers into IT field",
                "Career Gap Candidates",
            ]),
            ("Why Choose Vetri Technology Solutions", [
                "Free Work From Home Internship",
                "Free Paid Internship Opportunities for Top Performers - After Interview",
                "90% Practical Training with Real-Time Implementation",
                "10+ Industry-level Projects For Hands-On Experience",
                "Integrated Product Internship for Real-World exposure",
                "One-On-One Mentorship for Personalized Guidance",
                "3+ Mock Interviews For Job Preparation",
                "Free Internship Certificate & Free Premium Job Portal Access",
                # NOTE: source data had an incomplete final bullet here
                # ("Resume Building and..." was cut off) — edit this section
                # in Django Admin to add the missing text once you know it.
            ]),
        ],
        "faqs": [
            ("Do I Need Prior Coding Knowledge to Join this Training?", "No, this Gen AI Python FullStack Training is Beginner Friendly. You can Start without Prior Coding Experience."),
            ("How Many Projects Do I Build in this Training ?", "You will build Real World applications - 7 FullStack Applications, 3 Mobile Apps, 1 Generative AI Tool & 1 Agentic AI Tool in this Training Program."),
            ("What Technologies & AI Tools will I learn in this Training?", "HTML, CSS, JavaScript, Python, Django, ReactJS, React Native, MySQL, PostgreSQL, MongoDB, Bootstrap, Git, Django REST Framework, Postman, NumPy, Pandas, Scikit-learn, TensorFlow, Hugging Face, FAISS, ChromaDB, Docker, Linux, AWS EC2, Cursor AI, GitHub Copilot, v0.dev, Expo AI, Android Studio, Gemini, Amazon Q Developer, Prisma AI, MongoDB Atlas AI, Swagger AI, TensorFlow Google Colab, Kaggle, OpenAI, Claude, LangChain, LangGraph, LlamaIndex, CrewAI, OpenAI Agents SDK, Tavily, Google Vertex AI"),
            ("Do I need to Pay Additional Fees for WFH Internships ?", "Integrated WFH Internship will be Offered for 2 Months Worth ₹6,000 is free for all Candidates. The Paid Internship will be Offered for the Top-Performing Students based on their Performance during the Training & Clearing the Projects Interviews."),
            ("Do I Create any AI Tool in this Program?", "Yes, Two AI Tools will get created by the Candidates - One Generative AI Tool & One Agentic AI Tool that will assist in the coding."),
            ("Do I get any Placement Support ?", "Yes, All Trainees are eligible to get the Placement Support Portal from Vetri Placment Solutions. The Portal Access will be provided for the lifetime along with the Placement Guidance."),
            ("I am an NON IT Candidate, Can I Join this Training ?", "Yes, any Non IT and IT Background candidates can Join this Program."),
            ("Is it Live Classes or Recorded Sessions?", "All the Trainings will happen Daily Live Online via Microsoft Teams (Monday to Friday), The recordings will also be provided post daily Live Session."),
            ("Do I get Course Completion & Internship Certificate ?", "Yes, Successfully completing the Candidates will get Both Course Completion Certificate & Internship Certificate."),
            ("Any Additional Fees to be Paid for the Placement Support ?", "No, The Placement Guidance is Completely free!!! It will be Provided by our Own Consultancy - Vetri Consultancy Services. A Vetri Job Portal Premium Access worth of ₹5,000 also will also be Provided for the Free of Cost only for VTS Trainees."),
            ("What is the Eligibility to Join the Training Programs ?", "Any Degree Candidates below 40 Age Females & Below 30 Age Males are Eligible."),
            ("Can I visit the Office Directly ? Where is the Office Located ?", "Yes, the Office is located in Two Places 1.VTS & VIS,April's Complex, Shanthi Complex, Surandai - 627859, Tenkasi District 2.VTS & VIS, Murali's Tower, Opposite VOC Stadium, Palyamkottai, Tirunelveli-627002 Office Timings - 10.00 AM to 05.00 PM (Monday to Saturday - Excluding Public Holidays)"),
        ],
    },
    {
        "id": "digital-marketing",
        "image_path": "images/course-digital-marketing.png",
        "title": "GEN AI Digital Marketing Training with Internship",
        "duration": "3 Months",
        "highlight": "Master SEO & Paid Advertising With AI",
        "description": "Learn GEN AI Digital Marketing with hands-on training in SEO, social media, and paid advertising. Work on real campaigns, use modern AI tools, and build practical marketing skills through projects and internship experience.",
        "overview": "",  # was empty in source data too — fill in via admin if needed
        "category": "Emerging Tech",
        "brochure_path": "brochures/digital-marketing.pdf",
        "order": 3,
        "tools": [
            ("WordPress", "icons/tools/wordpress.png"),
            ("Google search console", "icons/tools/google-search-console.png"),
            ("Google Business Profile", "icons/tools/google-business-profile.png"),
            ("AnswerThePublic", "icons/tools/answerthepublic.png"),
            ("Screaming Frog", "icons/tools/screaming-frog.png"),
            ("GTMetrix", "icons/tools/gtmetrix.png"),
            ("Surfer SEO", "icons/tools/surfer-seo.png"),
            ("Frase.io", "icons/tools/frase-io.png"),
            ("MarketMuse", "icons/tools/marketmuse.png"),
            ("Semrush AI", "icons/tools/semrush-ai.png"),
            ("Meta Business suite", "icons/tools/meta-business-suite.png"),
            ("QuillBot", "icons/tools/quillbot.png"),
            ("Jasper.ai", "icons/tools/jasper-ai.png"),
            ("Copy.ai", "icons/tools/copy-ai.png"),
            ("Pictory.ai", "icons/tools/pictory-ai.png"),
            ("Synthesia", "icons/tools/synthesia.png"),
            ("Lumen5", "icons/tools/lumen5.png"),
            ("Perplexity", "icons/tools/perplexity.png"),
            ("Figma", "icons/tools/figma.png"),
            ("Canva AI", "icons/tools/canva-ai.png"),
            ("Adobe Firefly", "icons/tools/adobe-firefly.png"),
            ("Predis.ai", "icons/tools/predis-ai.png"),
            ("Ocoya", "icons/tools/ocoya.png"),
            ("Hootsuite AI", "icons/tools/hootsuite-ai.png"),
            ("SocialBee AI", "icons/tools/socialbee-ai.png"),
            ("Linktree", "icons/tools/linktree.png"),
            ("Mailchimp", "icons/tools/mailchimp.png"),
            ("Persado", "icons/tools/persado.png"),
            ("Phrasee", "icons/tools/phrasee.png"),
            ("AdCreative.ai", "icons/tools/adcreative-ai.png"),
            ("Madgicx", "icons/tools/madgicx.png"),
            ("Google Analytics", "icons/tools/google-analytics.png"),
            ("Hotjar", "icons/tools/hotjar.png"),
            ("Microsoft Clarity", "icons/tools/visuals-microsoft-clarity.jpg"),
            ("Exploding Topics & Glimpse AI", "icons/tools/exploding-topics-glimpse-ai.png"),
            ("Drift", "icons/tools/drift.png"),
            ("ManyChat", "icons/tools/manychat.png"),
        ],
        "benefits": [
            ("Skills You Will Gain in Digital Marketing", [
                "Understand SEO fundamentals and keyword research",
                "Create and manage Google Ads and social media campaigns",
                "Learn content marketing and copywriting strategies",
                "Analyze campaign performance using analytics tools",
                "Use AI tools for content creation and automation",
                "Build complete digital marketing strategies",
            ]),
            ("Key Benefits of Digital Marketing Course", [
                "Gain hands-on experience with real marketing campaigns",
                "Build practical knowledge in SEO and paid advertising",
                "Learn industry tools used by digital marketers",
                "Develop analytical and strategic thinking skills",
                "Create a strong portfolio with real campaign experience",
            ]),
            ("Career Opportunities in Digital Marketing", [
                "Digital Marketing Executive", "SEO Specialist", "Social Media Manager",
                "Performance Marketer", "Content Strategist",
            ]),
            ("Who Can Join This Course", [
                "Students and freshers interested in marketing",
                "Business owners who want to grow online",
                "Career switchers into digital marketing",
                "Anyone interested in online marketing skills",
            ]),
            ("Why Choose Vetri Technology Solutions", [
                "90% practical training with real-time implementation",
                "7+ industry-level projects for hands-on experience",
                "Integrated internship for real-world exposure",
                "One-on-one mentorship for personalized guidance",
                "3+ mock interviews for job preparation",
                "Free Internship Certificate & Free Premium Job Portal Access",
                "Resume building and interview support",
                "Certification upon course completion",
            ]),
        ],
        "faqs": [
            ("Do I need prior marketing knowledge?", "No, this Gen AI Digital Marketing course is beginner friendly. you can start without prior Marketing Knowledge/Experience."),
            ("I am an NON IT Candidate, Can I Join this Training ?", "Yes, any Non IT and IT Background candidates can Join this Program."),
            ("Is internship included in this Training Program?", "Yes, 2 Months of Free WFH Integrated Internship is Included for all the Candidates in the Batch."),
            ("Any Additional Fees to be Paid for the 2 Months WFH Internship?", "No, The Internship is Free of Cost from our Own IT Startup VETRI IT SYSTEMS Private Limited worth of ₹6,000."),
            ("Do I learn Gen AI Tools?", "Yes, You will Learn Gen AI Tools in the Training Period."),
            ("Is it Live Classes or Recorded Sessions ?", "All the Trainings will happen Daily Live Online via Microsoft Teams (Monday to Friday), The recordings will also be provided post daily Live Session."),
            ("Do I get Course Completion & Internship Certificate ?", "Yes, Successfully completing the Candidates will get Both Course Completion Certificate & Internship Certificate."),
            ("Any Additional Fees to be Paid for the Placement Support ?", "No, The Placement Guidance is Completely free!!! It will be Provided by our Own Consultancy - Vetri Consultancy Services. A Vetri Job Portal Premium Access worth of ₹5,000 also will also be Provided for the Free of Cost only for VTS Trainees."),
            ("What is the Eligibility to Join the Training Programs ?", "Any Degree Candidates below 40 age Females are Eligible."),
            ("Can I visit the Office Directly ? Where is the Office Located ?", "Yes, the Office is located in Two Places 1.VTS & VIS,April's Complex, Shanthi Complex, Surandai - 627859, Tenkasi District 2.VTS & VIS, Murali's Tower, Opposite VOC Stadium, Palyamkottai, Tirunelveli-627002 Office Timings - 10.00 AM to 05.00 PM (Monday to Saturday - Excluding Public Holidays)"),
        ],
    },
]


class Command(BaseCommand):
    help = "Imports the existing 3 hardcoded courses (from coursesData.ts) into the database."

    def handle(self, *args, **options):
        if not ASSETS_DIR:
            self.stdout.write(self.style.WARNING(
                "ASSETS_DIR is not set — all image/icon/brochure uploads will be skipped. "
                "Text data (titles, tools, benefits, FAQs) will still import fully. "
                "You can upload images manually afterward in Django Admin, or set "
                "ASSETS_DIR at the top of this file and re-run."
            ))

        for course_data in COURSES_DATA:
            course, created = Course.objects.get_or_create(
                id=course_data["id"],
                defaults={
                    "title": course_data["title"],
                    "duration": course_data["duration"],
                    "highlight": course_data["highlight"],
                    "description": course_data["description"],
                    "overview": course_data["overview"],
                    "category": course_data["category"],
                    "order": course_data["order"],
                },
            )

            if not created:
                self.stdout.write(self.style.WARNING(
                    f"Course '{course.id}' already exists — skipping (delete it in admin first to re-import)."
                ))
                continue

            image_ok = attach_file(course, "image", course_data["image_path"])
            if not image_ok:
                self.stdout.write(self.style.WARNING(f"  Cover image not found for '{course.id}' — upload manually."))

            if course_data.get("brochure_path"):
                brochure_ok = attach_file(course, "brochure_file", course_data["brochure_path"])
                if not brochure_ok:
                    self.stdout.write(self.style.WARNING(f"  Brochure PDF not found for '{course.id}' — upload manually."))

            for order, (name, icon_path) in enumerate(course_data["tools"]):
                tool = Tool.objects.create(course=course, name=name, order=order)
                icon_ok = attach_file(tool, "icon", icon_path)
                if not icon_ok:
                    self.stdout.write(self.style.WARNING(f"  Tool icon not found for '{name}' — upload manually."))

            for order, (title, items) in enumerate(course_data["benefits"]):
                BenefitSection.objects.create(
                    course=course, title=title, items_text="\n".join(items), order=order
                )

            for order, (question, answer) in enumerate(course_data["faqs"]):
                Faq.objects.create(course=course, question=question, answer=answer, order=order)

            self.stdout.write(self.style.SUCCESS(f"Imported course: {course.title}"))

        self.stdout.write(self.style.SUCCESS("Done. Check Django Admin to review the imported courses."))