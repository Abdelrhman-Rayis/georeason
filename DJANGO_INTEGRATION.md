# Django-Mundi.ai Integration

## Overview

This document describes the integration of our Django-based Mundi GIS application with the official [Mundi.ai](https://github.com/BuntingLabs/mundi.ai) project. This integration combines the best features of both platforms to create a powerful, AI-native GIS solution.

## What's Been Integrated

### ✅ Local LLM Integration
- **Ollama Support**: Full integration with Ollama for local AI processing
- **AI Analysis**: GIS layer analysis using local LLM
- **Project Descriptions**: AI-generated project descriptions
- **Styling Suggestions**: AI-powered layer styling recommendations
- **Health Monitoring**: Real-time LLM service health checks

### ✅ API Endpoints Added
- `GET /api/local-llm/status` - Check LLM availability
- `GET /api/local-llm/models` - List available Ollama models
- `POST /api/local-llm/analyze-layer` - Analyze GIS layers
- `POST /api/local-llm/generate-description` - Generate project descriptions
- `POST /api/local-llm/suggest-styling` - Get styling suggestions
- `POST /api/local-llm/chat` - General chat completion
- `GET /api/local-llm/health` - Health check

### ✅ Features Preserved from Django App
- **OpenStreetMap Integration**: Leaflet.js mapping capabilities
- **File Upload**: GeoJSON and spatial data upload
- **User Authentication**: User management system
- **Interactive Mapping**: Drawing tools and layer management
- **AI-Powered Analysis**: Local LLM integration

## Architecture

### Backend Integration
```
Mundi.ai (FastAPI)
├── Core GIS Features
├── PostGIS Integration
├── QGIS Processing
└── Local LLM Integration (NEW)
    ├── Ollama Service
    ├── AI Analysis
    ├── Styling Suggestions
    └── Health Monitoring
```

### Frontend Integration
```
Mundi.ai Frontend (TypeScript/React)
├── Modern GIS Interface
├── Real-time Collaboration
└── Local LLM Features (NEW)
    ├── AI Analysis UI
    ├── Model Selection
    └── Health Status
```

## Setup Instructions

### 1. Prerequisites
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., gemma3:4b)
ollama pull gemma3:4b

# Start Ollama service
ollama serve
```

### 2. Environment Configuration
```bash
# Add to your .env file
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gemma3:4b
OLLAMA_API_KEY=ollama
```

### 3. Start Mundi.ai with Local LLM
```bash
# Clone the integrated repository
git clone <your-forked-repo>
cd mundi.ai

# Start with Docker Compose
docker-compose up -d

# Or run locally
pip install -r requirements.txt
uvicorn src.wsgi:app --host 0.0.0.0 --port 8000 --reload
```

## Usage Examples

### 1. Check LLM Status
```bash
curl http://localhost:8000/api/local-llm/status
```

### 2. Analyze a GIS Layer
```bash
curl -X POST http://localhost:8000/api/local-llm/analyze-layer \
  -H "Content-Type: application/json" \
  -d '{
    "layer_id": "layer-123",
    "question": "What can you tell me about this data?",
    "layer_info": {
      "name": "Population Data",
      "layer_type": "vector",
      "feature_count": 1000,
      "geometry_type": "Point"
    }
  }'
```

### 3. Generate Project Description
```bash
curl -X POST http://localhost:8000/api/local-llm/generate-description \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "project-456",
    "project_info": {
      "name": "Urban Planning Project",
      "description": "City development analysis",
      "layer_count": 5
    }
  }'
```

## Benefits of Integration

### For Users
- **Best of Both Worlds**: Mundi.ai's advanced GIS + local AI capabilities
- **Privacy**: All AI processing happens locally with Ollama
- **Cost-Effective**: No external API costs for AI features
- **Flexibility**: Choose between cloud and local deployment
- **Enhanced AI**: Combined AI approaches for better analysis

### For Developers
- **Modern Stack**: FastAPI + TypeScript + React
- **Scalable Architecture**: Microservices-ready design
- **Open Source**: Full AGPL-3.0 licensed solution
- **Active Community**: Join Mundi.ai's growing ecosystem
- **Standards Compliant**: Follow GIS industry standards

## Migration Path

### From Django App
1. **Data Export**: Export your existing data
2. **Feature Mapping**: Map Django features to Mundi.ai equivalents
3. **User Migration**: Migrate user accounts and permissions
4. **Training**: Provide documentation for new interface

### For New Users
1. **One-Click Setup**: Docker Compose deployment
2. **Comprehensive Features**: All features available out of the box
3. **Documentation**: Complete user and developer guides
4. **Community Support**: Active community and forums

## Development

### Adding New LLM Features
1. **Extend LocalLLMService**: Add new methods to `src/local_llm.py`
2. **Create API Routes**: Add endpoints to `src/routes/local_llm_routes.py`
3. **Update Frontend**: Add UI components in `frontendts/src/`
4. **Test Integration**: Add tests in `src/test_*.py`

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## Troubleshooting

### Common Issues

#### Ollama Not Available
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

#### Model Not Found
```bash
# List available models
ollama list

# Pull the required model
ollama pull gemma3:4b
```

#### API Connection Issues
```bash
# Check API health
curl http://localhost:8000/api/local-llm/health

# Verify environment variables
echo $OLLAMA_BASE_URL
echo $OLLAMA_MODEL
```

## Future Enhancements

### Planned Features
- **Advanced AI Models**: Support for more Ollama models
- **Batch Processing**: Process multiple layers simultaneously
- **Custom Prompts**: User-defined analysis prompts
- **Model Fine-tuning**: Custom model training capabilities
- **Performance Optimization**: Caching and optimization

### Integration Roadmap
- **Phase 1**: Core LLM integration ✅
- **Phase 2**: Advanced AI features
- **Phase 3**: Performance optimization
- **Phase 4**: Community features

## License

This integration maintains the AGPL-3.0 license of the original Mundi.ai project while adding local LLM capabilities. All contributions must comply with the license terms.

## Support

- **Documentation**: [docs.mundi.ai](https://docs.mundi.ai)
- **Community**: [GitHub Discussions](https://github.com/BuntingLabs/mundi.ai/discussions)
- **Issues**: [GitHub Issues](https://github.com/BuntingLabs/mundi.ai/issues)
- **Discord**: [Mundi.ai Discord](https://discord.gg/mundi-ai)

## Conclusion

This integration successfully combines the power of Mundi.ai's modern GIS platform with the flexibility and privacy of local AI processing. Users now have access to a comprehensive, AI-native GIS solution that can run entirely locally while maintaining all the advanced features of the original Mundi.ai platform.

The integration is designed to be:
- **Easy to deploy**: One-command setup with Docker
- **Privacy-focused**: All AI processing happens locally
- **Cost-effective**: No external API dependencies
- **Extensible**: Easy to add new features and models
- **Community-driven**: Open source and actively maintained 