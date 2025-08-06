from django.db import models
from django.contrib.auth.models import User
import uuid


class MundiMapProject(models.Model):
    """Model to store Mundi map project information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    mundi_project_id = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class MundiLayer(models.Model):
    """Model to store Mundi layer information"""
    LAYER_TYPES = [
        ('vector', 'Vector'),
        ('raster', 'Raster'),
        ('point_cloud', 'Point Cloud'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    layer_type = models.CharField(max_length=20, choices=LAYER_TYPES)
    mundi_layer_id = models.CharField(max_length=255, unique=True)
    map_project = models.ForeignKey(MundiMapProject, on_delete=models.CASCADE, related_name='layers')
    file_path = models.FileField(upload_to='mundi_layers/', blank=True, null=True)
    style_config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_layer_type_display()})"


class MundiMapRender(models.Model):
    """Model to store rendered map images"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map_project = models.ForeignKey(MundiMapProject, on_delete=models.CASCADE, related_name='renders')
    render_id = models.CharField(max_length=255, unique=True)
    image_file = models.ImageField(upload_to='mundi_renders/', blank=True, null=True)
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=600)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Render {self.render_id} for {self.map_project.name}"
