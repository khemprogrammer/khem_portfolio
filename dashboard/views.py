from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from projects.models import Project, ProjectCategory, Technology, ProjectImage
from contact.models import ContactMessage
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
import datetime


# Login view - only accessible to superusers
def dashboard_login(request):
    # If already logged in as superuser, redirect to dashboard
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid credentials or not a superuser.')
    
    return render(request, 'dashboard/login.html')


# Logout view
@login_required(login_url='dashboard:login')
def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')


# Dashboard home - overview statistics
@login_required(login_url='dashboard:login')
def index(request):
    if not request.user.is_superuser:
        return redirect('dashboard:login')
    
    # Statistics
    total_projects = Project.objects.count()
    featured_projects = Project.objects.filter(is_featured=True).count()
    pinned_projects = Project.objects.filter(is_pinned=True).count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(status='new').count()
    
    # Recent messages
    recent_messages = ContactMessage.objects.all()[:5]
    
    # Recent projects
    recent_projects = Project.objects.all()[:5]
    
    # Messages by status
    messages_by_status = {
        'new': ContactMessage.objects.filter(status='new').count(),
        'read': ContactMessage.objects.filter(status='read').count(),
        'replied': ContactMessage.objects.filter(status='replied').count(),
    }
    
    context = {
        'total_projects': total_projects,
        'featured_projects': featured_projects,
        'pinned_projects': pinned_projects,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'recent_messages': recent_messages,
        'recent_projects': recent_projects,
        'messages_by_status': messages_by_status,
    }
    
    return render(request, 'dashboard/index.html', context)


# Projects list with pagination and search
@login_required(login_url='dashboard:login')
def projects(request):
    if not request.user.is_superuser:
        return redirect('dashboard:login')
    
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    projects_list = Project.objects.all().order_by('-is_pinned', '-is_featured', '-created_at')
    
    if search_query:
        projects_list = projects_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        projects_list = projects_list.filter(status=status_filter)
    
    paginator = Paginator(projects_list, 10)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)
    
    context = {
        'projects': projects_page,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/projects.html', context)


# Create new project
@login_required(login_url='dashboard:login')
def project_create(request):
    if not request.user.is_superuser:
        return redirect('dashboard:login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description')
        short_description = request.POST.get('short_description')
        status = request.POST.get('status', 'completed')
        category_id = request.POST.get('category')
        github_url = request.POST.get('github_url')
        demo_url = request.POST.get('demo_url')
        is_featured = request.POST.get('is_featured') == 'on'
        is_pinned = request.POST.get('is_pinned') == 'on'
        
        project = Project.objects.create(
            title=title,
            subtitle=subtitle,
            description=description,
            short_description=short_description,
            status=status,
            github_url=github_url,
            demo_url=demo_url,
            is_featured=is_featured,
            is_pinned=is_pinned,
        )
        
        if category_id:
            project.category = ProjectCategory.objects.get(id=category_id)
            project.save()
        
        # Handle technologies
        technology_ids = request.POST.getlist('technologies')
        if technology_ids:
            technologies = Technology.objects.filter(id__in=technology_ids)
            project.technologies.set(technologies)
        
        messages.success(request, 'Project created successfully!')
        return redirect('dashboard:projects')
    
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    context = {
        'categories': categories,
        'technologies': technologies,
        'status_choices': Project.STATUS_CHOICES,
    }
    
    return render(request, 'dashboard/project_form.html', context)


# Edit existing project
@login_required(login_url='dashboard:login')
def project_edit(request, project_id):
    if not request.user.is_superuser:
        return redirect('dashboard:login')
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.subtitle = request.POST.get('subtitle')
        project.description = request.POST.get('description')
        project.short_description = request.POST.get('short_description')
        project.status = request.POST.get('status', 'completed')
        project.github_url = request.POST.get('github_url')
        project.demo_url = request.POST.get('demo_url')
        project.is_featured = request.POST.get('is_featured') == 'on'
        project.is_pinned = request.POST.get('is_pinned') == 'on'
        
        category_id = request.POST.get('category')
        if category_id:
            project.category = ProjectCategory.objects.get(id=category_id)
        else:
            project.category = None
        
        project.save()
        
        # Handle technologies
        technology_ids = request.POST.getlist('technologies')
        technologies = Technology.objects.filter(id__in=technology_ids)
        project.technologies.set(technologies)
        
        messages.success(request, 'Project updated successfully!')
        return redirect('dashboard:projects')
    
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    
    context = {
        'project': project,
        'categories': categories,
        'technologies': technologies,
        'status_choices': Project.STATUS_CHOICES,
    }
    
    return render(request, 'dashboard/project_form.html', context)


# Delete project
@login_required(login_url='dashboard:login')
@require_http_methods(["POST"])
def project_delete(request, project_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    
    messages.success(request, 'Project deleted successfully!')
    return JsonResponse({'success': True})


# Toggle pin status
@login_required(login_url='dashboard:login')
@require_http_methods(["POST"])
def project_toggle_pin(request, project_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    project = get_object_or_404(Project, id=project_id)
    project.is_pinned = not project.is_pinned
    project.save()
    
    return JsonResponse({
        'success': True, 
        'is_pinned': project.is_pinned,
        'message': 'Project pinned!' if project.is_pinned else 'Project unpinned!'
    })


# Toggle featured status
@login_required(login_url='dashboard:login')
@require_http_methods(["POST"])
def project_toggle_featured(request, project_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    project = get_object_or_404(Project, id=project_id)
    project.is_featured = not project.is_featured
    project.save()
    
    return JsonResponse({
        'success': True, 
        'is_featured': project.is_featured,
        'message': 'Project marked as featured!' if project.is_featured else 'Project removed from featured!'
    })


# Messages list
@login_required(login_url='dashboard:login')
def messages_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard:login')
    
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    messages_qs = ContactMessage.objects.all().order_by('-created_at')
    
    if search_query:
        messages_qs = messages_qs.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    if status_filter:
        messages_qs = messages_qs.filter(status=status_filter)
    
    paginator = Paginator(messages_qs, 15)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages': messages_page,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/messages.html', context)


# View single message
@login_required(login_url='dashboard:login')
def message_detail(request, message_id):
    if not request.user.is_superuser:
        return redirect('dashboard:login')
    
    message = get_object_or_404(ContactMessage, id=message_id)
    
    # Mark as read if new
    if message.status == 'new':
        message.status = 'read'
        message.save()
    
    context = {
        'message': message,
    }
    
    return render(request, 'dashboard/message_detail.html', context)


# Update message status
@login_required(login_url='dashboard:login')
@require_http_methods(["POST"])
def message_update_status(request, message_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    message = get_object_or_404(ContactMessage, id=message_id)
    new_status = request.POST.get('status')
    
    if new_status in ['new', 'read', 'replied', 'archived']:
        message.status = new_status
        message.save()
        return JsonResponse({'success': True, 'status': new_status})
    
    return JsonResponse({'success': False, 'message': 'Invalid status'})


# Delete message
@login_required(login_url='dashboard:login')
@require_http_methods(["POST"])
def message_delete(request, message_id):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    
    messages.success(request, 'Message deleted successfully!')
    return JsonResponse({'success': True})
