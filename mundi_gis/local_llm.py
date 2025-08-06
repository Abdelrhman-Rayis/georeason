import requests
import json
import os
from typing import Dict, List, Optional, Any
from django.conf import settings


class LocalLLMService:
    """Service for interacting with local LLM via Ollama"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434/v1"
        self.model = getattr(settings, 'OLLAMA_MODEL', 'orieg/gemma3-tools:1b')
        self.api_key = "ollama"  # Dummy key for Ollama
        
    def is_available(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/models")
            if response.status_code == 200:
                return response.json().get('models', [])
            return []
        except requests.exceptions.RequestException:
            return []
    
    def analyze_gis_data(self, layer_info: Dict[str, Any], question: str) -> str:
        """Analyze GIS data using local LLM"""
        system_prompt = """You are Kue, an AI assistant specialized in Geographic Information Systems (GIS) and spatial data analysis. 
        You help users understand and analyze geographic data layers, maps, and spatial relationships.
        
        When analyzing GIS data, consider:
        - Layer type (vector/raster/point cloud)
        - Geometry types and feature counts
        - Spatial relationships and patterns
        - Attribute data and metadata
        - Potential use cases and insights
        
        Provide clear, informative responses that help users understand their geographic data."""
        
        user_prompt = f"""
        Layer Information:
        - Name: {layer_info.get('name', 'Unknown')}
        - Type: {layer_info.get('layer_type', 'Unknown')}
        - Feature Count: {layer_info.get('feature_count', 'Unknown')}
        - Geometry Type: {layer_info.get('geometry_type', 'Unknown')}
        - Description: {layer_info.get('description', 'No description')}
        - Created: {layer_info.get('created_at', 'Unknown')}
        
        User Question: {question}
        
        Please analyze this GIS layer and answer the user's question.
        """
        
        return self._make_chat_completion(system_prompt, user_prompt)
    
    def generate_map_description(self, project_info: Dict[str, Any]) -> str:
        """Generate a description for a map project"""
        system_prompt = """You are an expert GIS analyst. Generate concise, informative descriptions for map projects based on their layers and metadata."""
        
        user_prompt = f"""
        Map Project: {project_info.get('name', 'Unknown')}
        Layers: {project_info.get('layer_count', 0)} layers
        Description: {project_info.get('description', 'No description provided')}
        
        Generate a brief, professional description of this map project.
        """
        
        return self._make_chat_completion(system_prompt, user_prompt)
    
    def suggest_layer_styling(self, layer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest styling options for a GIS layer"""
        system_prompt = """You are a GIS styling expert. Suggest appropriate styling options for different types of geographic data layers."""
        
        user_prompt = f"""
        Layer: {layer_info.get('name', 'Unknown')}
        Type: {layer_info.get('layer_type', 'Unknown')}
        Geometry: {layer_info.get('geometry_type', 'Unknown')}
        Feature Count: {layer_info.get('feature_count', 'Unknown')}
        
        Suggest appropriate styling options for this layer. Return as JSON with:
        - color_scheme: suggested color scheme
        - opacity: suggested opacity (0-1)
        - stroke_width: for vector layers
        - point_size: for point layers
        - classification: suggested classification method
        """
        
        response = self._make_chat_completion(system_prompt, user_prompt)
        
        # Try to parse JSON response
        try:
            # Extract JSON from response if it's wrapped in text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Return default styling if JSON parsing fails
        return {
            "color_scheme": "viridis",
            "opacity": 0.8,
            "stroke_width": 1,
            "point_size": 5,
            "classification": "natural_breaks"
        }
    
    def _make_chat_completion(self, system_prompt: str, user_prompt: str) -> str:
        """Make a chat completion request to Ollama"""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing response: {str(e)}"
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Ollama and return status"""
        try:
            # Test basic connectivity
            models_response = requests.get(f"{self.base_url}/models", timeout=5)
            
            if models_response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"Ollama server returned status {models_response.status_code}",
                    "available": False
                }
            
            # Test model availability
            models = models_response.json().get('models', [])
            model_names = [model.get('name', '') for model in models]
            
            if self.model not in model_names:
                return {
                    "status": "warning",
                    "message": f"Model {self.model} not found. Available models: {', '.join(model_names)}",
                    "available": False,
                    "available_models": model_names
                }
            
            # Test chat completion
            test_response = self._make_chat_completion(
                "You are a helpful assistant.",
                "Say 'Hello, Ollama is working!'"
            )
            
            if "Hello" in test_response or "working" in test_response.lower():
                return {
                    "status": "success",
                    "message": "Ollama is working correctly",
                    "available": True,
                    "model": self.model,
                    "available_models": model_names
                }
            else:
                return {
                    "status": "warning",
                    "message": "Ollama responded but may not be working as expected",
                    "available": True,
                    "model": self.model,
                    "available_models": model_names
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": "Cannot connect to Ollama server. Make sure it's running on localhost:11434",
                "available": False
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "available": False
            } 