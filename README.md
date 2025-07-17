# Image Processing with Redness Detection

A comprehensive Python library for image processing with specialized focus on detecting red areas in images. This project demonstrates object-oriented programming principles and computer vision techniques in an educational, beginner-friendly format.

## 🎯 Project Overview

This library provides tools for:
- **Basic image processing** operations (loading, displaying, saving)
- **Threshold filtering** by absolute values or percentages
- **Advanced red area detection** using color channel analysis
- **Automated file management** through organized asset directories

## 📁 Project Structure

```
project/
├── src/
│   └── image_processing.py     # Main library code
├── assets/                     # Image storage directory
│   ├── input_images/          # Original images
│   ├── processed_images/      # Processed results
│   └── test_images/           # Generated test images
└── README.md                  # This file
```

## 🚀 Quick Start

### Installation Requirements

```bash
pip install matplotlib numpy imageio
```

### Basic Usage

```python
from src.image_processing import RednessDetector

# Create detector instance
detector = RednessDetector('your_image.png')

# Display original image
detector.display_image()

# Detect red areas
detector.detect_red_areas(sensitivity=1.2)

# Show before/after comparison
detector.show_before_after()
```

## 📚 Core Classes and Methods

### 1. `MyImage` (Base Class)

The foundation class handling basic image operations.

```python
class MyImage:
    def __init__(self, image_name: str)
    def set_image(self, image_name: str) -> None
    def display_image() -> None
    def get_image_array() -> np.ndarray
    def save_processed_image(suffix: str) -> str
```

**Key Features:**
- Automatic asset directory management
- Cross-platform path handling
- Consistent image loading/saving interface

### 2. `ThresholdByNumber` (Absolute Threshold)

Applies binary threshold based on absolute pixel values.

```python
threshold_processor = ThresholdByNumber('image.png')
threshold_processor.apply_threshold(128)  # Values below 128 → black, above → white
```

**Algorithm Logic:**
```python
new_array[pixels < threshold_value] = 0      # Black
new_array[pixels >= threshold_value] = 255   # White
```

### 3. `ThresholdByPercentage` (Relative Threshold)

Applies threshold based on percentage of maximum brightness.

```python
percentage_processor = ThresholdByPercentage('image.png')
percentage_processor.apply_threshold(75)  # 75% of max brightness as threshold
```

**Algorithm Logic:**
```python
threshold_value = (percentage / 100) * 255
```

### 4. `RednessDetector` (Advanced Red Detection)

The main feature: sophisticated red area detection using color channel analysis.

```python
detector = RednessDetector('image.png')
detector.detect_red_areas(sensitivity=1.5)
detector.show_before_after()
```

## 🔬 Red Detection Algorithm Deep Dive

### Core Principle

The algorithm identifies pixels where the red channel value significantly exceeds green and blue channels:

```python
red_mask = (red_channel > green_channel * sensitivity) & \
           (red_channel > blue_channel * sensitivity)
```

### Sensitivity Parameter

- **`sensitivity = 1.0`**: Red must equal green/blue (very sensitive)
- **`sensitivity = 1.5`**: Red must be 50% higher than green/blue (balanced)
- **`sensitivity = 2.0`**: Red must be twice as high as green/blue (less sensitive)

### Visual Example

```
Original Pixel: [200, 100, 80] (RGB)
Sensitivity: 1.2

Check: 200 > 100 * 1.2 = 120 ✓
Check: 200 > 80 * 1.2 = 96 ✓
Result: RED DETECTED → [255, 255, 255] (white)
```

### Output Format

- **White pixels** (255, 255, 255): Red areas detected
- **Black pixels** (0, 0, 0): Non-red areas
- **Statistics**: Percentage of red pixels found

## 🎨 Creating Test Images

The library includes a test image generator:

```python
from src.image_processing import create_test_image_with_red_dots

# Generate test image with random red dots
test_image_name = create_test_image_with_red_dots()
print(f"Test image created: {test_image_name}")
```

**Generated Image Features:**
- 400x400 pixel dimensions
- Light gray background (RGB: 200, 200, 200)
- 25 random red dots (RGB: 255, 0, 0)
- Circular dots with random sizes (5-20 pixel radius)

## 📊 Practical Applications

### Medical Imaging
```python
# Detect inflammation or redness in medical photos
medical_detector = RednessDetector('skin_condition.jpg')
medical_detector.detect_red_areas(sensitivity=1.1)  # High sensitivity for medical use
```

### Quality Control
```python
# Detect red defects in manufacturing
quality_detector = RednessDetector('product_image.jpg')
quality_detector.detect_red_areas(sensitivity=1.8)  # Lower sensitivity for robust detection
```

### Scientific Research
```python
# Analyze red markers in biological samples
research_detector = RednessDetector('microscope_image.tif')
research_detector.detect_red_areas(sensitivity=1.3)
```

## 🔧 File Management System

### Automatic Directory Creation

The system automatically creates and manages the `assets` folder:

```python
def _get_assets_path(self, filename: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')
    
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    return os.path.join(assets_dir, filename)
```

### Intelligent File Naming

Processed images are saved with descriptive suffixes:

```python
# Examples of generated filenames:
# photo.png → photo_red_detection_sens_1.2.png
# image.jpg → image_threshold_128.jpg
# test.png → test_threshold_75percent.png
```

## 📈 Performance Considerations

### Memory Efficiency
- Uses NumPy arrays for fast pixel manipulation
- Processes images in-place when possible
- Automatic dtype optimization (uint8 for final images)

### Algorithm Complexity
- **Time Complexity**: O(n) where n = number of pixels
- **Space Complexity**: O(n) for temporary arrays
- **Recommended Max Image Size**: 2000x2000 pixels

## 🛠️ Advanced Usage Examples

### Batch Processing
```python
import os
from src.image_processing import RednessDetector

def batch_process_images(image_list, sensitivity=1.2):
    results = []
    for image_name in image_list:
        detector = RednessDetector(image_name)
        detector.detect_red_areas(sensitivity)
        results.append(f"Processed: {image_name}")
    return results

# Process multiple images
images = ['photo1.jpg', 'photo2.png', 'photo3.tif']
results = batch_process_images(images, sensitivity=1.5)
```

### Custom Sensitivity Testing
```python
def test_multiple_sensitivities(image_name):
    sensitivities = [1.0, 1.2, 1.5, 2.0]
    
    for sens in sensitivities:
        detector = RednessDetector(image_name)
        detector.detect_red_areas(sensitivity=sens)
        print(f"Sensitivity {sens}: Processing complete")

test_multiple_sensitivities('test_image.png')
```

### Statistical Analysis
```python
def analyze_red_distribution(image_name):
    detector = RednessDetector(image_name)
    original_array = detector.get_image_array().copy()
    
    # Get red channel statistics
    red_channel = original_array[:, :, 0]
    red_mean = np.mean(red_channel)
    red_std = np.std(red_channel)
    
    print(f"Red channel statistics:")
    print(f"Mean: {red_mean:.2f}")
    print(f"Standard deviation: {red_std:.2f}")
    
    # Perform detection
    detector.detect_red_areas(sensitivity=1.2)
    
    return red_mean, red_std
```

## 🐛 Troubleshooting

### Common Issues

1. **"Error: Image must be RGB (3 channels)"**
   - Solution: Ensure image is in RGB format, not grayscale
   - Convert: `image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)`

2. **"No module named 'imageio'"**
   - Solution: Install required packages
   - Command: `pip install imageio matplotlib numpy`

3. **"Image file not found"**
   - Solution: Check that image exists in assets folder
   - Verify path: `os.path.exists('assets/your_image.png')`

4. **Memory issues with large images**
   - Solution: Resize image before processing
   - Example: `image = cv2.resize(image, (800, 600))`

## 📋 API Reference

### Method Parameters

| Method | Parameter | Type | Default | Description |
|--------|-----------|------|---------|-------------|
| `detect_red_areas()` | `sensitivity` | `float` | `1.2` | Detection sensitivity factor |
| `apply_threshold()` | `threshold_value` | `int` | Required | Absolute threshold value (0-255) |
| `apply_threshold()` | `percentage` | `int` | Required | Percentage threshold (0-100) |

### Return Values

| Method | Returns | Description |
|--------|---------|-------------|
| `get_image_array()` | `np.ndarray` | Raw image data as numpy array |
| `save_processed_image()` | `str` | Path where processed image was saved |
| `create_test_image_with_red_dots()` | `str` | Filename of generated test image |

## 🤝 Contributing

This project is educational and welcomes contributions:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-filter`
3. **Commit changes**: `git commit -m "Add new filter"`
4. **Push to branch**: `git push origin feature/new-filter`
5. **Submit pull request**

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎓 Educational Goals

This codebase demonstrates:
- **Object-Oriented Programming** principles
- **Computer Vision** fundamentals
- **File I/O** management
- **NumPy** array operations
- **Matplotlib** visualization
- **Clean code** practices
- **Documentation** standards

Perfect for students learning Python, computer vision, or image processing concepts!

---

*Created with ❤️ for educational purposes*
