from django import forms
from .models import MundiMapProject, MundiLayer


class MundiMapProjectForm(forms.ModelForm):
    """Form for creating and editing Mundi map projects"""
    
    class Meta:
        model = MundiMapProject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter project description'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Project name is required.")
        return name


class MundiLayerForm(forms.ModelForm):
    """Form for uploading layers to Mundi map projects"""
    
    class Meta:
        model = MundiLayer
        fields = ['name', 'layer_type', 'file_path', 'style_config']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter layer name'
            }),
            'layer_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'file_path': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.geojson,.shp,.tif,.las,.laz,.csv'
            }),
            'style_config': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter JSON style configuration (optional)'
            }),
        }
    
    def clean_file_path(self):
        file_path = self.cleaned_data.get('file_path')
        if not file_path:
            raise forms.ValidationError("Please select a file to upload.")
        
        # Check file size (max 100MB)
        if file_path.size > 100 * 1024 * 1024:
            raise forms.ValidationError("File size must be less than 100MB.")
        
        # Check file extension
        allowed_extensions = ['.geojson', '.shp', '.tif', '.las', '.laz', '.csv']
        file_extension = file_path.name.lower()
        
        if not any(file_extension.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        return file_path
    
    def clean_style_config(self):
        style_config = self.cleaned_data.get('style_config')
        if style_config:
            try:
                import json
                json.loads(style_config)
            except json.JSONDecodeError:
                raise forms.ValidationError("Style configuration must be valid JSON.")
        return style_config


class MapRenderForm(forms.Form):
    """Form for rendering maps"""
    width = forms.IntegerField(
        min_value=100,
        max_value=2000,
        initial=800,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Width in pixels'
        })
    )
    height = forms.IntegerField(
        min_value=100,
        max_value=2000,
        initial=600,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Height in pixels'
        })
    )
    format = forms.ChoiceField(
        choices=[('png', 'PNG'), ('jpg', 'JPEG'), ('pdf', 'PDF')],
        initial='png',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    ) 