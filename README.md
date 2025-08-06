# Zoal AI - AI-Powered Chatbot & GIS Platform

A comprehensive Django application featuring an AI-powered chatbot with knowledge about Sudanese and African culture, plus a modern Geographic Information System (GIS) powered by Mundi AI.

## 🌟 Features

### 🤖 AI Chatbot
- **Multi-Model Support**: OpenAI GPT-3.5 and Google Gemini integration
- **Cultural Knowledge**: Specialized in Sudanese and African culture
- **Session Management**: Persistent chat history and context
- **Real-time Responses**: Fast, intelligent AI responses
- **Modern UI**: Beautiful, responsive chat interface

### 🗺️ Mundi GIS Platform
- **Map Project Management**: Create, edit, and organize geographic data projects
- **Multi-Format Support**: GeoJSON, Shapefile, GeoTIFF, LAS/LAZ, CSV
- **AI-Powered Analysis**: Integration with Mundi AI for advanced geospatial analysis
- **Map Rendering**: Generate high-quality map images for reports
- **Modern Dashboard**: Beautiful, responsive interface with statistics
- **User Management**: Secure authentication and project ownership

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <your-github-repo-url>
   cd zoal_ai
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   # Django Settings
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   
   # AI API Keys
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-api-key
   
   # Mundi AI Integration
   MUNDI_API_BASE_URL=https://app.mundi.ai/api
   MUNDI_API_KEY=your-mundi-api-key
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 📱 Usage

### AI Chatbot
- **Access**: `http://localhost:8000/`
- **Features**: 
  - Choose between OpenAI and Google AI models
  - Chat about Sudanese and African culture
  - View chat history
  - Real-time responses

### Mundi GIS Platform
- **Access**: `http://localhost:8000/mundi/`
- **Login**: Use your superuser credentials
- **Features**:
  - Create map projects
  - Upload GIS layers
  - Render maps
  - Manage geographic data

### Admin Interface
- **Access**: `http://localhost:8000/admin/`
- **Features**: Manage users, projects, and system settings

## 🏗️ Project Structure

```
zoal_ai/
├── chatbot/                 # AI Chatbot Application
│   ├── models.py           # Chat session and message models
│   ├── views.py            # Chat interface and AI integration
│   ├── urls.py             # Chatbot URL routing
│   └── templates/          # Chat interface templates
│
├── mundi_gis/              # GIS Platform Application
│   ├── models.py           # Map projects, layers, renders
│   ├── views.py            # GIS management views
│   ├── forms.py            # Data input forms
│   ├── admin.py            # Django admin configuration
│   ├── urls.py             # GIS URL routing
│   └── templates/          # GIS interface templates
│
├── zoal_ai/                # Main Django Project
│   ├── settings.py         # Django configuration
│   ├── urls.py             # Main URL routing
│   └── views.py            # Authentication views
│
├── templates/              # Global templates
│   ├── auth/               # Authentication templates
│   └── mundi_gis/          # GIS templates
│
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Uploaded files
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

## 🔧 Configuration

### AI Models Configuration

#### OpenAI Integration
1. Get your API key from [OpenAI Platform](https://platform.openai.com/)
2. Add to `.env`: `OPENAI_API_KEY=your-key-here`
3. The chatbot will use GPT-3.5-turbo by default

#### Google Gemini Integration
1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GOOGLE_API_KEY=your-key-here`
3. The chatbot will use Gemini 1.5 Flash

### Mundi AI Integration
1. Sign up at [app.mundi.ai](https://app.mundi.ai)
2. Get your API key from the Mundi dashboard
3. Add to `.env`:
   ```env
   MUNDI_API_BASE_URL=https://app.mundi.ai/api
   MUNDI_API_KEY=your-mundi-api-key
   ```

## 📊 Supported GIS File Formats

### Vector Data
- **GeoJSON (.geojson)** - Points, lines, polygons
- **Shapefile (.shp)** - ESRI shapefile format
- **CSV (.csv)** - Point data with coordinates

### Raster & Point Cloud Data
- **GeoTIFF (.tif)** - Satellite imagery, elevation data
- **LAS/LAZ (.las/.laz)** - LiDAR point cloud data

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Code Style
```bash
# Install development dependencies
pip install black flake8

# Format code
black .

# Check code style
flake8 .
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Set up SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "zoal_ai.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django**: Web framework
- **OpenAI**: GPT-3.5-turbo integration
- **Google AI**: Gemini integration
- **Mundi AI**: GIS platform integration
- **Bootstrap**: UI components
- **Font Awesome**: Icons

## 📞 Support

- **Issues**: Report bugs and feature requests via GitHub issues
- **Documentation**: Check the inline code documentation
- **Community**: Join our community discussions

## 🔄 Version History

- **v1.0.0**: Initial release with chatbot and basic GIS functionality
- **v1.1.0**: Added Mundi AI integration and advanced GIS features
- **v1.2.0**: Enhanced UI and authentication system

---

**Built with ❤️ for the Sudanese and African community** 