from django.urls import path
from . import views
from .views import login_view, home_view

urlpatterns = [
    path("", login_view, name="login"),
    path("home/", home_view, name="home"),
    path("student/home/", views.student_home, name="student_home"),
    path("student/profile/", views.student_profile_view, name="student_profile"),
    path("announcements/", views.announcements_list, name="announcements"),
    path("event_registration/", views.event_registration, name="event_registration"),
    path("suggestions/", views.suggestion_view, name="suggestion"),
    path("clubs/", views.clubs_page, name="clubs"),
    path("admin_anits/home/", views.admin_home, name="admin_home"),
    path("club/", views.admin_club, name="admin_club"),
    path("feedback/", views.feedback_page, name="feedback_page"),
    path('add_student/', views.add_student_information, name='add_student_information'),
]
