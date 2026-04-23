from django.db import models
from django.contrib.auth.models import User


class ResumeAnalysis(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    resume_file = models.FileField(upload_to="resumes/")

    job_description = models.TextField(blank=True)

    ats_score = models.IntegerField(default=0)

    skill_score = models.IntegerField(default=0)

    keyword_score = models.IntegerField(default=0)

    semantic_score = models.IntegerField(default=0)

    impact_score = models.IntegerField(default=0)

    section_score = models.IntegerField(default=0)

    # ✅ Added fields (fixes your error)
    responsibility_score = models.IntegerField(default=0)

    job_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ATS Score {self.ats_score}"


class Resume(models.Model):

    TEMPLATE_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('two_column', 'Two Column'),
        ('minimal', 'Minimal'),
        ('professional', 'Professional'),
    ]

    # Basic Info
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200, blank=True, null=True)

    # Optional Links
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    other_url = models.URLField(blank=True, null=True)

    # Resume Sections
    summary = models.TextField()
    experience = models.TextField()
    skills = models.TextField()
    education = models.TextField()
    projects = models.TextField(blank=True, null=True)
    strengths = models.TextField(blank=True, null=True)

    # Photo optional
    photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True)

    # Template selected
    template_choice = models.CharField(
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default="modern"
    )