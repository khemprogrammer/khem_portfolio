from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
]