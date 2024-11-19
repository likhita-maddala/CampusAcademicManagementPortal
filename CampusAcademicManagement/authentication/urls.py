from django.urls import path
from . import views
from .views import login_view, home_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("home/", home_view, name="home"),
    path("student/home/", views.student_home, name="student_home"),
    path("student/profile/", views.student_profile_view, name="student_profile"),
    path("announcements/", views.announcements_list, name="announcements"),
    path("event_registration/", views.event_registration, name="event_registration"),
    path("suggestions/", views.suggestion_view, name="suggestion"),
    path("clubs/", views.clubs_page, name="clubs"),
]
