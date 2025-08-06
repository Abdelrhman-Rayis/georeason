from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mundi_gis.models import MundiMapProject, MundiLayer
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Check and debug layer loading issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking layers...'))
        
        # Check all projects
        projects = MundiMapProject.objects.all()
        self.stdout.write(f'Found {projects.count()} projects')
        
        for project in projects:
            self.stdout.write(f'\nProject: {project.name} (ID: {project.id})')
            self.stdout.write(f'Created by: {project.created_by.username}')
            
            layers = project.layers.all()
            self.stdout.write(f'Layers: {layers.count()}')
            
            for layer in layers:
                self.stdout.write(f'  - {layer.name} ({layer.layer_type})')
                self.stdout.write(f'    ID: {layer.id}')
                self.stdout.write(f'    File path: {layer.file_path}')
                
                # Check if file exists
                if layer.file_path:
                    if hasattr(layer.file_path, 'path'):
                        file_path = layer.file_path.path
                    else:
                        file_path = os.path.join(settings.MEDIA_ROOT, str(layer.file_path))
                    
                    self.stdout.write(f'    Full path: {file_path}')
                    self.stdout.write(f'    Exists: {os.path.exists(file_path)}')
                    
                    if os.path.exists(file_path):
                        try:
                            file_size = os.path.getsize(file_path)
                            self.stdout.write(f'    File size: {file_size} bytes')
                            
                            # Try to read as JSON
                            import json
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                            self.stdout.write(f'    Valid JSON: Yes')
                            if 'features' in data:
                                self.stdout.write(f'    Features: {len(data["features"])}')
                        except Exception as e:
                            self.stdout.write(f'    Error reading file: {e}')
                else:
                    self.stdout.write(f'    No file path')
                
                self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('Layer check complete!')) 