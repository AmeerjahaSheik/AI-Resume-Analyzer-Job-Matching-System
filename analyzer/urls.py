from django.urls import path
from . import views

app_name = "analyzer"

urlpatterns = [

    path("", views.landing, name="landing"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("analyze/", views.analyze_resume, name="analyze_resume"),

    path("intro/", views.intro, name="intro"),
    path("templates/", views.templates, name="templates"),
    path("preview/", views.resume_preview, name="resume_preview"),
    

    

    path("build/<int:id>/", views.build_resume, name="build_resume"),

    path("generate/<int:id>/", views.generate_resume, name="generate_resume"),

]

