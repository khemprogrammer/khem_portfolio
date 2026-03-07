from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import ContactForm, NewsletterForm, QuickContactForm
from .models import ContactInfo
from portfolio.models import Profile


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/contact/success/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['contact_info'] = ContactInfo.objects.filter(is_active=True).first()
        context['newsletter_form'] = NewsletterForm()
        return context
    
    def form_valid(self, form):
        # Save the message
        message = form.save()
        
        # Send email notification
        try:
            subject = f"Portfolio Contact: {message.subject or 'New Message'}"
            email_body = f"""
Name: {message.name}
Email: {message.email}
Subject: {message.subject or 'N/A'}

Message:
{message.message}

---
Sent from your portfolio website
            """
            
            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True
            )
        except Exception as e:
            # Log error but don't stop the success message
            print(f"Email sending failed: {e}")
        
        messages.success(
            self.request, 
            "Thank you for your message! I'll get back to you soon."
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors below."
        )
        return super().form_invalid(form)


class ContactSuccessView(TemplateView):
    template_name = 'contact/contact_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        return context


class NewsletterSubscribeView(View):
    """Handle AJAX newsletter subscription"""
    
    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        
        if form.is_valid():
            subscriber = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing to the newsletter!'
            })
        else:
            errors = []
            for field, error_list in form.errors.items():
                errors.extend(error_list)
            
            return JsonResponse({
                'success': False,
                'message': ' '.join(errors)
            }, status=400)


class QuickContactAjaxView(View):
    """Handle AJAX quick contact form submission"""
    
    def post(self, request, *args, **kwargs):
        form = QuickContactForm(request.POST)
        
        if form.is_valid():
            # Create and save contact message manually
            from .models import ContactMessage
            
            message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject='Quick Contact',
                message=form.cleaned_data['message']
            )
            
            # Add request metadata
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                message.ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                message.ip_address = request.META.get('REMOTE_ADDR')
            message.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
            
            message.save()
            
            # Try to send email notification
            try:
                send_mail(
                    subject='Portfolio Quick Contact',
                    message=f"From: {message.name}\nEmail: {message.email}\n\n{message.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True
                )
            except:
                pass
            
            return JsonResponse({
                'success': True,
                'message': 'Message sent successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please check your input and try again.'
            }, status=400)