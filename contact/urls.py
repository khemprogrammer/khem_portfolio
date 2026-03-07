from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('success/', views.ContactSuccessView.as_view(), name='success'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('quick/', views.QuickContactAjaxView.as_view(), name='quick_contact'),
]