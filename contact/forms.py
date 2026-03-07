from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    """Contact form with validation"""
    
    # Honeypot field for spam protection
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none;'}),
        label=""
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message...',
                'rows': 5,
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean_website(self):
        """Check honeypot field - if filled, likely spam"""
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError("Spam detected!")
        return website
    
    def clean_message(self):
        """Validate message content"""
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        
        # Check for common spam patterns
        spam_words = ['viagra', 'cialis', 'casino', 'lottery', 'winner', 'click here', 'buy now']
        message_lower = message.lower()
        for word in spam_words:
            if word in message_lower:
                raise forms.ValidationError("Your message contains inappropriate content.")
        
        return message
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Add request metadata
        if self.request:
            instance.ip_address = self.get_client_ip(self.request)
            instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:500]
        
        if commit:
            instance.save()
        
        return instance
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name (optional)'
            }),
        }
    
    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email', '').lower().strip()
        
        # Check if already subscribed
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed to our newsletter.")
        
        return email
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.email = instance.email.lower().strip()
        
        # Check if previously unsubscribed
        existing = NewsletterSubscriber.objects.filter(email=instance.email).first()
        if existing:
            existing.is_active = True
            existing.name = instance.name or existing.name
            existing.unsubscribed_at = None
            if commit:
                existing.save()
            return existing
        
        if commit:
            instance.save()
        return instance


class QuickContactForm(forms.Form):
    """Simplified contact form for quick messages"""
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'How can I help you?',
            'rows': 3
        })
    )