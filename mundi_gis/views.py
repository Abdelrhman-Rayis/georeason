from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
import requests
import json
import os
from .models import MundiMapProject, MundiLayer, MundiMapRender
from .forms import MundiMapProjectForm, MundiLayerForm
from .local_llm import LocalLLMService


# Mundi API configuration
MUNDI_API_BASE_URL = os.getenv('MUNDI_API_BASE_URL', 'https://app.mundi.ai/api')
MUNDI_API_KEY = os.getenv('MUNDI_API_KEY', '')


def mundi_api_request(endpoint, method='GET', data=None, headers=None):
    """Helper function to make requests to Mundi API"""
    url = f"{MUNDI_API_BASE_URL}/{endpoint}"
    
    default_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {MUNDI_API_KEY}'
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=default_headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=default_headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=default_headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=default_headers)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


@login_required
def dashboard(request):
    """Main dashboard for Mundi GIS application"""
    user_projects = MundiMapProject.objects.filter(created_by=request.user, is_active=True)
    
    # Get recent projects
    recent_projects = user_projects[:5]
    
    # Get project statistics
    total_projects = user_projects.count()
    total_layers = MundiLayer.objects.filter(map_project__created_by=request.user).count()
    total_renders = MundiMapRender.objects.filter(map_project__created_by=request.user).count()
    
    context = {
        'recent_projects': recent_projects,
        'total_projects': total_projects,
        'total_layers': total_layers,
        'total_renders': total_renders,
        'mundi_api_available': bool(MUNDI_API_KEY),
        'ollama_available': LocalLLMService().is_available(),
    }
    
    return render(request, 'mundi_gis/dashboard.html', context)


@login_required
def project_list(request):
    """List all map projects for the user"""
    projects = MundiMapProject.objects.filter(created_by=request.user, is_active=True)
    
    # Pagination
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'projects': page_obj,
    }
    
    return render(request, 'mundi_gis/project_list.html', context)


@login_required
def project_detail(request, project_id):
    """Detail view for a specific map project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    layers = project.layers.all()
    renders = project.renders.all()[:5]  # Recent renders
    
    context = {
        'project': project,
        'layers': layers,
        'renders': renders,
    }
    
    return render(request, 'mundi_gis/project_detail.html', context)


@login_required
def project_create(request):
    """Create a new map project"""
    if request.method == 'POST':
        form = MundiMapProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            
            # Try to create project in Mundi API (optional)
            if MUNDI_API_KEY:
                api_data = {
                    'name': project.name,
                    'description': project.description,
                }
                
                api_response = mundi_api_request('maps', method='POST', data=api_data)
                
                if 'error' not in api_response:
                    project.mundi_project_id = api_response.get('id')
                    project.save()
                    messages.success(request, 'Map project created successfully with Mundi AI integration!')
                    return redirect('mundi_gis:project_detail', project_id=project.id)
                else:
                    # If API fails, still save locally but warn user
                    project.mundi_project_id = f"local_{project.id}"
                    project.save()
                    messages.warning(request, f'Project created locally. Mundi AI integration failed: {api_response["error"]}')
                    return redirect('mundi_gis:project_detail', project_id=project.id)
            else:
                # No API key configured, save locally only
                project.mundi_project_id = f"local_{project.id}"
                project.save()
                messages.success(request, 'Map project created successfully! (Local mode - no Mundi AI integration)')
                return redirect('mundi_gis:project_detail', project_id=project.id)
    else:
        form = MundiMapProjectForm()
    
    context = {
        'form': form,
        'title': 'Create New Map Project',
    }
    
    return render(request, 'mundi_gis/project_form.html', context)


@login_required
def project_update(request, project_id):
    """Update an existing map project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    
    if request.method == 'POST':
        form = MundiMapProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            
            # Try to update project in Mundi API (optional)
            if MUNDI_API_KEY and not project.mundi_project_id.startswith('local_'):
                api_data = {
                    'name': project.name,
                    'description': project.description,
                }
                
                api_response = mundi_api_request(f'maps/{project.mundi_project_id}', 
                                               method='PUT', data=api_data)
                
                if 'error' not in api_response:
                    messages.success(request, 'Map project updated successfully with Mundi AI integration!')
                    return redirect('mundi_gis:project_detail', project_id=project.id)
                else:
                    messages.warning(request, f'Project updated locally. Mundi AI integration failed: {api_response["error"]}')
                    return redirect('mundi_gis:project_detail', project_id=project.id)
            else:
                # No API key or local project, save locally only
                messages.success(request, 'Map project updated successfully! (Local mode)')
                return redirect('mundi_gis:project_detail', project_id=project.id)
    else:
        form = MundiMapProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'title': 'Update Map Project',
    }
    
    return render(request, 'mundi_gis/project_form.html', context)


@login_required
def project_delete(request, project_id):
    """Delete a map project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    
    if request.method == 'POST':
        # Try to delete project from Mundi API (optional)
        if MUNDI_API_KEY and not project.mundi_project_id.startswith('local_'):
            api_response = mundi_api_request(f'maps/{project.mundi_project_id}', 
                                           method='DELETE')
            
            if 'error' not in api_response:
                project.is_active = False
                project.save()
                messages.success(request, 'Map project deleted successfully from Mundi AI!')
                return redirect('mundi_gis:project_list')
            else:
                # If API fails, still delete locally
                project.is_active = False
                project.save()
                messages.warning(request, f'Project deleted locally. Mundi AI deletion failed: {api_response["error"]}')
                return redirect('mundi_gis:project_list')
        else:
            # No API key or local project, delete locally only
            project.is_active = False
            project.save()
            messages.success(request, 'Map project deleted successfully! (Local mode)')
            return redirect('mundi_gis:project_list')
    
    context = {
        'project': project,
    }
    
    return render(request, 'mundi_gis/project_confirm_delete.html', context)


@login_required
def layer_upload(request, project_id):
    """Upload a layer to a map project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    
    if request.method == 'POST':
        form = MundiLayerForm(request.POST, request.FILES)
        if form.is_valid():
            layer = form.save(commit=False)
            layer.map_project = project
            
            # Upload file to Mundi API (optional)
            if request.FILES.get('file_path'):
                if MUNDI_API_KEY and not project.mundi_project_id.startswith('local_'):
                    files = {'file': request.FILES['file_path']}
                    headers = {'Authorization': f'Bearer {MUNDI_API_KEY}'}
                    
                    upload_url = f"{MUNDI_API_BASE_URL}/maps/{project.mundi_project_id}/layers"
                    
                    try:
                        response = requests.post(upload_url, files=files, headers=headers)
                        response.raise_for_status()
                        api_response = response.json()
                        
                        layer.mundi_layer_id = api_response.get('id')
                        layer.save()
                        
                        messages.success(request, 'Layer uploaded successfully with Mundi AI integration!')
                        return redirect('mundi_gis:project_detail', project_id=project.id)
                    except requests.exceptions.RequestException as e:
                        # If API fails, still save locally
                        layer.mundi_layer_id = f"local_{layer.id}"
                        layer.save()
                        messages.warning(request, f'Layer saved locally. Mundi AI upload failed: {str(e)}')
                        return redirect('mundi_gis:project_detail', project_id=project.id)
                else:
                    # No API key or local project, save locally only
                    layer.mundi_layer_id = f"local_{layer.id}"
                    layer.save()
                    
                    messages.success(request, 'Layer uploaded successfully! (Local mode)')
                    return redirect('mundi_gis:project_detail', project_id=project.id)
    else:
        form = MundiLayerForm()
    
    context = {
        'form': form,
        'project': project,
    }
    
    return render(request, 'mundi_gis/layer_upload.html', context)


@login_required
def render_map(request, project_id):
    """Render a map as PNG"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    
    if request.method == 'POST':
        width = request.POST.get('width', 800)
        height = request.POST.get('height', 600)
        
        # Render map via Mundi API (optional)
        if MUNDI_API_KEY and not project.mundi_project_id.startswith('local_'):
            api_data = {
                'width': int(width),
                'height': int(height),
            }
            
            api_response = mundi_api_request(f'maps/{project.mundi_project_id}/render', 
                                           method='POST', data=api_data)
            
            if 'error' not in api_response:
                render_obj = MundiMapRender.objects.create(
                    map_project=project,
                    render_id=api_response.get('id'),
                    width=width,
                    height=height,
                    image_file=api_response.get('image_url')
                )
                
                messages.success(request, 'Map rendered successfully with Mundi AI!')
                return redirect('mundi_gis:project_detail', project_id=project.id)
            else:
                messages.warning(request, f'Map rendering failed: {api_response["error"]}. Try using local mode.')
                return redirect('mundi_gis:project_detail', project_id=project.id)
        else:
            # Local mode - create a placeholder render
            import time
            render_obj = MundiMapRender.objects.create(
                map_project=project,
                render_id=f"local_render_{project.id}_{int(width)}x{int(height)}_{int(time.time())}",
                width=width,
                height=height
            )
            
            messages.success(request, 'Map render created successfully! (Local mode - no actual image generated)')
            return redirect('mundi_gis:project_detail', project_id=project.id)
    
    context = {
        'project': project,
    }
    
    return render(request, 'mundi_gis/render_map.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def mundi_webhook(request):
    """Handle webhooks from Mundi API"""
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        
        if event_type == 'map.updated':
            project_id = data.get('project_id')
            project = MundiMapProject.objects.get(mundi_project_id=project_id)
            # Handle map update
            pass
        elif event_type == 'layer.uploaded':
            layer_id = data.get('layer_id')
            layer = MundiLayer.objects.get(mundi_layer_id=layer_id)
            # Handle layer upload
            pass
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def ai_analyze_layer(request, layer_id):
    """Analyze a layer using local LLM"""
    try:
        layer = get_object_or_404(MundiLayer, id=layer_id, map_project__created_by=request.user)
        question = request.POST.get('question', 'Tell me about this layer')
        
        llm_service = LocalLLMService()
        
        if not llm_service.is_available():
            return JsonResponse({
                'error': 'Local LLM (Ollama) is not available. Please make sure Ollama is running.',
                'available': False
            }, status=503)
        
        layer_info = {
            'name': layer.name,
            'layer_type': layer.get_layer_type_display(),
            'feature_count': 'Unknown',  # Would need to be calculated from actual data
            'geometry_type': 'Unknown',  # Would need to be extracted from file
            'description': f'Layer uploaded on {layer.created_at.strftime("%Y-%m-%d")}',
            'created_at': layer.created_at.strftime("%Y-%m-%d")
        }
        
        analysis = llm_service.analyze_gis_data(layer_info, question)
        
        return JsonResponse({
            'analysis': analysis,
            'question': question,
            'layer_name': layer.name,
            'available': True
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def ai_suggest_styling(request, layer_id):
    """Get AI suggestions for layer styling"""
    try:
        layer = get_object_or_404(MundiLayer, id=layer_id, map_project__created_by=request.user)
        
        llm_service = LocalLLMService()
        
        if not llm_service.is_available():
            return JsonResponse({
                'error': 'Local LLM (Ollama) is not available.',
                'available': False
            }, status=503)
        
        layer_info = {
            'name': layer.name,
            'layer_type': layer.get_layer_type_display(),
            'geometry_type': 'Unknown',
            'feature_count': 'Unknown'
        }
        
        styling_suggestions = llm_service.suggest_layer_styling(layer_info)
        
        return JsonResponse({
            'styling': styling_suggestions,
            'layer_name': layer.name,
            'available': True
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def ai_generate_description(request, project_id):
    """Generate AI description for a project"""
    try:
        project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
        
        llm_service = LocalLLMService()
        
        if not llm_service.is_available():
            return JsonResponse({
                'error': 'Local LLM (Ollama) is not available.',
                'available': False
            }, status=503)
        
        project_info = {
            'name': project.name,
            'description': project.description,
            'layer_count': project.layers.count()
        }
        
        description = llm_service.generate_map_description(project_info)
        
        return JsonResponse({
            'description': description,
            'project_name': project.name,
            'available': True
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def test_ollama_connection(request):
    """Test the connection to Ollama"""
    try:
        llm_service = LocalLLMService()
        status = llm_service.test_connection()
        
        return JsonResponse(status)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'available': False
        }, status=500)


@login_required
def ai_analysis_page(request, project_id):
    """AI Analysis page for a project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    layers = project.layers.all()
    
    context = {
        'project': project,
        'layers': layers,
    }
    
    return render(request, 'mundi_gis/ai_analysis.html', context)


@login_required
def ai_chat_page(request, project_id):
    """AI Chat interface for a project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    
    context = {
        'project': project,
    }
    
    return render(request, 'mundi_gis/ai_chat.html', context)


@login_required
def ai_analyze_project(request):
    """Analyze project with AI"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        question = data.get('question', '')
        project_info = data.get('project_info', {})
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        llm_service = LocalLLMService()
        
        if not llm_service.is_available():
            return JsonResponse({
                'error': 'Local LLM (Ollama) is not available. Please make sure Ollama is running.',
                'available': False
            }, status=503)
        
        # Create a comprehensive prompt for the AI
        prompt = f"""
        You are a GIS (Geographic Information System) expert assistant. Analyze the following project and answer the user's question.

        Project Information:
        - Name: {project_info.get('name', 'Unknown')}
        - Description: {project_info.get('description', 'No description')}
        - Number of Layers: {project_info.get('layer_count', 0)}
        
        Layers:
        {chr(10).join([f"- {layer.get('name', 'Unknown')} ({layer.get('type', 'Unknown')}): {layer.get('description', 'No description')}" for layer in project_info.get('layers', [])])}

        User Question: {question}

        Please provide a detailed, helpful response that demonstrates your GIS expertise. If the question is about data analysis, suggest what insights could be gained. If it's about styling, provide specific recommendations. If it's about the project structure, explain the components and their purposes.
        """
        
        analysis = llm_service.analyze_text(prompt)
        
        return JsonResponse({
            'analysis': analysis,
            'question': question,
            'available': True
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def layer_data(request, project_id, layer_id):
    """Serve layer data as GeoJSON"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    layer = get_object_or_404(MundiLayer, id=layer_id, project=project)
    
    try:
        # Handle both string paths and FieldFile objects
        if hasattr(layer.file_path, 'path'):
            file_path = layer.file_path.path
        else:
            file_path = os.path.join(settings.MEDIA_ROOT, str(layer.file_path))
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                geojson_data = json.load(f)
            
            # Add layer metadata to the response
            response_data = {
                'layer_id': layer.id,
                'layer_name': layer.name,
                'layer_type': layer.layer_type,
                'geojson': geojson_data
            }
            
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def project_layers_data(request, project_id):
    """Get all layers data for a project"""
    project = get_object_or_404(MundiMapProject, id=project_id, created_by=request.user)
    layers = project.layers.all()
    
    layers_data = []
    print(f"Processing {layers.count()} layers for project {project.name}")
    for layer in layers:
        print(f"Processing layer: {layer.name} (ID: {layer.id})")
        try:
            # Handle both string paths and FieldFile objects
            if hasattr(layer.file_path, 'path'):
                file_path = layer.file_path.path
            else:
                file_path = os.path.join(settings.MEDIA_ROOT, str(layer.file_path))
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    geojson_data = json.load(f)
                
                layer_info = {
                    'id': layer.id,
                    'name': layer.name,
                    'layer_type': layer.layer_type,
                    'description': f'{layer.name} ({layer.get_layer_type_display()}) layer',
                    'created_at': layer.created_at.isoformat(),
                    'geojson': geojson_data
                }
                layers_data.append(layer_info)
        except Exception as e:
            print(f"Error loading layer {layer.name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return JsonResponse({'layers': layers_data})
