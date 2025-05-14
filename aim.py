#!/usr/bin/env python3
"""
🔍 AIM(ADVANCED IMAGE METADATA) FORENSIC EXTRACTOR 🕵️
A professional tool for digital forensics, investigative journalism, and photography analysis.
"""

import os
import exifread
from PIL import Image, ExifTags, ImageQt
from datetime import datetime
import json
import sys
import platform
import hashlib
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QFileDialog, QTabWidget, 
                            QTreeWidget, QTreeWidgetItem, QProgressBar, QMessageBox,
                            QLineEdit, QGroupBox, QScrollArea, QSizePolicy, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QPalette, QLinearGradient, QBrush

# ======================
# 🛠️ HELPER FUNCTIONS
# ======================

def calculate_file_hashes(file_path):
    """Calculate various cryptographic hashes for forensic verification"""
    hash_functions = {
        'MD5': hashlib.md5(),
        'SHA1': hashlib.sha1(),
        'SHA256': hashlib.sha256(),
        'SHA512': hashlib.sha512(),
        'BLAKE2b': hashlib.blake2b(),
        'BLAKE2s': hashlib.blake2s()
    }
    
    hashes = {}
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                for hash_func in hash_functions.values():
                    hash_func.update(chunk)
        
        for name, hash_func in hash_functions.items():
            hashes[name] = hash_func.hexdigest()
    except Exception as e:
        for name in hash_functions.keys():
            hashes[name] = f"Error: {str(e)}"
    
    return hashes

def convert_gps_coordinates(gps_data):
    """Converts GPS coordinates from EXIF format to decimal degrees with enhanced error handling"""
    try:
        latitude = gps_data['GPSLatitude']
        lat_ref = gps_data['GPSLatitudeRef']
        longitude = gps_data['GPSLongitude']
        long_ref = gps_data['GPSLongitudeRef']
        
        # Handle different GPS coordinate formats
        def convert_coord(coord):
            if isinstance(coord, tuple) or isinstance(coord, list):
                return float(coord[0]) + float(coord[1])/60 + float(coord[2])/3600
            elif isinstance(coord, str):
                parts = coord.split(',')
                if len(parts) == 3:
                    return float(parts[0]) + float(parts[1])/60 + float(parts[2])/3600
            return float(coord)
        
        lat = convert_coord(latitude)
        if str(lat_ref).upper() != 'N':
            lat = -lat
            
        lon = convert_coord(longitude)
        if str(long_ref).upper() != 'E':
            lon = -lon
            
        return lat, lon
    except (KeyError, TypeError, ValueError, IndexError) as e:
        return None, None

def format_exif_time(time_str):
    """Formats EXIF datetime string into human-readable format with enhanced parsing"""
    try:
        # Handle various datetime formats
        time_str = str(time_str).strip()
        for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
            try:
                return datetime.strptime(time_str, fmt).strftime("%B %d, %Y at %H:%M:%S")
            except ValueError:
                continue
        return time_str  # Return original if no format matched
    except (ValueError, TypeError):
        return str(time_str)

