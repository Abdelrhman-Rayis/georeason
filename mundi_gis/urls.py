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
    
    # AI Analysis endpoints
    path('ai/analyze-layer/<uuid:layer_id>/', views.ai_analyze_layer, name='ai_analyze_layer'),
    path('ai/suggest-styling/<uuid:layer_id>/', views.ai_suggest_styling, name='ai_suggest_styling'),
    path('ai/generate-description/<uuid:project_id>/', views.ai_generate_description, name='ai_generate_description'),
    path('ai/test-connection/', views.test_ollama_connection, name='test_ollama_connection'),
    path('projects/<uuid:project_id>/ai-analysis/', views.ai_analysis_page, name='ai_analysis_page'),
    
    # Layer data endpoints
    path('projects/<uuid:project_id>/layers/<int:layer_id>/data/', views.layer_data, name='layer_data'),
    path('projects/<uuid:project_id>/layers-data/', views.project_layers_data, name='project_layers_data'),
] 