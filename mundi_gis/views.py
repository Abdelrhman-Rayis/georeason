from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import requests
import json
import os
from .models import MundiMapProject, MundiLayer, MundiMapRender
from .forms import MundiMapProjectForm, MundiLayerForm


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
            
            # Create project in Mundi API
            api_data = {
                'name': project.name,
                'description': project.description,
            }
            
            api_response = mundi_api_request('maps', method='POST', data=api_data)
            
            if 'error' not in api_response:
                project.mundi_project_id = api_response.get('id')
                project.save()
                messages.success(request, 'Map project created successfully!')
                return redirect('mundi_gis:project_detail', project_id=project.id)
            else:
                messages.error(request, f'Failed to create project: {api_response["error"]}')
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
            
            # Update project in Mundi API
            api_data = {
                'name': project.name,
                'description': project.description,
            }
            
            api_response = mundi_api_request(f'maps/{project.mundi_project_id}', 
                                           method='PUT', data=api_data)
            
            if 'error' not in api_response:
                messages.success(request, 'Map project updated successfully!')
                return redirect('mundi_gis:project_detail', project_id=project.id)
            else:
                messages.error(request, f'Failed to update project: {api_response["error"]}')
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
        # Delete project from Mundi API
        api_response = mundi_api_request(f'maps/{project.mundi_project_id}', 
                                       method='DELETE')
        
        if 'error' not in api_response:
            project.is_active = False
            project.save()
            messages.success(request, 'Map project deleted successfully!')
            return redirect('mundi_gis:project_list')
        else:
            messages.error(request, f'Failed to delete project: {api_response["error"]}')
    
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
            
            # Upload file to Mundi API
            if request.FILES.get('file_path'):
                files = {'file': request.FILES['file_path']}
                headers = {'Authorization': f'Bearer {MUNDI_API_KEY}'}
                
                upload_url = f"{MUNDI_API_BASE_URL}/maps/{project.mundi_project_id}/layers"
                
                try:
                    response = requests.post(upload_url, files=files, headers=headers)
                    response.raise_for_status()
                    api_response = response.json()
                    
                    layer.mundi_layer_id = api_response.get('id')
                    layer.save()
                    
                    messages.success(request, 'Layer uploaded successfully!')
                    return redirect('mundi_gis:project_detail', project_id=project.id)
                except requests.exceptions.RequestException as e:
                    messages.error(request, f'Failed to upload layer: {str(e)}')
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
        
        # Render map via Mundi API
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
            
            messages.success(request, 'Map rendered successfully!')
            return redirect('mundi_gis:project_detail', project_id=project.id)
        else:
            messages.error(request, f'Failed to render map: {api_response["error"]}')
    
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
