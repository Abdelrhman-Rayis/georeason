from django.urls import path
from . import views

app_name = 'mundi_gis'

urlpatterns = [
    # Dashboard and overview
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    
    # Project management
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<uuid:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<uuid:project_id>/edit/', views.project_update, name='project_update'),
    path('projects/<uuid:project_id>/delete/', views.project_delete, name='project_delete'),
    
    # Layer management
    path('projects/<uuid:project_id>/upload-layer/', views.layer_upload, name='layer_upload'),
    
    # Map rendering
    path('projects/<uuid:project_id>/render/', views.render_map, name='render_map'),
    
    # API webhooks
    path('webhook/', views.mundi_webhook, name='webhook'),
] 