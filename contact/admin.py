from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, NewsletterSubscriber, ContactInfo


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject_preview', 'status', 'is_spam', 'created_at']
    list_filter = ['status', 'is_spam', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived', 'mark_as_spam']
    
    fieldsets = (
        ('Message', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'is_spam')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_preview(self, obj):
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = 'Subject'
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
    mark_as_archived.short_description = "Mark selected messages as archived"
    
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True)
    mark_as_spam.short_description = "Mark selected messages as spam"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    actions = ['activate', 'deactivate']
    
    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = "Activate selected subscribers"
    
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = "Deactivate selected subscribers"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'is_active']
    fieldsets = (
        ('Contact Details', {
            'fields': ('email', 'phone', 'address', 'working_hours')
        }),
        ('Social Media', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'facebook_url', 'instagram_url')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )