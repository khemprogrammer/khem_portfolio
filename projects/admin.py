from django.contrib import admin
from .models import ProjectCategory, Technology, Project, ProjectImage, ProjectFeature


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 2


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_count', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'is_featured', 
        'is_public', 'github_stars', 'created_at'
    ]
    list_filter = ['status', 'is_featured', 'is_public', 'category', 'technologies']
    search_fields = ['title', 'description', 'github_repo_name']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    list_editable = ['status', 'is_featured', 'is_public']
    date_hierarchy = 'created_at'
    inlines = [ProjectFeatureInline, ProjectImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'subtitle', 'short_description', 'description')
        }),
        ('Categorization', {
            'fields': ('category', 'technologies')
        }),
        ('Media', {
            'fields': ('image', 'thumbnail', 'video_url')
        }),
        ('Links', {
            'fields': ('github_url', 'demo_url', 'documentation_url')
        }),
        ('GitHub Integration', {
            'fields': ('github_repo_name', 'github_stars', 'github_forks', 'last_github_sync'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'is_public', 'order')
        }),
    )
    readonly_fields = ['github_stars', 'github_forks', 'last_github_sync', 'created_at', 'updated_at']


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order']
    list_filter = ['project']


@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'order']
    list_filter = ['project']