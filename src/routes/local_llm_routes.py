"""
Local LLM Integration Routes for Mundi.ai
Integrates Ollama-based local LLM capabilities with Mundi.ai's AI features
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import json
from ..local_llm import LocalLLMService

router = APIRouter(prefix="/local-llm", tags=["Local LLM"])

# Initialize LLM service
llm_service = LocalLLMService()

class LayerAnalysisRequest(BaseModel):
    layer_id: str
    question: str
    layer_info: Dict[str, Any]

class ProjectDescriptionRequest(BaseModel):
    project_id: str
    project_info: Dict[str, Any]

class StylingRequest(BaseModel):
    layer_id: str
    layer_info: Dict[str, Any]

@router.get("/status")
async def get_llm_status():
    """Check if local LLM (Ollama) is available"""
    try:
        status = llm_service.test_connection()
        return {
            "available": llm_service.is_available(),
            "status": status,
            "model": llm_service.model,
            "base_url": llm_service.base_url
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "model": llm_service.model,
            "base_url": llm_service.base_url
        }

@router.get("/models")
async def get_available_models():
    """Get list of available Ollama models"""
    try:
        models = llm_service.get_available_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

@router.post("/analyze-layer")
async def analyze_layer(request: LayerAnalysisRequest):
    """Analyze a GIS layer using local LLM"""
    try:
        if not llm_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="Local LLM (Ollama) is not available. Please ensure Ollama is running."
            )
        
        analysis = llm_service.analyze_gis_data(request.layer_info, request.question)
        
        return {
            "layer_id": request.layer_id,
            "question": request.question,
            "analysis": analysis,
            "model": llm_service.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/generate-description")
async def generate_project_description(request: ProjectDescriptionRequest):
    """Generate AI description for a project"""
    try:
        if not llm_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="Local LLM (Ollama) is not available. Please ensure Ollama is running."
            )
        
        description = llm_service.generate_map_description(request.project_info)
        
        return {
            "project_id": request.project_id,
            "description": description,
            "model": llm_service.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Description generation failed: {str(e)}")

@router.post("/suggest-styling")
async def suggest_layer_styling(request: StylingRequest):
    """Get AI suggestions for layer styling"""
    try:
        if not llm_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="Local LLM (Ollama) is not available. Please ensure Ollama is running."
            )
        
        styling_suggestions = llm_service.suggest_layer_styling(request.layer_info)
        
        return {
            "layer_id": request.layer_id,
            "styling": styling_suggestions,
            "model": llm_service.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Styling suggestion failed: {str(e)}")

@router.post("/chat")
async def chat_completion(system_prompt: str, user_prompt: str):
    """General chat completion with local LLM"""
    try:
        if not llm_service.is_available():
            raise HTTPException(
                status_code=503, 
                detail="Local LLM (Ollama) is not available. Please ensure Ollama is running."
            )
        
        response = llm_service._make_chat_completion(system_prompt, user_prompt)
        
        return {
            "response": response,
            "model": llm_service.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for local LLM service"""
    try:
        available = llm_service.is_available()
        models = llm_service.get_available_models() if available else []
        
        return {
            "service": "local-llm",
            "status": "healthy" if available else "unavailable",
            "available": available,
            "model_count": len(models),
            "current_model": llm_service.model
        }
    except Exception as e:
        return {
            "service": "local-llm",
            "status": "error",
            "available": False,
            "error": str(e)
        }
