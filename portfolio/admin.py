from django.contrib import admin
from .models import (
    Profile, SkillCategory, Skill, Experience, 
    Education, Certification, Stat
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'location', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'title', 'email']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'location', 'email', 'phone')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'website_url')
        }),
        ('Hero Section', {
            'fields': ('hero_headline', 'hero_subheadline')
        }),
        ('About', {
            'fields': ('short_bio', 'full_bio')
        }),
        ('Media', {
            'fields': ('profile_image', 'resume')
        }),
        ('Status', {
            'fields': ('is_active', 'updated_at')
        }),
    )
    readonly_fields = ['updated_at']


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ['name', 'proficiency', 'is_featured']


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'skill_count']
    list_editable = ['order']
    inlines = [SkillInline]
    
    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = 'Skills'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured']
    list_filter = ['category', 'proficiency', 'is_featured']
    search_fields = ['name', 'category__name']
    list_editable = ['proficiency', 'is_featured']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    search_fields = ['title', 'company']
    date_hierarchy = 'start_date'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date']
    search_fields = ['degree', 'institution']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'date_issued']
    search_fields = ['name', 'issuer']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'suffix', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']