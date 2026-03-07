from django.db import models
from django.utils.text import slugify


class SkillCategory(models.Model):
    """Categories for skills (e.g., Programming, Frameworks, Tools)"""
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual skills with proficiency levels"""
    PROFICIENCY_CHOICES = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
    ]
    
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(choices=PROFICIENCY_CHOICES, default=3)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class or image path")
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    
    class Meta:
        ordering = ['-proficiency', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Experience(models.Model):
    """Work experience and professional history"""
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_current', '-start_date', 'order']
        verbose_name_plural = "Experiences"
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    """Educational background"""
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-end_date', '-start_date']
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certification(models.Model):
    """Professional certifications"""
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_issued = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-date_issued']
    
    def __str__(self):
        return f"{self.name} - {self.issuer}"


class Profile(models.Model):
    """Main profile information"""
    name = models.CharField(max_length=200, default="Khem Bahadur Lodh")
    title = models.CharField(max_length=300, default="Python Developer | Full-Stack Developer | AI Enthusiast")
    location = models.CharField(max_length=200, default="Nepal")
    email = models.EmailField(default="contact@khemlodh.com.np")
    phone = models.CharField(max_length=20, blank=True)
    
    # Social links
    github_url = models.URLField(default="https://github.com/khemprogrammer")
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    # About content
    short_bio = models.TextField(
        default="Khem Bahadur Lodh is a passionate Python developer focused on building intelligent applications, AI tools, and modern web platforms."
    )
    full_bio = models.TextField(blank=True, help_text="Detailed biography for about page")
    
    # Resume
    resume = models.FileField(upload_to='resumes/', blank=True)
    
    # Hero section
    hero_headline = models.CharField(
        max_length=300,
        default="Building Intelligent Applications with Python & AI"
    )
    hero_subheadline = models.CharField(
        max_length=300,
        default="Transforming ideas into powerful digital solutions"
    )
    
    # Profile image
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one active profile
        if self.is_active:
            Profile.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Stat(models.Model):
    """Statistics for the portfolio (e.g., Years Experience, Projects Completed)"""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g., +, %")
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.label}: {self.value}{self.suffix}"