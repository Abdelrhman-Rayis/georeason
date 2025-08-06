// Mundi GIS Map Management
class MundiMap {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.map = null;
        this.layers = [];
        this.options = {
            center: [0, 0],
            zoom: 2,
            minZoom: 1,
            maxZoom: 18,
            ...options
        };
        this.init();
    }

    init() {
        console.log('Initializing MundiMap for container:', this.containerId);
        
        // Check if container exists
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error('Map container not found:', this.containerId);
            return;
        }
        
        console.log('Container dimensions:', container.offsetWidth, 'x', container.offsetHeight);
        
        // Initialize the map
        this.map = L.map(this.containerId, {
            center: this.options.center,
            zoom: this.options.zoom,
            minZoom: this.options.minZoom,
            maxZoom: this.options.maxZoom,
            zoomControl: true,
            attributionControl: true
        });

        console.log('Map initialized, adding base layer...');
        
        // Add OpenStreetMap base layer
        this.addBaseLayer();
        
        // Add layer control
        this.layerControl = L.control.layers(null, null, {
            collapsed: false,
            position: 'topright'
        }).addTo(this.map);

        // Add scale control
        L.control.scale({
            position: 'bottomleft',
            metric: true,
            imperial: true
        }).addTo(this.map);

        // Add fullscreen control
        this.addFullscreenControl();

        // Add search control
        this.addSearchControl();

        // Add drawing tools
        this.addDrawingTools();

        console.log('Mundi Map initialized');
    }

    addBaseLayer() {
        console.log('Adding base layers...');
        
        // OpenStreetMap base layer
        const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        });

        // CartoDB Positron (light theme)
        const cartoPositron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        });

        // CartoDB Dark Matter (dark theme)
        const cartoDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        });

        // Satellite imagery
        const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 19
        });

        // Add base layers to control
        this.layerControl.addBaseLayer(osmLayer, 'OpenStreetMap');
        this.layerControl.addBaseLayer(cartoPositron, 'CartoDB Light');
        this.layerControl.addBaseLayer(cartoDark, 'CartoDB Dark');
        this.layerControl.addBaseLayer(satellite, 'Satellite');

        // Set default base layer
        console.log('Adding OpenStreetMap layer to map...');
        osmLayer.addTo(this.map);
        
        // Force map refresh
        setTimeout(() => {
            console.log('Forcing map refresh...');
            this.map.invalidateSize();
        }, 100);
    }
    }

    addFullscreenControl() {
        // Simple fullscreen control
        const fullscreenControl = L.Control.extend({
            options: {
                position: 'topright'
            },

            onAdd: function(map) {
                const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
                const button = L.DomUtil.create('a', 'leaflet-control-fullscreen', container);
                button.innerHTML = '<i class="fas fa-expand"></i>';
                button.title = 'Toggle Fullscreen';
                button.style.width = '30px';
                button.style.height = '30px';
                button.style.lineHeight = '30px';
                button.style.textAlign = 'center';

                button.onclick = function() {
                    const elem = document.getElementById(map._container.id);
                    if (!document.fullscreenElement) {
                        elem.requestFullscreen().catch(err => {
                            console.log('Error attempting to enable fullscreen:', err);
                        });
                    } else {
                        document.exitFullscreen();
                    }
                };

                return container;
            }
        });

        this.map.addControl(new fullscreenControl());
    }

    addSearchControl() {
        // Simple search control
        const searchControl = L.Control.extend({
            options: {
                position: 'topleft'
            },

            onAdd: function(map) {
                const container = L.DomUtil.create('div', 'leaflet-control-search', map.getContainer());
                container.style.cssText = `
                    background: white;
                    padding: 5px;
                    border-radius: 4px;
                    box-shadow: 0 1px 5px rgba(0,0,0,0.4);
                    margin: 10px;
                `;

                const input = L.DomUtil.create('input', 'search-input', container);
                input.type = 'text';
                input.placeholder = 'Search location...';
                input.style.cssText = `
                    width: 200px;
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    font-size: 12px;
                `;

                const button = L.DomUtil.create('button', 'search-button', container);
                button.innerHTML = '<i class="fas fa-search"></i>';
                button.style.cssText = `
                    margin-left: 5px;
                    padding: 5px 10px;
                    background: #007cbf;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    cursor: pointer;
                `;

                button.onclick = function() {
                    const query = input.value;
                    if (query) {
                        // Use Nominatim for geocoding
                        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`)
                            .then(response => response.json())
                            .then(data => {
                                if (data.length > 0) {
                                    const result = data[0];
                                    const lat = parseFloat(result.lat);
                                    const lon = parseFloat(result.lon);
                                    map.setView([lat, lon], 12);
                                    
                                    // Add a marker
                                    L.marker([lat, lon])
                                        .addTo(map)
                                        .bindPopup(`<b>${result.display_name}</b>`)
                                        .openPopup();
                                } else {
                                    alert('Location not found');
                                }
                            })
                            .catch(error => {
                                console.error('Search error:', error);
                                alert('Search failed');
                            });
                    }
                };

                return container;
            }
        });

        this.map.addControl(new searchControl());
    }

    addDrawingTools() {
        // Initialize draw control
        const drawnItems = new L.FeatureGroup();
        this.map.addLayer(drawnItems);

        const drawControl = new L.Control.Draw({
            draw: {
                polygon: {
                    allowIntersection: false,
                    drawError: {
                        color: '#e1e100',
                        message: '<strong>Oh snap!<strong> you can\'t draw that!'
                    },
                    shapeOptions: {
                        color: '#bada55'
                    }
                },
                circle: {
                    shapeOptions: {
                        color: '#662d91'
                    }
                },
                rectangle: {
                    shapeOptions: {
                        color: '#662d91'
                    }
                },
                polyline: {
                    shapeOptions: {
                        color: '#662d91'
                    }
                },
                marker: {
                    icon: L.divIcon({
                        className: 'custom-marker',
                        html: '<i class="fas fa-map-marker-alt" style="color: #e74c3c; font-size: 24px;"></i>',
                        iconSize: [24, 24],
                        iconAnchor: [12, 24]
                    })
                }
            },
            edit: {
                featureGroup: drawnItems,
                remove: true
            }
        });

        this.map.addControl(drawControl);

        // Handle draw events
        this.map.on('draw:created', (e) => {
            const layer = e.layer;
            drawnItems.addLayer(layer);
            
            // Add popup with layer info
            const layerType = e.layerType;
            const popupContent = `
                <div>
                    <h6>${layerType.charAt(0).toUpperCase() + layerType.slice(1)}</h6>
                    <p>Created: ${new Date().toLocaleString()}</p>
                    <button onclick="exportLayer('${layerType}')" class="btn btn-sm btn-primary">
                        <i class="fas fa-download"></i> Export
                    </button>
                </div>
            `;
            
            layer.bindPopup(popupContent);
        });

        this.map.on('draw:edited', (e) => {
            const layers = e.layers;
            layers.eachLayer((layer) => {
                // Handle edited layers
                console.log('Layer edited:', layer);
            });
        });

        this.map.on('draw:deleted', (e) => {
            const layers = e.layers;
            layers.eachLayer((layer) => {
                // Handle deleted layers
                console.log('Layer deleted:', layer);
            });
        });
    }

    // Add a GeoJSON layer
    addGeoJSONLayer(geojson, options = {}) {
        const defaultOptions = {
            style: {
                color: '#3388ff',
                weight: 2,
                opacity: 0.8,
                fillOpacity: 0.2
            },
            pointToLayer: (feature, latlng) => {
                return L.circleMarker(latlng, {
                    radius: 6,
                    fillColor: '#3388ff',
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            },
            onEachFeature: (feature, layer) => {
                if (feature.properties) {
                    const popupContent = `
                        <div>
                            <h6>${feature.properties.name || 'Feature'}</h6>
                            <p>${JSON.stringify(feature.properties, null, 2)}</p>
                        </div>
                    `;
                    layer.bindPopup(popupContent);
                }
            }
        };

        const layerOptions = { ...defaultOptions, ...options };
        const layer = L.geoJSON(geojson, layerOptions);
        
        this.layers.push(layer);
        this.layerControl.addOverlay(layer, options.name || 'GeoJSON Layer');
        layer.addTo(this.map);

        // Fit map to layer bounds if it's the first layer
        if (this.layers.length === 1) {
            this.map.fitBounds(layer.getBounds());
        }

        return layer;
    }

    // Add a marker
    addMarker(lat, lng, options = {}) {
        const defaultOptions = {
            title: 'Marker',
            popup: 'Marker'
        };

        const markerOptions = { ...defaultOptions, ...options };
        const marker = L.marker([lat, lng], markerOptions);
        
        if (markerOptions.popup) {
            marker.bindPopup(markerOptions.popup);
        }

        this.layers.push(marker);
        this.layerControl.addOverlay(marker, markerOptions.title);
        marker.addTo(this.map);

        return marker;
    }

    // Remove a layer
    removeLayer(layer) {
        const index = this.layers.indexOf(layer);
        if (index > -1) {
            this.layers.splice(index, 1);
            this.map.removeLayer(layer);
            this.layerControl.removeLayer(layer);
        }
    }

    // Clear all layers
    clearLayers() {
        this.layers.forEach(layer => {
            this.map.removeLayer(layer);
            this.layerControl.removeLayer(layer);
        });
        this.layers = [];
    }

    // Get map bounds
    getBounds() {
        return this.map.getBounds();
    }

    // Set map view
    setView(lat, lng, zoom) {
        this.map.setView([lat, lng], zoom);
    }

    // Export map as image
    exportMap() {
        // This would require additional libraries like html2canvas
        console.log('Export functionality would be implemented here');
    }
}

// Global function to export layers
function exportLayer(layerType) {
    console.log(`Exporting ${layerType} layer`);
    // Implementation would depend on the specific layer type
}

// Initialize map when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Auto-initialize map if container exists
    const mapContainer = document.getElementById('mundi-map');
    if (mapContainer) {
        window.mundiMap = new MundiMap('mundi-map', {
            center: [0, 0],
            zoom: 2
        });
    }
}); 