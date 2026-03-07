from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Login/Logout
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    
    # Dashboard
    path('', views.index, name='index'),
    
    # Projects
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:project_id>/toggle-pin/', views.project_toggle_pin, name='project_toggle_pin'),
    path('projects/<int:project_id>/toggle-featured/', views.project_toggle_featured, name='project_toggle_featured'),
    
    # Messages
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('messages/<int:message_id>/update/', views.message_update_status, name='message_update_status'),
    path('messages/<int:message_id>/delete/', views.message_delete, name='message_delete'),
]
