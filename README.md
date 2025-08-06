# GeoReason: AI-Powered GIS Platform

## 🌍 Overview

GeoReason is a comprehensive AI-powered Geographic Information System (GIS) platform that combines the best features of Django-based GIS applications with the modern [Mundi.ai](https://github.com/BuntingLabs/mundi.ai) platform. This project provides both a standalone Django application and an integrated solution with the official Mundi.ai project.

## 🚀 Features

### ✅ Core GIS Capabilities
- **Interactive Mapping**: OpenStreetMap integration with Leaflet.js
- **File Upload**: Support for GeoJSON, Shapefiles, and other spatial data formats
- **Layer Management**: Advanced layer organization and styling
- **Project Management**: Create, organize, and manage GIS projects
- **User Authentication**: Secure user management system

### 🤖 AI-Powered Features
- **Local LLM Integration**: Full Ollama support for local AI processing
- **GIS Analysis**: AI-powered spatial data analysis
- **Project Descriptions**: AI-generated project descriptions
- **Styling Suggestions**: AI recommendations for layer styling
- **Real-time Analysis**: Interactive AI chat for GIS queries

### 🏗️ Architecture Options

#### Option 1: Django Application (Current)
- **Framework**: Django 5.1.4
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **Frontend**: Bootstrap 5 + Leaflet.js
- **AI**: Local Ollama integration
- **Deployment**: Simple Django deployment

#### Option 2: Mundi.ai Integration (Advanced)
- **Framework**: FastAPI + TypeScript + React
- **Database**: PostgreSQL with PostGIS
- **Frontend**: Modern React interface
- **AI**: Enhanced local LLM + cloud AI options
- **Deployment**: Docker Compose with microservices

## 📦 Installation

### Prerequisites
```bash
# Install Python 3.11+
python3 --version

# Install Ollama for local AI
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (e.g., gemma3:4b)
ollama pull gemma3:4b
```

### Quick Start (Django Version)
```bash
# Clone the repository
git clone https://github.com/Abdelrhman-Rayis/georeason.git
cd georeason

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Start the development server
python3 manage.py runserver

# Start Ollama (in another terminal)
ollama serve
```

### Advanced Setup (Mundi.ai Integration)
```bash
# Clone the Mundi.ai integration branch
git clone -b mundi-integration https://github.com/Abdelrhman-Rayis/georeason.git
cd georeason

# Start with Docker Compose
docker-compose up -d

# Or run locally
pip install -r requirements.txt
uvicorn src.wsgi:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Configuration

### Environment Variables
```bash
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gemma3:4b
OLLAMA_API_KEY=ollama

# Mundi.ai Settings (for integration)
MUNDI_API_KEY=your-mundi-api-key
POSTGRES_HOST=localhost
POSTGRES_DB=georeason
POSTGRES_USER=georeason_user
POSTGRES_PASSWORD=your-password
```

## 🎯 Usage

### 1. Create a Project
1. Navigate to `/mundi/` (Django) or the main interface (Mundi.ai)
2. Click "Create New Project"
3. Enter project name and description
4. Start adding layers

### 2. Upload Spatial Data
1. Select your project
2. Click "Upload Layer"
3. Choose your file (GeoJSON, Shapefile, etc.)
4. Configure layer settings
5. View on the interactive map

### 3. AI Analysis
1. Select a layer
2. Click "AI Analysis"
3. Ask questions about your data
4. Get AI-powered insights and suggestions

### 4. Interactive Mapping
- **Zoom/Pan**: Navigate the map
- **Layer Control**: Toggle layer visibility
- **Drawing Tools**: Add markers, lines, polygons
- **Search**: Find locations worldwide
- **Fullscreen**: Toggle fullscreen mode

## 🔌 API Endpoints

### Local LLM API (Mundi.ai Integration)
- `GET /api/local-llm/status` - Check LLM availability
- `GET /api/local-llm/models` - List available Ollama models
- `POST /api/local-llm/analyze-layer` - Analyze GIS layers
- `POST /api/local-llm/generate-description` - Generate project descriptions
- `POST /api/local-llm/suggest-styling` - Get styling suggestions
- `POST /api/local-llm/chat` - General chat completion
- `GET /api/local-llm/health` - Health check

### Example API Usage
```bash
# Check LLM status
curl http://localhost:8000/api/local-llm/status

# Analyze a layer
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

## 🏗️ Project Structure

```
georeason/
├── chatbot/                 # Django chatbot app
├── mundi_gis/              # Django GIS app
│   ├── models.py           # GIS data models
│   ├── views.py            # GIS views and logic
│   ├── local_llm.py        # Ollama integration
│   └── templates/          # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── templates/              # Base templates
├── media/                  # Uploaded files
├── requirements.txt        # Python dependencies
├── manage.py              # Django management
├── INTEGRATION_PLAN.md     # Mundi.ai integration plan
├── DJANGO_INTEGRATION.md   # Technical integration guide
└── README.md              # This file
```

## 🔄 Migration Path

### From Django to Mundi.ai Integration
1. **Export Data**: Use Django admin to export your data
2. **Setup Mundi.ai**: Follow the integration guide
3. **Import Data**: Use Mundi.ai's data import tools
4. **Configure AI**: Set up Ollama and models
5. **Test Features**: Verify all functionality works

### Benefits of Migration
- **Modern Stack**: FastAPI + TypeScript + React
- **Scalability**: Microservices architecture
- **Advanced Features**: Enhanced AI capabilities
- **Community**: Active Mundi.ai community
- **Standards**: Industry-standard GIS tools

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python3 manage.py test

# Run linting
flake8 .
black .
```

## 📚 Documentation

- [Integration Plan](INTEGRATION_PLAN.md) - Comprehensive integration strategy
- [Django Integration](DJANGO_INTEGRATION.md) - Technical implementation guide
- [Mundi.ai Documentation](https://docs.mundi.ai) - Official Mundi.ai docs
- [API Reference](https://docs.mundi.ai/api) - API documentation

## 🐛 Troubleshooting

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

#### Database Issues
```bash
# Reset migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser
```

## 📄 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Mundi.ai](https://github.com/BuntingLabs/mundi.ai) - The amazing open-source GIS platform
- [Ollama](https://ollama.ai) - Local LLM framework
- [OpenStreetMap](https://openstreetmap.org) - Open mapping data
- [Leaflet.js](https://leafletjs.com) - Interactive maps library
- [Django](https://djangoproject.com) - Web framework
- [FastAPI](https://fastapi.tiangolo.com) - Modern API framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Abdelrhman-Rayis/georeason/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Abdelrhman-Rayis/georeason/discussions)
- **Documentation**: [Project Wiki](https://github.com/Abdelrhman-Rayis/georeason/wiki)
- **Mundi.ai Community**: [Discord](https://discord.gg/mundi-ai)

Demo
<img width="2992" height="2396" alt="Image" src="https://github.com/user-attachments/assets/bab2904f-5f8b-4d81-b585-f713e638ddaa" />

---

 
 
