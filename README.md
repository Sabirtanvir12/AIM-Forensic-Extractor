# 🔍 AIM (Advanced Image Metadata) Forensic Extractor 🕵️‍♂️

![AIM Forensic Extractor Demo](https://i.postimg.cc/vZNGwyHW/Screenshot-2025-05-14-194433.png)


**A professional-grade digital forensics tool for extracting, analyzing, and visualizing image metadata with advanced forensic capabilities**

**Version:** 2.0  
**Developer:** Sabir Khan  
**GitHub:** [https://github.com/Sabirtanvir12](https://github.com/Sabirtanvir12)

---

## 🌟 Key Features

### 🕵️‍♂️ Forensic Investigation
- **Comprehensive Metadata Extraction** (EXIF, IPTC, XMP, GPS, etc.)
- **Tampering Detection** with Error Level Analysis (ELA)
- **Steganography Indicators** detection
- **File Authenticity Verification** with multiple hash algorithms

### 📊 Advanced Analysis
- **Visual Timeline** of image creation/modification
- **Geolocation Mapping** with Google Maps/OpenStreetMap integration
- **Device Fingerprinting** (Camera/Phone identification)
- **Thumbnail Extraction** from embedded previews

### 💻 User Experience
- **Beautiful Dark Theme UI** with professional aesthetics
- **Three View Modes** (Structured, JSON, Forensic)
- **Cross-platform** (Windows, Linux, macOS)
- **One-Click Reports** (JSON/TXT export)

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Qt 5.15+
- Pillow 9.0+
- exifread 3.0+

## Installation ⚙️

### Prerequisites
- Python 3.6+
- Windows:
  - Built-in WiFi tools
- Linux:
  - `aircrack-ng` suite
  - `nmcli` (NetworkManager)

### Installation Steps
```bash
git clone https://github.com/Sabirtanvir12/AIM-Forensic-Extractor.git
cd aim
```

```bash
pip install python3-pyqt5 python3-pil python3-exifread
```
```bash
python3 aim.py
```

---
### 💻 Windows
1. Download the ZIP file from GitHub and extract it.
2. Open the extracted folder.
3. Right-click inside the folder and select **Open in Terminal**.
4. Install dependencies:
   ```powershell
   pip install python3-pyqt5 python3-pil python3-exifread
   ```

5. Run the script using:
   ```powershell
   Duble click then run with ide or python debuger
   ```

---

## 🖱️ Usage Guide

### 🔓 Open an Image
- Click 📂 **Open Image** or simply **drag & drop** any supported image file (`.jpg`, `.png`, `.tiff`, `.webp`, `.heic`, `.dng`, etc.)

### 🧠 Analyze Metadata

- 🔹 **Structured View**:  
  Explore metadata organized in an intuitive category tree (e.g., File Info, Camera Info, GPS, EXIF).

- 🔹 **JSON View**:  
  View the raw extracted metadata in machine-readable JSON format.

- 🔹 **Forensic View**:  
  Detect **tampering indicators**, verify **hash values**, and flag suspicious changes in metadata.

### 💾 Export Results

- Save extracted data in:
  - 📄 **JSON format** for programmatic use
  - 📝 **TXT format** for human-readable reports

### 🌍 Geolocation

- Click on **GPS coordinates** to instantly open the location on your default browser using online maps.(If Available)

---

## 📸 Supported Image Formats

| Format     | Metadata Support | Thumbnail Preview | GPS Data |
|------------|------------------|-------------------|----------|
| **JPEG/JPG** | ✅ Full          | ✅ Yes            | ✅ Yes   |
| **PNG**      | ✅ Full          | ❌ No             | ✅ Yes   |
| **TIFF**     | ✅ Full          | ✅ Yes            | ✅ Yes   |
| **WebP**     | ✅ Full          | ✅ Yes            | ✅ Yes   |
| **HEIC**     | ⚠️ Partial       | ✅ Yes            | ✅ Yes   |
| **RAW (DNG)**| ⚠️ Partial       | ✅ Yes            | ✅ Yes   |

> ℹ️ Some formats (e.g., HEIC, DNG) may show **limited metadata** depending on OS/library support.

---

## 🏆 Professional Use Cases

### 🔎 Digital Forensics
- Extract crucial evidence from **crime scene photos**
- Verify **image authenticity** in legal investigations
- Detect **image tampering** or manipulation using metadata anomalies

### 📰 Journalism
- Validate **source images** used in breaking stories or leaks
- Extract **hidden metadata** to verify image origin or author
- Use **GPS coordinates** to geolocate content from conflict zones

### 📸 Photography
- Review **camera settings** like shutter speed, aperture, ISO
- Track **shooting locations** and time metadata
- Organize and manage **large photo libraries** based on embedded EXIF info

---
### 📊 Sample Report Output(JSON)
- {
-  "📁 File Information": {
-   "File Name": "evidence.jpg",
-    "File Size": "4.2 MB",
-    "Created": "2023-05-15 14:22:10"
-  },
-  "📍 GPS Data": {
-    "Latitude": "40.7128° N",
-    "Longitude": "74.0060° W",
-    "Google Maps": "https://maps.google.com/?q=40.7128,-74.0060"
-  },
-  "🕵️‍♂️ Forensic Analysis": {
-    "SHA256 Hash": "a1b2c3...",
-    "Tampering Indicators": "High ELA variance detected",
-    "Thumbnail Present": true
-  }
- }

---

## 📜 License

🔒 This project is licensed under the **MIT License**. See the `LICENSE` file for more details.  

---
## ❤️ Support

If you like this project, don't forget to **⭐ star the repo**! 😊  

📧 For any queries, reach out via **[sabirtanvir10@gmail.com](mailto:sabirtanvir10@gmail.com)** or open an **issue**.