def get_human_readable_size(size_bytes):
    """Converts bytes to human-readable format with more precise units"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size_bytes < 1024.0:
            if unit == 'B':
                return f"{size_bytes} {unit}"
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def extract_phone_info(model_str):
    """Enhanced phone brand and model extraction with more brands and patterns"""
    phone_db = {
        'iPhone': r'iPhone\s*([0-9]+[a-zA-Z]*)',
        'iPad': r'iPad\s*([0-9]+[a-zA-Z]*)',
        'Samsung': r'Samsung[-\s]*(Galaxy\s*[A-Za-z0-9]+)',
        'Huawei': r'Huawei[-\s]*([A-Za-z0-9]+)',
        'Xiaomi': r'Xiaomi[-\s]*(Mi\s*[A-Za-z0-9]+)',
        'Google': r'Google[-\s]*(Pixel\s*[0-9]+)',
        'OnePlus': r'OnePlus[-\s]*([0-9]+[A-Z]*)',
        'Sony': r'Sony[-\s]*(Xperia\s*[A-Za-z0-9]+)',
        'LG': r'LG[-\s]*([A-Za-z0-9]+)',
        'Motorola': r'Moto[-\s]*([A-Za-z0-9]+)'
    }
    
    model_str = str(model_str)
    for brand, pattern in phone_db.items():
        import re
        match = re.search(pattern, model_str, re.IGNORECASE)
        if match:
            model = match.group(1) if match.groups() else model_str.replace(brand, '').strip()
            return brand, model
    return None, model_str

def extract_thumbnail(image_path):
    """Extract embedded thumbnail if exists"""
    try:
        with Image.open(image_path) as img:
            if hasattr(img, 'thumbnail'):
                return img.thumbnail
            return None
    except Exception:
        return None

def analyze_steganography(image_path):
    """Basic steganography detection (placeholder for real analysis)"""
    try:
        with open(image_path, 'rb') as f:
            content = f.read()
            if b'Photoshop' in content:
                return "Potential Photoshop editing detected"
            if b'Steg' in content or b'steg' in content:
                return "Possible steganography markers found"
        return "No obvious steganography markers detected"
    except Exception:
        return "Steganography analysis failed"

# ======================
# 🔍 METADATA EXTRACTION
# ======================

def extract_all_metadata(image_path):
    """
    Enhanced metadata extraction with more forensic capabilities
    Returns: Dictionary with categorized metadata
    """
    metadata = {
        '⚠️ Warnings': [],
        '🔒 File Integrity': {},
        '🕵️‍♂️ Forensic Analysis': {}
    }
    
    try:
        # 🗃️ Enhanced file information with hashes
        file_stats = os.stat(image_path)
        metadata['📁 File Information'] = {
            'File Name': os.path.basename(image_path),
            'File Path': os.path.abspath(image_path),
            'File Extension': os.path.splitext(image_path)[1].upper().replace('.', ''),
            'File Size': get_human_readable_size(file_stats.st_size),
            'Created': datetime.fromtimestamp(file_stats.st_ctime).strftime("%B %d, %Y at %H:%M:%S"),
            'Modified': datetime.fromtimestamp(file_stats.st_mtime).strftime("%B %d, %Y at %H:%M:%S"),
            'Accessed': datetime.fromtimestamp(file_stats.st_atime).strftime("%B %d, %Y at %H:%M:%S"),
            'File Permissions': oct(file_stats.st_mode)[-3:]
        }
        
        # 🔒 File hashes for forensic verification
        metadata['🔒 File Integrity'] = calculate_file_hashes(image_path)
        
        # 🖼️ Open image and get basic properties
        with Image.open(image_path) as img:
            metadata['📁 File Information']['File Type'] = img.format
            metadata['📁 File Information']['MIME Type'] = Image.MIME.get(img.format, "Unknown")
            
            # 📏 Enhanced image dimensions and quality
            width, height = img.size
            metadata['📐 Image Dimensions & Quality'] = {
                'Width': f"{width} pixels",
                'Height': f"{height} pixels",
                'Megapixels': f"{(width * height) / 1000000:.2f} MP",
                'Aspect Ratio': f"{width/height:.2f}:1",
                'Color Mode': img.mode,
                'Bit Depth': getattr(img, 'bits', 'Unknown'),
                'Is Animated': getattr(img, 'is_animated', False),
                'Has Transparency': 'Yes' if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info) else 'No'
            }

            # 🕵️‍♂️ Basic forensic analysis
            metadata['🕵️‍♂️ Forensic Analysis']['Thumbnail Present'] = 'Yes' if extract_thumbnail(image_path) else 'No'
            metadata['🕵️‍♂️ Forensic Analysis']['Steganography Indicators'] = analyze_steganography(image_path)
            
            # 📷 Enhanced EXIF data extraction
            exif_data = {}
            if hasattr(img, '_getexif') and img._getexif() is not None:
                for tag_id, value in img._getexif().items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    try:
                        # Handle different data types
                        if isinstance(value, bytes):
                            try:
                                value = value.decode('utf-8', errors='replace')
                            except UnicodeDecodeError:
                                value = str(value)
                        exif_data[tag_name] = value
                    except Exception as e:
                        metadata['⚠️ Warnings'].append(f"EXIF tag {tag_name} processing error: {str(e)}")

            # 📡 Enhanced GPS data processing
            gps_info = {}
            if 'GPSInfo' in exif_data:
                try:
                    gps_data = exif_data['GPSInfo']
                    if isinstance(gps_data, dict):
                        # Handle GPSInfo as dictionary (Pillow >= 6.0)
                        gps_info_dict = gps_data
                    else:
                        # Handle GPSInfo as tuple (Pillow < 6.0)
                        gps_info_dict = {
                            1: gps_data[1],  # GPSLatitudeRef
                            2: gps_data[2],  # GPSLatitude
                            3: gps_data[3],  # GPSLongitudeRef
                            4: gps_data[4],  # GPSLongitude
                        }
                        if len(gps_data) > 5:
                            gps_info_dict[5] = gps_data[5]  # GPSAltitude
                        if len(gps_data) > 6:
                            gps_info_dict[6] = gps_data[6]  # GPSTimeStamp
                        if len(gps_data) > 16:
                            gps_info_dict[16] = gps_data[16]  # GPSImgDirection
                    
                    lat, lon = convert_gps_coordinates({
                        'GPSLatitude': gps_info_dict.get(2),
                        'GPSLatitudeRef': gps_info_dict.get(1),
                        'GPSLongitude': gps_info_dict.get(4),
                        'GPSLongitudeRef': gps_info_dict.get(3)
                    })
                    
                    if lat is not None and lon is not None:
                        gps_info['Latitude'] = f"{lat:.6f}°"
                        gps_info['Longitude'] = f"{lon:.6f}°"
                        gps_info['Google Maps Link'] = f"https://maps.google.com/?q={lat},{lon}"
                        gps_info['OpenStreetMap Link'] = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"
                        
                        if 5 in gps_info_dict:  # Altitude
                            gps_info['Altitude'] = f"{gps_info_dict[5]} meters"
                        if 6 in gps_info_dict:  # Timestamp
                            gps_info['GPS Timestamp'] = str(gps_info_dict[6])
                        if 16 in gps_info_dict:  # Direction
                            gps_info['Direction'] = f"{gps_info_dict[16]}°"
                except Exception as e:
                    metadata['⚠️ Warnings'].append(f"GPS data processing error: {str(e)}")
            
            metadata['📍 GPS & Location Data'] = gps_info if gps_info else "No GPS data found"

            # 📅 Enhanced Date/Time information
            date_info = {}
            if 'DateTime' in exif_data:
                date_info['Capture Time'] = format_exif_time(exif_data['DateTime'])
            if 'DateTimeOriginal' in exif_data:
                date_info['Original Capture Time'] = format_exif_time(exif_data['DateTimeOriginal'])
            if 'DateTimeDigitized' in exif_data:
                date_info['Digitization Time'] = format_exif_time(exif_data['DateTimeDigitized'])
            if 'SubSecTimeOriginal' in exif_data:
                date_info['Subsecond Time'] = exif_data['SubSecTimeOriginal']
            
            metadata['🕒 Date & Time Information'] = date_info if date_info else "No date/time metadata found"

            # 📷 Enhanced Camera information
            camera_info = {}
            if 'Make' in exif_data:
                camera_info['Manufacturer'] = exif_data['Make']
            if 'Model' in exif_data:
                camera_info['Model'] = exif_data['Model']
                # Check if this might be a phone
                phone_brand, phone_model = extract_phone_info(exif_data['Model'])
                if phone_brand:
                    metadata['📱 Device Information'] = {
                        'Device Type': 'Smartphone',
                        'Brand': phone_brand,
                        'Model': phone_model,
                        'Operating System': 'Unknown'
                    }
                    # Try to detect OS based on brand
                    if phone_brand.lower() in ('iphone', 'ipad'):
                        metadata['📱 Device Information']['Operating System'] = 'iOS'
                    elif phone_brand.lower() in ('samsung', 'huawei', 'xiaomi', 'google', 'oneplus', 'sony', 'lg', 'motorola'):
                        metadata['📱 Device Information']['Operating System'] = 'Android'
            if 'Software' in exif_data:
                camera_info['Software'] = exif_data['Software']
            if 'ExifVersion' in exif_data:
                camera_info['EXIF Version'] = exif_data['ExifVersion'].decode('ascii') if isinstance(exif_data['ExifVersion'], bytes) else exif_data['ExifVersion']
            if 'BodySerialNumber' in exif_data:
                camera_info['Camera Serial Number'] = exif_data['BodySerialNumber']
            
            # 🎚️ Enhanced Camera settings
            camera_settings = {}
            if 'ExposureTime' in exif_data:
                try:
                    if isinstance(exif_data['ExposureTime'], tuple):
                        camera_settings['Exposure Time'] = f"{exif_data['ExposureTime'][0]}/{exif_data['ExposureTime'][1]} sec"
                    else:
                        camera_settings['Exposure Time'] = f"{exif_data['ExposureTime']} sec"
                except:
                    camera_settings['Exposure Time'] = str(exif_data['ExposureTime'])
            if 'FNumber' in exif_data:
                try:
                    if isinstance(exif_data['FNumber'], tuple):
                        camera_settings['Aperture'] = f"f/{exif_data['FNumber'][0]/exif_data['FNumber'][1]:.1f}"
                    else:
                        camera_settings['Aperture'] = f"f/{float(exif_data['FNumber']):.1f}"
                except:
                    camera_settings['Aperture'] = str(exif_data['FNumber'])
            if 'ISOSpeedRatings' in exif_data:
                camera_settings['ISO Speed'] = exif_data['ISOSpeedRatings']
            if 'FocalLength' in exif_data:
                try:
                    if isinstance(exif_data['FocalLength'], tuple):
                        camera_settings['Focal Length'] = f"{exif_data['FocalLength'][0]/exif_data['FocalLength'][1]:.1f} mm"
                    else:
                        camera_settings['Focal Length'] = f"{float(exif_data['FocalLength']):.1f} mm"
                except:
                    camera_settings['Focal Length'] = str(exif_data['FocalLength'])
            if 'Flash' in exif_data:
                flash_info = {
                    0x0: "No Flash",
                    0x1: "Fired",
                    0x5: "Fired, Return not detected",
                    0x7: "Fired, Return detected",
                    0x8: "On, Did not fire",
                    0x9: "On, Fired",
                    0xD: "On, Return not detected",
                    0xF: "On, Return detected",
                    0x10: "Off, Did not fire",
                    0x14: "Off, Did not fire, Return not detected",
                    0x18: "Auto, Did not fire",
                    0x19: "Auto, Fired",
                    0x1D: "Auto, Fired, Return not detected",
                    0x1F: "Auto, Fired, Return detected",
                    0x20: "No flash function",
                    0x30: "Off, No flash function",
                    0x41: "Fired, Red-eye reduction",
                    0x45: "Fired, Red-eye reduction, Return not detected",
                    0x47: "Fired, Red-eye reduction, Return detected",
                    0x49: "On, Red-eye reduction",
                    0x4D: "On, Red-eye reduction, Return not detected",
                    0x4F: "On, Red-eye reduction, Return detected",
                    0x50: "Off, Red-eye reduction",
                    0x58: "Auto, Did not fire, Red-eye reduction",
                    0x59: "Auto, Fired, Red-eye reduction",
                    0x5D: "Auto, Fired, Red-eye reduction, Return not detected",
                    0x5F: "Auto, Fired, Red-eye reduction, Return detected"
                }
                camera_settings['Flash'] = flash_info.get(exif_data['Flash'], f"Unknown (Value: {exif_data['Flash']})")
            
            metadata['📷 Camera Information'] = {**camera_info, **camera_settings} if camera_info or camera_settings else "No camera metadata found"

        # 🔍 Enhanced EXIF extraction with exifread
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            
            # ✨ Additional interesting metadata
            interesting_tags = {
                'Image Orientation': 'Orientation',
                'EXIF LightSource': 'Light Source',
                'EXIF ExposureProgram': 'Exposure Program',
                'EXIF MeteringMode': 'Metering Mode',
                'EXIF WhiteBalance': 'White Balance',
                'EXIF SceneCaptureType': 'Scene Type',
                'EXIF LensModel': 'Lens Model',
                'EXIF LensSerialNumber': 'Lens Serial',
                'EXIF BodySerialNumber': 'Camera Serial',
                'EXIF Contrast': 'Contrast',
                'EXIF Saturation': 'Saturation',
                'EXIF Sharpness': 'Sharpness',
                'EXIF DigitalZoomRatio': 'Digital Zoom',
                'EXIF ExposureBiasValue': 'Exposure Bias',
                'EXIF MaxApertureValue': 'Max Aperture',
                'EXIF SubjectDistance': 'Subject Distance',
                'EXIF FocalLengthIn35mmFilm': '35mm Equivalent Focal Length',
            }
            
            additional_data = {}
            for exif_key, display_name in interesting_tags.items():
                if exif_key in tags:
                    additional_data[display_name] = str(tags[exif_key])
            
            if additional_data:
                metadata['⚙️ Additional EXIF Data'] = additional_data

        # 🕵️‍♂️ Add system information
        metadata['💻 Tool Information'] = {
            'Tool Name': 'AIM Forensic Extractor',
            'Tool Version': 'v1.0',
            'Tool Owner': 'Sabir Khan',
            'Python Version': platform.python_version(),
            'Operating System': platform.system(),
            'OS Version': platform.version(),
            'Processor': platform.processor()
        }

    except Exception as e:
        metadata['❌ Critical Error'] = f"Failed to process image: {str(e)}"
        import traceback
        metadata['❌ Stack Trace'] = traceback.format_exc()
    
    return metadata

# ======================
# 🖥️ GUI APPLICATION
# ======================

class MetadataExtractorApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 AIM(ADVANCED IMAGE METADATA) FORENSIC EXTRACTOR 🕵️")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(QSize(900, 600))
        
        # Set application style with professional dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QGroupBox {
                border: 1px solid #333;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: #e0e0e0;
                font-weight: bold;
                font-size: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #424242;
                color: #757575;
            }
            QTreeWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #333;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: #e0e0e0;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                selection-background-color: #1e88e5;
            }
            QProgressBar {
                border: 1px solid #333;
                border-radius: 3px;
                text-align: center;
                color: white;
                background-color: #1e1e1e;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                width: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #333;
                background: #1e1e1e;
            }
            QTabBar::tab {
                background: #1e1e1e;
                color: #e0e0e0;
                padding: 8px 12px;
                border: 1px solid #333;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #1e88e5;
                color: white;
            }
            QTabBar::tab:hover {
                background: #333;
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #1e1e1e;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)
        
        # Header section
        self.create_header_section()
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #333;")
        self.main_layout.addWidget(separator)
        
        # Image preview and metadata section
        self.create_metadata_section()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("color: #9e9e9e; background-color: #121212;")
        self.status_bar.showMessage("Ready to analyze images")
        
        # Initialize variables
        self.current_file = None
        self.metadata = None
        
        # Start animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(50)
        
        # Animation variables
        self.animation_phase = 0
        self.animation_colors = [
            QColor(30, 136, 229),  # Blue
            QColor(76, 175, 80),    # Green
            QColor(156, 39, 176),   # Purple
            QColor(255, 193, 7),    # Yellow
            QColor(255, 87, 34)     # Orange
        ]
    
    def create_header_section(self):
        """Create the header section with logo, title, and buttons"""
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #1e1e1e; border-radius: 5px;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        # Logo and title
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        self.title_label = QLabel("🔍 AIM(ADVANCED IMAGE METADATA) FORENSIC EXTRACTOR 🕵️")
        self.title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #ffffff;
        """)
        
        self.subtitle_label = QLabel("Professional digital forensics tool for image analysis")
        self.subtitle_label.setStyleSheet("""
            font-size: 12px; 
            color: #9e9e9e;
        """)
        
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)
        title_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.open_button = QPushButton("📂 Open Image")
        self.open_button.setToolTip("Open an image file for analysis")
        self.open_button.clicked.connect(self.open_image)
        self.open_button.setCursor(Qt.PointingHandCursor)
        
        self.save_button = QPushButton("💾 Save Report")
        self.save_button.setToolTip("Save the metadata report to a JSON file")
        self.save_button.clicked.connect(self.save_report)
        self.save_button.setEnabled(False)
        self.save_button.setCursor(Qt.PointingHandCursor)
        
        self.export_button = QPushButton("📄 Export to TXT")
        self.export_button.setToolTip("Export the metadata report to a text file")
        self.export_button.clicked.connect(self.export_to_txt)
        self.export_button.setEnabled(False)
        self.export_button.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.export_button)
        
        header_layout.addLayout(title_layout, stretch=4)
        header_layout.addLayout(button_layout, stretch=1)
        
        self.main_layout.addWidget(header_widget)
    
    def create_metadata_section(self):
        """Create the metadata display section with tabs"""
        # Main container
        metadata_container = QHBoxLayout()
        metadata_container.setSpacing(15)
        
        # Left side - image preview
        self.image_preview_group = QGroupBox("Image Preview")
        self.image_preview_group.setMinimumWidth(300)
        image_preview_layout = QVBoxLayout()
        image_preview_layout.setContentsMargins(10, 15, 10, 10)
        
        # Image preview with frame
        self.image_frame = QFrame()
        self.image_frame.setFrameShape(QFrame.Box)
        self.image_frame.setLineWidth(1)
        self.image_frame.setStyleSheet("background-color: #1e1e1e; border-color: #333;")
        frame_layout = QVBoxLayout(self.image_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #121212;")
        self.image_label.setText("No image loaded")
        
        frame_layout.addWidget(self.image_label)
        
        # Image info
        self.image_info_label = QLabel()
        self.image_info_label.setAlignment(Qt.AlignCenter)
        self.image_info_label.setStyleSheet("font-size: 11px; color: #9e9e9e;")
        self.image_info_label.setText("Select an image to begin analysis")
        
        image_preview_layout.addWidget(self.image_frame)
        image_preview_layout.addWidget(self.image_info_label)
        self.image_preview_group.setLayout(image_preview_layout)
        
        # Right side - metadata tabs
        self.metadata_tabs = QTabWidget()
        self.metadata_tabs.setDocumentMode(True)
        
        # Create tabs
        self.tree_tab = QWidget()
        self.json_tab = QWidget()
        self.forensic_tab = QWidget()
        
        self.tree_tab_layout = QVBoxLayout(self.tree_tab)
        self.json_tab_layout = QVBoxLayout(self.json_tab)
        self.forensic_tab_layout = QVBoxLayout(self.forensic_tab)
        
        # Tree view tab
        self.metadata_tree = QTreeWidget()
        self.metadata_tree.setHeaderLabels(["Property", "Value"])
        self.metadata_tree.setColumnWidth(0, 300)
        self.metadata_tree.setAlternatingRowColors(True)
        self.metadata_tree.setIndentation(15)
        self.tree_tab_layout.addWidget(self.metadata_tree)
        
        # JSON view tab
        self.json_view = QTextEdit()
        self.json_view.setReadOnly(True)
        self.json_tab_layout.addWidget(self.json_view)
        
        # Forensic tab
        self.forensic_view = QTextEdit()
        self.forensic_view.setReadOnly(True)
        self.forensic_tab_layout.addWidget(self.forensic_view)
        
        # Add tabs
        self.metadata_tabs.addTab(self.tree_tab, "📊 Structured View")
        self.metadata_tabs.addTab(self.json_tab, "📝 JSON View")
        self.metadata_tabs.addTab(self.forensic_tab, "🕵️‍♂️ Forensic Analysis")
        
        # Add widgets to container
        metadata_container.addWidget(self.image_preview_group)
        metadata_container.addWidget(self.metadata_tabs, stretch=1)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        
        self.main_layout.addLayout(metadata_container)
        self.main_layout.addWidget(self.progress_bar)
    
    def update_animations(self):
        """Update UI animations"""
        self.animation_phase = (self.animation_phase + 1) % 360
        color_index = int((self.animation_phase / 360) * len(self.animation_colors))
        next_color_index = (color_index + 1) % len(self.animation_colors)
        
        # Calculate intermediate color
        progress = ((self.animation_phase / 360) * len(self.animation_colors)) % 1
        current_color = self.animation_colors[color_index]
        next_color = self.animation_colors[next_color_index]
        
        r = int(current_color.red() + (next_color.red() - current_color.red()) * progress)
        g = int(current_color.green() + (next_color.green() - current_color.green()) * progress)
        b = int(current_color.blue() + (next_color.blue() - current_color.blue()) * progress)
        
        # Apply gradient to title
        gradient = QLinearGradient(0, 0, self.title_label.width(), 0)
        gradient.setColorAt(0, QColor(r, g, b))
        gradient.setColorAt(1, QColor(
            (r + self.animation_colors[next_color_index].red()) // 2,
            (g + self.animation_colors[next_color_index].green()) // 2,
            (b + self.animation_colors[next_color_index].blue()) // 2
        ))
        
        palette = self.title_label.palette()
        palette.setColor(QPalette.WindowText, QColor(r, g, b))
        self.title_label.setPalette(palette)
    
    def open_image(self):
        """Open an image file and extract metadata"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif *.heic *.webp)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setStyleSheet("""
            QFileDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
            }
            QTreeView, QListView {
                background-color: #1e1e1e;
                color: #e0e0e0;
                alternate-background-color: #121212;
            }
            QTreeView::item:hover, QListView::item:hover {
                background-color: #333;
            }
        """)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.current_file = selected_files[0]
                self.analyze_image()
    
    def analyze_image(self):
        """Analyze the selected image and display metadata"""
        if not self.current_file:
            return
        
        # Show progress bar
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        QApplication.processEvents()
        
        try:
            # Load image preview
            pixmap = QPixmap(self.current_file)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")
            else:
                self.image_label.setText("Preview not available")
                self.image_label.setPixmap(QPixmap())
            
            # Update file info
            file_size = os.path.getsize(self.current_file)
            self.image_info_label.setText(
                f"{os.path.basename(self.current_file)}\n"
                f"{get_human_readable_size(file_size)}"
            )
            
            # Extract metadata with progress updates
            self.progress_bar.setValue(20)
            QApplication.processEvents()
            
            self.metadata = extract_all_metadata(self.current_file)
            
            self.progress_bar.setValue(80)
            QApplication.processEvents()
            
            # Display metadata
            self.display_metadata()
            
            self.progress_bar.setValue(100)
            QApplication.processEvents()
            
            # Enable save and export buttons
            self.save_button.setEnabled(True)
            self.export_button.setEnabled(True)
            
            self.status_bar.showMessage(f"Analysis complete: {os.path.basename(self.current_file)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to analyze image: {str(e)}")
            self.status_bar.showMessage(f"Error analyzing image: {str(e)}")
        finally:
            # Hide progress bar after a short delay
            QTimer.singleShot(1000, self.progress_bar.hide)
    
    def display_metadata(self):
        """Display extracted metadata in the UI"""
        if not self.metadata:
            return
        
        # Clear previous data
        self.metadata_tree.clear()
        self.json_view.clear()
        self.forensic_view.clear()
        
        # Display in tree view
        self.populate_tree_view()
        
        # Display raw JSON
        self.json_view.setPlainText(json.dumps(self.metadata, indent=4))
        
        # Display forensic analysis
        self.display_forensic_analysis()
    
    def populate_tree_view(self):
        """Populate the tree widget with metadata"""
        for category, data in self.metadata.items():
            if category.startswith('⚠️') or category.startswith('❌'):
                continue
                
            category_item = QTreeWidgetItem([category])
            self.metadata_tree.addTopLevelItem(category_item)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        sub_item = QTreeWidgetItem([key])
                        category_item.addChild(sub_item)
                        for sub_key, sub_value in value.items():
                            sub_sub_item = QTreeWidgetItem([sub_key, str(sub_value)])
                            sub_item.addChild(sub_sub_item)
                    else:
                        item = QTreeWidgetItem([key, str(value)])
                        category_item.addChild(item)
            else:
                item = QTreeWidgetItem([str(data)])
                category_item.addChild(item)
        
        self.metadata_tree.expandAll()
    
    def display_forensic_analysis(self):
        """Display forensic analysis information"""
        if not self.metadata:
            return
        
        analysis_text = "=== FORENSIC ANALYSIS REPORT ===\n\n"
        
        # File integrity
        if '🔒 File Integrity' in self.metadata:
            analysis_text += "=== FILE INTEGRITY ===\n"
            for hash_name, hash_value in self.metadata['🔒 File Integrity'].items():
                analysis_text += f"{hash_name}: {hash_value}\n"
            analysis_text += "\n"
        
        # Forensic indicators
        if '🕵️ Forensic Analysis' in self.metadata:
            analysis_text += "=== FORENSIC INDICATORS ===\n"
            for indicator, value in self.metadata['🕵️ Forensic Analysis'].items():
                analysis_text += f"{indicator}: {value}\n"
            analysis_text += "\n"
        
        # Warnings
        if '⚠️ Warnings' in self.metadata and self.metadata['⚠️ Warnings']:
            analysis_text += "=== WARNINGS ===\n"
            for warning in self.metadata['⚠️ Warnings']:
                analysis_text += f"• {warning}\n"
            analysis_text += "\n"
        
        # Critical errors
        if '❌ Critical Error' in self.metadata:
            analysis_text += "=== CRITICAL ERROR ===\n"
            analysis_text += self.metadata['❌ Critical Error'] + "\n"
            if '❌ Stack Trace' in self.metadata:
                analysis_text += "\nStack Trace:\n" + self.metadata['❌ Stack Trace']
            analysis_text += "\n"
        
        self.forensic_view.setPlainText(analysis_text)
    
    def save_report(self):
        """Save metadata report to JSON file"""
        if not self.metadata:
            return
        
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.setDefaultSuffix("json")
        
        # Suggest a filename based on the image
        if self.current_file:
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            file_dialog.selectFile(f"{base_name}_metadata.json")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                output_path = selected_files[0]
                try:
                    with open(output_path, 'w') as f:
                        json.dump(self.metadata, f, indent=4)
                    QMessageBox.information(self, "Success", f"Report saved successfully to:\n{output_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save report:\n{str(e)}")
    
    def export_to_txt(self):
        """Export metadata report to text file"""
        if not self.metadata:
            return
        
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setDefaultSuffix("txt")
        
        # Suggest a filename based on the image
        if self.current_file:
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            file_dialog.selectFile(f"{base_name}_metadata_report.txt")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                output_path = selected_files[0]
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        # Write header
                        f.write("="*60 + "\n")
                        f.write("IMAGE METADATA FORENSIC REPORT\n")
                        f.write("="*60 + "\n\n")
                        
                        # Write basic info
                        if '📁 File Information' in self.metadata:
                            f.write("=== FILE INFORMATION ===\n")
                            for key, value in self.metadata['📁 File Information'].items():
                                f.write(f"{key}: {value}\n")
                            f.write("\n")
                        
                        # Write forensic info
                        f.write(self.forensic_view.toPlainText())
                        
                        # Write all metadata
                        f.write("\n=== COMPLETE METADATA ===\n")
                        f.write(json.dumps(self.metadata, indent=4))
                    
                    QMessageBox.information(self, "Success", f"Report exported successfully to:\n{output_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to export report:\n{str(e)}")
    
    def resizeEvent(self, event):
        """Handle window resize events to update image preview"""
        super().resizeEvent(event)
        if self.current_file and not self.image_label.pixmap().isNull():
            pixmap = QPixmap(self.current_file)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

# ======================
# 🚀 APPLICATION START
# ======================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style and font
    app.setStyle('Fusion')
    font = QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    # Create and show main window
    window = MetadataExtractorApp()
    window.show()
    
    # Check for command line argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            window.current_file = image_path
            QTimer.singleShot(100, window.analyze_image)
    
    sys.exit(app.exec_())
