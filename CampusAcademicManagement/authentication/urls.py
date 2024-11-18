from django.urls import path
from . import views
from .views import login_view, home_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("home/", home_view, name="home"),
    path("student/home/", views.student_home, name="student_home"),
    path("student/profile/", views.student_profile_view, name="student_profile"),
]
