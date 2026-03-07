from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Profile, SkillCategory, Skill, Experience, Education, Stat
from projects.models import Project
from projects.github_api import GitHubAPI


class HomeView(TemplateView):
    template_name = 'portfolio/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['featured_skills'] = Skill.objects.filter(is_featured=True)[:6]
        context['stats'] = Stat.objects.filter(is_active=True)
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:3]
        context['recent_projects'] = Project.objects.all()[:6]
        
        # Fetch GitHub stats
        github = GitHubAPI()
        context['github_stats'] = github.get_user_stats()
        
        return context


class AboutView(TemplateView):
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['skill_categories'] = SkillCategory.objects.prefetch_related('skills')
        context['experiences'] = Experience.objects.all()
        context['education'] = Education.objects.all()
        context['stats'] = Stat.objects.filter(is_active=True)
        return context


class SkillsView(TemplateView):
    template_name = 'portfolio/skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['skill_categories'] = SkillCategory.objects.prefetch_related('skills')
        return context


class ExperienceView(TemplateView):
    template_name = 'portfolio/experience.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['experiences'] = Experience.objects.all()
        context['education'] = Education.objects.all()
        return context