# Wildlife Poacher Detection System

A comprehensive machine learning-based system for detecting and monitoring wildlife poaching activities in protected areas. This application combines object detection, anomaly detection, and real-time alerting to help rangers and wildlife protection teams prevent poaching incidents.

## Features

- **Object Detection**: Identify poachers, animals, vehicles, and rangers in surveillance footage using deep learning models
- **Anomaly Detection**: Detect unusual movement patterns, night activities, zone breaches, and noise anomalies using ML algorithms
- **Real-time Monitoring**: Interactive dashboard displaying live alerts and threat assessments
- **Geospatial Analysis**: Heat maps and location-based visualization of detected threats
- **Role-based Access Control**: Support for different user roles (Admin, Ranger, Analyst, Researcher)
- **Analytics & Reporting**: Performance metrics, ROC curves, and confusion matrices for model evaluation

## Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Folium
- **ML/Statistics**: Scikit-learn
- **Reporting**: ReportLab

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd animal-poaching-detection
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Demo Credentials

- **Admin**: admin / admin123
- **Ranger**: ranger / ranger123
- **Analyst**: analyst / analyst123
- **Researcher**: researcher / researcher123

## Project Structure

```
├── app.py                      # Main Streamlit application
├── object_detection.py         # Object detection model
├── anomaly_detection.py        # Anomaly detection system
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
└── 2025-08-30T04-23_export.csv # Sample data
```

## Components

### Object Detection (`object_detection.py`)
Detects and classifies objects in surveillance images:
- **Classes**: Poacher, Animal, Vehicle, Ranger
- Returns bounding boxes and confidence scores
- Ready for integration with YOLO or EfficientDet models

### Anomaly Detection (`anomaly_detection.py`)
Identifies unusual patterns and behaviors:
- **Anomaly Types**: Unusual Movement, Night Activity, Zone Breach, Noise Spike
- **Severity Levels**: Low, Medium, High
- Uses isolation forest or autoencoder approach (extensible)

### Main Application (`app.py`)
Comprehensive dashboard featuring:
- User authentication and role management
- Alert management and filtering
- Real-time data visualization
- Geospatial mapping with heat maps
- Model performance metrics

## Future Enhancements

- Integration with actual YOLO/EfficientDet models
- Real Isolation Forest/Autoencoder implementation
- Live camera feed processing
- Mobile app integration
- Database backend for persistent storage
- Advanced temporal analysis
- Sound/Acoustic detection capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or feedback, please reach out through GitHub issues.

---

**Note**: This system is designed to assist wildlife protection teams. Always combine automated detection with trained personnel for best results.
