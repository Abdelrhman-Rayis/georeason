# Mundi GIS Application

A Django-based Geographic Information System (GIS) application that integrates with [Mundi AI](https://docs.mundi.ai/), an open-source, AI-native GIS platform.

## Features

- **Map Project Management**: Create, edit, and organize geographic data projects
- **Layer Upload**: Support for multiple GIS file formats (GeoJSON, Shapefile, GeoTIFF, LAS/LAZ, CSV)
- **Map Rendering**: Generate high-quality map images for reports and presentations
- **AI-Powered Analysis**: Integration with Mundi AI for advanced geospatial analysis
- **Modern UI**: Beautiful, responsive interface built with Bootstrap 5
- **User Management**: Secure user authentication and project ownership

## Supported File Formats

### Vector Data
- **GeoJSON (.geojson)** - Points, lines, polygons
- **Shapefile (.shp)** - ESRI shapefile format
- **CSV (.csv)** - Point data with coordinates

### Raster & Point Cloud Data
- **GeoTIFF (.tif)** - Satellite imagery, elevation data
- **LAS/LAZ (.las/.laz)** - LiDAR point cloud data

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in your project root:
   ```env
   SECRET_KEY=your-django-secret-key
   MUNDI_API_BASE_URL=https://app.mundi.ai/api
   MUNDI_API_KEY=your-mundi-api-key
   ```

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Getting Started

1. **Access the Application**
   - Navigate to `http://localhost:8000/mundi/`
   - Login with your credentials

2. **Create Your First Project**
   - Click "New Project" from the dashboard
   - Enter a descriptive name and description
   - Save the project

3. **Upload Layers**
   - Navigate to your project
   - Click "Upload Layer"
   - Select your GIS file and configure settings
   - Upload the layer

4. **Render Maps**
   - From your project page, click "Render Map"
   - Configure dimensions and format
   - Generate your map image

### API Integration

The application integrates with Mundi AI's API for:
- Map project creation and management
- Layer upload and processing
- Map rendering and styling
- Webhook notifications

### File Upload Guidelines

- **Maximum file size**: 100MB
- **Coordinate Reference System**: Ensure your files have proper CRS
- **CSV files**: Must include latitude and longitude columns
- **Shapefiles**: Include all related files (.shp, .shx, .dbf, etc.)

## Project Structure

```
mundi_gis/
├── models.py          # Database models
├── views.py           # View logic and API integration
├── forms.py           # Form definitions
├── admin.py           # Django admin configuration
├── urls.py            # URL routing
└── templates/         # HTML templates
    └── mundi_gis/
        ├── base.html
        ├── dashboard.html
        ├── project_list.html
        ├── project_detail.html
        ├── project_form.html
        ├── layer_upload.html
        └── render_map.html
```

## Models

### MundiMapProject
- Stores map project information
- Links to Mundi AI project IDs
- User ownership and metadata

### MundiLayer
- Manages uploaded GIS layers
- Supports multiple file formats
- Style configuration storage

### MundiMapRender
- Tracks generated map images
- Stores render metadata
- Links to project and layer data

## Configuration

### Mundi AI Integration

To use the full features of this application, you'll need:

1. **Mundi AI Account**: Sign up at [app.mundi.ai](https://app.mundi.ai)
2. **API Key**: Obtain your API key from the Mundi dashboard
3. **Environment Setup**: Configure your API credentials in `.env`

### Development vs Production

- **Development**: Uses local file storage and SQLite database
- **Production**: Configure for PostgreSQL and cloud storage
- **Media Files**: Set up proper media file serving for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation**: [Mundi AI Docs](https://docs.mundi.ai/)
- **Issues**: Report bugs and feature requests via GitHub issues
- **Community**: Join the Mundi AI community for support and discussions

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Powered by [Mundi AI](https://docs.mundi.ai/)
- UI components from [Bootstrap](https://getbootstrap.com/)
- Icons from [Font Awesome](https://fontawesome.com/) 