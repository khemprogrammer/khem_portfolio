from django.db import models
from django.utils.text import slugify


class ProjectCategory(models.Model):
    """Categories for projects (e.g., Web App, AI/ML, Mobile)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Technology(models.Model):
    """Technologies used in projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#6c757d", help_text="Hex color code")
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects"""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('maintenance', 'Under Maintenance'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, help_text="Brief summary for cards")
    
    # Relations
    category = models.ForeignKey(
        ProjectCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='projects'
    )
    technologies = models.ManyToManyField(Technology, blank=True, related_name='projects')
    
    # Media
    image = models.ImageField(upload_to='projects/', blank=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True)
    video_url = models.URLField(blank=True, help_text="Demo video URL")
    
    # Links
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    
    # GitHub integration
    github_repo_name = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Repository name for GitHub API sync"
    )
    github_stars = models.PositiveIntegerField(default=0)
    github_forks = models.PositiveIntegerField(default=0)
    last_github_sync = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_public = models.BooleanField(default=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_featured', '-created_at', 'order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.short_description and self.description:
            self.short_description = self.description[:200] + '...' if len(self.description) > 200 else self.description
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('projects:detail', kwargs={'slug': self.slug})


class ProjectImage(models.Model):
    """Additional images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"


class ProjectFeature(models.Model):
    """Key features of a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"