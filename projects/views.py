from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from .models import Project, ProjectCategory, Technology
from .github_api import GitHubAPI


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True).prefetch_related('technologies')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by technology
        tech_slug = self.request.GET.get('tech')
        if tech_slug:
            queryset = queryset.filter(technologies__slug=tech_slug)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(technologies__name__icontains=search)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        context['technologies'] = Technology.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_tech'] = self.request.GET.get('tech', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Featured projects for sidebar
        context['featured_projects'] = Project.objects.filter(
            is_featured=True, is_public=True
        )[:3]
        
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Project.objects.filter(is_public=True).prefetch_related(
            'technologies', 'images', 'features'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Related projects
        context['related_projects'] = Project.objects.filter(
            is_public=True,
            category=project.category
        ).exclude(id=project.id)[:3]
        
        # GitHub data if available
        if project.github_repo_name:
            github = GitHubAPI()
            context['github_repo'] = github.get_repository(project.github_repo_name)
            context['github_languages'] = github.get_languages(project.github_repo_name)
        
        return context


class GitHubStatsView(TemplateView):
    template_name = 'projects/github_stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        github = GitHubAPI()
        
        # Get comprehensive stats
        context['stats'] = github.get_user_stats()
        context['repositories'] = github.get_repositories(per_page=30)
        context['profile'] = github.get_user_profile()
        
        return context