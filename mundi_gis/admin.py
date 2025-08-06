from django.contrib import admin
from .models import MundiMapProject, MundiLayer, MundiMapRender


@admin.register(MundiMapProject)
class MundiMapProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    readonly_fields = ['mundi_project_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Mundi Integration', {
            'fields': ('mundi_project_id', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MundiLayer)
class MundiLayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'layer_type', 'map_project', 'created_at']
    list_filter = ['layer_type', 'created_at']
    search_fields = ['name', 'map_project__name']
    readonly_fields = ['mundi_layer_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'layer_type', 'map_project')
        }),
        ('File Upload', {
            'fields': ('file_path',)
        }),
        ('Styling', {
            'fields': ('style_config',),
            'classes': ('collapse',)
        }),
        ('Mundi Integration', {
            'fields': ('mundi_layer_id',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MundiMapRender)
class MundiMapRenderAdmin(admin.ModelAdmin):
    list_display = ['render_id', 'map_project', 'width', 'height', 'created_at']
    list_filter = ['created_at']
    search_fields = ['render_id', 'map_project__name']
    readonly_fields = ['render_id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Render Information', {
            'fields': ('map_project', 'render_id', 'image_file')
        }),
        ('Dimensions', {
            'fields': ('width', 'height')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
