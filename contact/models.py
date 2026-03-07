from django.db import models
from django.core.validators import EmailValidator


class ContactMessage(models.Model):
    """Contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    
    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    is_spam = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class NewsletterSubscriber(models.Model):
    """Newsletter subscribers"""
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class ContactInfo(models.Model):
    """Contact information displayed on the website"""
    email = models.EmailField(default="contact@khemlodh.com.np")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Social media
    github_url = models.URLField(default="https://github.com/khemprogrammer")
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    # Map coordinates (for embedded maps)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Working hours
    working_hours = models.CharField(max_length=200, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return "Contact Information"
    
    def save(self, *args, **kwargs):
        # Ensure only one active contact info
        if self.is_active:
            ContactInfo.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)