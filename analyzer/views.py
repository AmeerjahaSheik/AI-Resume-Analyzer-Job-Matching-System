
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ResumeAnalysis, Resume

import PyPDF2
from docx import Document
import string
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ================= BASIC PAGES =================

def landing(request):
    return render(request, "landing.html")


def how_it_works(request):
    return render(request, "how_it_works.html")


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect("analyzer:dashboard")

        messages.error(request, "Invalid email or password")

    return render(request, "login.html")


def register_view(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("analyzer:register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name
        )

        login(request, user)
        return redirect("analyzer:dashboard")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("analyzer:landing")


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")


@login_required
def results(request):
    return render(request, "results.html")


@login_required
def intro(request):
    return render(request, "intro.html")


@login_required
def templates(request):
    return render(request, "templates.html")


@login_required
def resume_templates(request):
    return render(request, "templates.html")


@login_required
def resume_preview(request):
    return render(request, "resume_preview.html")


@login_required
def build_resume(request, id):
    return render(request, "resume_builder.html", {"template_id": id})


@login_required
def generate_resume(request, id):

    if request.method == "POST":

        context = {

            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "location": request.POST.get("location"),

            "summary": request.POST.get("summary"),

            "degree1": request.POST.get("degree1"),
            "college1": request.POST.get("college1"),
            "year1": request.POST.get("year1"),

            "degree2": request.POST.get("degree2"),
            "college2": request.POST.get("college2"),
            "year2": request.POST.get("year2"),

            "degree3": request.POST.get("degree3"),
            "college3": request.POST.get("college3"),
            "year3": request.POST.get("year3"),

            "skills": request.POST.get("skills"),

            "project_title": request.POST.get("project_title"),
            "project_description": request.POST.get("project_description"),
            "project_platform": request.POST.get("project_platform"),

            "job_title": request.POST.get("job_title"),
            "company": request.POST.get("company"),
            "job_duration": request.POST.get("job_duration"),
            "job_location": request.POST.get("job_location"),

            "exp1": request.POST.get("exp1"),
            "exp2": request.POST.get("exp2"),
            "exp3": request.POST.get("exp3"),

            "certifications": request.POST.get("certifications"),

            "linkedin": request.POST.get("linkedin"),
            "github": request.POST.get("github"),
        }

        template_file = f"resume_templates/template{id}.html"

        return render(request, template_file, context)

    return redirect("analyzer:dashboard")
# ================= TEXT EXTRACTION =================

def extract_text(file):

    text = ""

    if file.name.endswith(".pdf"):

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    elif file.name.endswith(".docx"):

        doc = Document(file)

        for para in doc.paragraphs:
            text += para.text

    return text.lower()


# ================= NLP PREPROCESS =================

def preprocess_text(text):

    text = text.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words("english"))

    tokens = [w for w in tokens if w not in stop_words]

    lemmatizer = WordNetLemmatizer()

    tokens = [lemmatizer.lemmatize(w) for w in tokens]

    return tokens


# ================= KEYWORD EXTRACTION =================

def extract_keywords(text, top_n=25):

    vectorizer = TfidfVectorizer(stop_words="english")

    matrix = vectorizer.fit_transform([text])

    feature_names = vectorizer.get_feature_names_out()

    scores = matrix.toarray()[0]

    word_scores = list(zip(feature_names, scores))

    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)

    keywords = [word for word, score in sorted_words[:top_n]]

    return set(keywords)


# ================= SECTION DETECTION =================

def detect_sections(text):

    sections = {
        "education": "education" in text,
        "experience": "experience" in text,
        "skills": "skills" in text,
        "projects": "project" in text,
        "certifications": "certification" in text
    }

    score = int((sum(sections.values()) / len(sections)) * 100)

    return score


# ================= SEMANTIC SIMILARITY =================

def calculate_semantic_similarity(resume_text, jd_text):

    sentences = [resume_text, jd_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf = vectorizer.fit_transform(sentences)

    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])

    return int(similarity[0][0] * 100)


# ================= ANALYZE RESUME =================

@login_required
def analyze_resume(request):

    if request.method == "POST":

        resume_file = request.FILES.get("resume")
        job_description = request.POST.get("job_description")
        career_level = request.POST.get("level")

        if not resume_file:
            messages.error(request, "Please upload a resume.")
            return redirect("analyzer:dashboard")

        # ================= TEXT EXTRACTION =================

        resume_text = extract_text(resume_file)
        tokens = preprocess_text(resume_text)

        resume_keywords = extract_keywords(resume_text, top_n=25)
        detected_skills = len(resume_keywords)

        # ================= SKILL SCORE =================

        expected_skills = {
            "entry": 10,
            "mid": 14,
            "professional": 18
        }.get(career_level, 12)

        skill_ratio = detected_skills / (detected_skills + expected_skills)
        skill_score = int(skill_ratio * 100)
        skill_score = min(skill_score, 85)

        # ================= KEYWORD / STRUCTURE SCORE =================

        keyword_score = detect_sections(resume_text)
        keyword_score = min(keyword_score, 85)

        # ================= IMPACT SCORE =================

        numbers = [t for t in tokens if re.search(r"\d+", t)]
        action_words = [t for t in tokens if t.endswith("ed")]

        impact_score = len(numbers) * 5 + len(action_words) * 2
        impact_score = min(impact_score, 80)

        # ================= ATS SCORE (ONLY RESUME BASED) =================

        weights = {
            "entry": (0.45, 0.30, 0.25),
            "mid": (0.40, 0.30, 0.30),
            "professional": (0.35, 0.30, 0.35)
        }.get(career_level, (0.40, 0.30, 0.30))

        ats_score = (
            skill_score * weights[0] +
            keyword_score * weights[1] +
            impact_score * weights[2]
        )

        ats_score = int(min(ats_score, 90))

        # ================= JOB MATCHING =================

        semantic_score = 0
        job_score = 0

        skill_alignment = 0
        experience_alignment = 0
        responsibility_alignment = 0

        jd_keywords = set()
        missing_keywords = []

        if job_description:

            jd_text = job_description.lower()
            jd_tokens = preprocess_text(jd_text)

            jd_keywords = set(jd_tokens)

            semantic_score = calculate_semantic_similarity(resume_text, jd_text)

            resume_token_set = set(tokens)

            matched_terms = resume_token_set.intersection(jd_keywords)
            missing_keywords = jd_keywords - resume_token_set

            skill_alignment = int((len(matched_terms) / max(len(jd_keywords), 1)) * 100)

            experience_alignment = semantic_score

            responsibility_alignment = int(
                (skill_alignment + experience_alignment) / 2
            )

            job_score = int(
                semantic_score * 0.7 +
                skill_score * 0.3
            )

            job_score = min(job_score, 90)

        # ================= DYNAMIC SUGGESTION ENGINE =================

        ai_feedback = []

        # -------- SKILL GAP ANALYSIS --------

        skill_gap_terms = list(missing_keywords)[:5]

        if skill_gap_terms:
            ai_feedback.append(
                "Some technologies and skills referenced in the job description "
                f"do not appear clearly in the resume such as {', '.join(skill_gap_terms)}. "
                "Incorporating relevant tools, frameworks, or technologies used in your projects "
                "can strengthen skill alignment."
            )

        # -------- SECTION GAP ANALYSIS --------

        detected_sections = []

        if "skills" in resume_text:
            detected_sections.append("skills")
        if "project" in resume_text:
            detected_sections.append("projects")
        if "experience" in resume_text:
            detected_sections.append("experience")
        if "education" in resume_text:
            detected_sections.append("education")
        if "certification" in resume_text:
            detected_sections.append("certifications")

        missing_sections = {
            "skills", "projects", "experience", "education", "certifications"
        } - set(detected_sections)

        if missing_sections:
            ai_feedback.append(
                "The resume structure could be strengthened by clearly defining sections such as "
                f"{', '.join(list(missing_sections)[:3])}. Structured sections help ATS systems "
                "identify relevant information more effectively."
            )

        # -------- IMPACT GAP ANALYSIS --------

        if len(numbers) < 3:
            ai_feedback.append(
                "Project and experience descriptions contain limited measurable outcomes. "
                "Including metrics such as performance improvements, user growth, dataset sizes, "
                "or efficiency gains can significantly strengthen impact."
            )

        # -------- JOB RESPONSIBILITY GAP --------

        if job_description and responsibility_alignment < 70:

            jd_sentences = job_description.split(".")
            key_responsibilities = jd_sentences[:3]

            ai_feedback.append(
                "The job description highlights responsibilities such as "
                f"{', '.join([s.strip() for s in key_responsibilities if s][:2])}. "
                "Reflecting similar responsibilities or related technical contributions "
                "in project descriptions can improve role alignment."
            )

        # -------- EXPERIENCE GAP --------

        if job_description and experience_alignment < 60:

            ai_feedback.append(
                "The job description emphasizes collaborative software development "
                "and enterprise application development. Expanding descriptions of "
                "team collaboration, debugging activities, or system design decisions "
                "can improve experience alignment."
            )

        # -------- ENSURE MINIMUM FEEDBACK --------

        if len(ai_feedback) < 3:
            ai_feedback.append(
                "The resume demonstrates solid technical foundations. Further improvements "
                "can be achieved by refining project explanations and highlighting "
                "technical decision-making during development."
            )

        # ================= SAVE RESULT =================

        ResumeAnalysis.objects.create(
            user=request.user,
            resume_file=resume_file,
            job_description=job_description,
            ats_score=ats_score,
            skill_score=skill_score,
            keyword_score=keyword_score,
            semantic_score=semantic_score,
            impact_score=impact_score,
            section_score=keyword_score,
            job_score=job_score
        )

        return render(request, "results.html", {

            "skill_score": skill_score,
            "keyword_score": keyword_score,
            "impact_score": impact_score,
            "ats_score": ats_score,

            "job_score": job_score,
            "semantic_score": semantic_score,

            "skill_alignment": skill_alignment,
            "experience_alignment": experience_alignment,
            "responsibility_alignment": responsibility_alignment,

            "ai_feedback": ai_feedback
        })

    return redirect("analyzer:dashboard")