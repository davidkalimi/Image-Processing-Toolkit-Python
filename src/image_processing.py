import matplotlib.pyplot as plt
from typing import TypeVar
import numpy as np
import matplotlib.image as mpimg
import imageio as im
import os

chooseReturn = TypeVar('T')


class MyImage(object):
    """
    Base class for image processing operations.
    Handles loading, saving, and basic image operations.
    """

    def __init__(self, image_name: str):
        """
        Initialize the image processor.

        Args:
            image_name: Name of the image file (e.g., 'photo.png')
        """
        self.image_path = self._get_assets_path(image_name)
        self.img_array = im.v2.imread(self.image_path)
        self.original_name = image_name

    def _get_assets_path(self, filename: str) -> str:
        """
        Get the full path to a file in the assets folder.

        Args:
            filename: Name of the file

        Returns:
            Full path to the file in assets folder
        """
        # Get current directory and go up to find assets folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

        # Create assets directory if it doesn't exist
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        return os.path.join(assets_dir, filename)

    def set_image(self, image_name: str) -> None:
        """
        Load a new image for processing.

        Args:
            image_name: Name of the new image file
        """
        self.image_path = self._get_assets_path(image_name)
        self.img_array = im.v2.imread(self.image_path)
        self.original_name = image_name

    def display_image(self) -> None:
        """Display the current image using matplotlib."""
        plt.figure(figsize=(8, 6))
        plt.imshow(self.img_array)
        plt.title(f'Image: {self.original_name}')
        plt.axis('off')
        plt.show()

    def get_image_array(self) -> np.ndarray:
        """
        Get the image as a numpy array.

        Returns:
            Numpy array representation of the image
        """
        return self.img_array

    def save_processed_image(self, suffix: str) -> str:
        """
        Save the processed image with a suffix.

        Args:
            suffix: Suffix to add to filename (e.g., '_processed')

        Returns:
            Path where the image was saved
        """
        name, ext = os.path.splitext(self.original_name)
        new_filename = f"{name}{suffix}{ext}"
        new_path = self._get_assets_path(new_filename)

        im.imwrite(new_path, self.img_array)
        print(f"Image saved: {new_path}")
        return new_path


class ThresholdByNumber(MyImage):
    """
    Apply threshold based on absolute pixel values.
    Pixels below threshold become black, above become white.
    """

    def apply_threshold(self, threshold_value: int) -> None:
        """
        Apply threshold filtering to the image.

        Args:
            threshold_value: Pixel values below this become 0, above become 255
        """
        # Create new array with same shape
        new_array = np.zeros(self.img_array.shape, dtype=int)

        # Apply threshold
        new_array[self.img_array < threshold_value] = 0
        new_array[self.img_array >= threshold_value] = 255

        # Update image array
        self.img_array = new_array.astype(np.uint8)

        # Save the result
        self.save_processed_image(f'_threshold_{threshold_value}')


class ThresholdByPercentage(MyImage):
    """
    Apply threshold based on percentage of maximum pixel value.
    Good for images with different brightness levels.
    """

    def apply_threshold(self, percentage: int) -> None:
        """
        Apply percentage-based threshold filtering.

        Args:
            percentage: Percentage value (0-100) for threshold
        """
        # Create new array with same shape
        new_array = np.zeros(self.img_array.shape, dtype=int)

        # Calculate threshold based on percentage
        threshold_value = (percentage / 100) * 255

        # Apply threshold
        new_array[self.img_array < threshold_value] = 0
        new_array[self.img_array >= threshold_value] = 255

        # Update image array
        self.img_array = new_array.astype(np.uint8)

        # Save the result
        self.save_processed_image(f'_threshold_{percentage}percent')


class RednessDetector(MyImage):
    """
    Auto Redness Detector - Identifies red areas in images.

    This class detects pixels that have significantly more red color
    than green or blue, which is useful for finding red objects,
    inflammation in medical images, or other red-dominant areas.
    """

    def detect_red_areas(self, sensitivity: float = 1.2) -> None:
        """
        Detect and highlight red areas in the image.

        The algorithm compares the red channel value to green and blue channels.
        Areas where red is significantly higher are marked as white,
        everything else becomes black.

        Args:
            sensitivity: How sensitive the detection is (higher = less sensitive)
                        1.0 = red must be equal to green/blue
                        1.5 = red must be 50% higher than green/blue
                        2.0 = red must be twice as high as green/blue
        """
        # Check if image is RGB
        if len(self.img_array.shape) != 3 or self.img_array.shape[2] != 3:
            print("Error: Image must be RGB (3 channels)")
            return

        # Separate RGB channels
        red_channel = self.img_array[:, :, 0].astype(float)
        green_channel = self.img_array[:, :, 1].astype(float)
        blue_channel = self.img_array[:, :, 2].astype(float)

        # Create mask for red areas
        # A pixel is considered "red" if red value is higher than green AND blue
        # multiplied by sensitivity factor
        red_mask = (red_channel > green_channel * sensitivity) & \
                   (red_channel > blue_channel * sensitivity)

        # Create new image: white for red areas, black for everything else
        new_image = np.zeros_like(self.img_array)
        new_image[red_mask] = [255, 255, 255]  # White for red areas
        new_image[~red_mask] = [0, 0, 0]  # Black for non-red areas

        # Update image array
        self.img_array = new_image.astype(np.uint8)

        # Save the result
        self.save_processed_image(f'_red_detection_sens_{sensitivity}')

        # Print statistics
        red_pixel_count = np.sum(red_mask)
        total_pixels = red_mask.size
        red_percentage = (red_pixel_count / total_pixels) * 100
        print(f"Red pixels detected: {red_pixel_count} ({red_percentage:.1f}%)")

    def show_before_after(self) -> None:
        """
        Display original image alongside the processed result.
        Useful for comparing the detection results.
        """
        # Load original image
        original = im.v2.imread(self.image_path)

        # Create side-by-side comparison
        plt.figure(figsize=(15, 6))

        # Original image
        plt.subplot(1, 2, 1)
        plt.imshow(original)
        plt.title('Original Image')
        plt.axis('off')

        # Processed image
        plt.subplot(1, 2, 2)
        plt.imshow(self.img_array)
        plt.title('Red Areas Detection')
        plt.axis('off')

        plt.tight_layout()
        plt.show()


def create_test_image_with_red_dots():
    """
    Create a test image with red dots for testing the redness detector.
    This function generates a sample image that you can use to test
    the detection algorithm.
    """
    import random

    # Create 400x400 image with light gray background
    height, width = 400, 400
    image = np.ones((height, width, 3), dtype=np.uint8) * 200

    # Add random red dots
    num_red_dots = 25

    for _ in range(num_red_dots):
        # Random position
        x = random.randint(15, width - 15)
        y = random.randint(15, height - 15)

        # Random size
        size = random.randint(5, 20)

        # Create circular red dot
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                if i * i + j * j <= size * size:  # Circle equation
                    if 0 <= y + i < height and 0 <= x + j < width:
                        image[y + i, x + j] = [255, 0, 0]  # Pure red

    # Save test image to assets folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(os.path.dirname(current_dir), 'assets')

    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    test_image_path = os.path.join(assets_dir, 'test_red_dots.png')
    im.imwrite(test_image_path, image)
    print(f"Test image created: {test_image_path}")

    return 'test_red_dots.png'


# Example usage for beginners
if __name__ == "__main__":
    print("=== Image Processing Demo ===")

    # Step 1: Create a test image (optional)
    print("\n1. Creating test image with red dots...")
    test_image = create_test_image_with_red_dots()

    # Step 2: Initialize the redness detector
    print("\n2. Loading image for redness detection...")
    detector = RednessDetector(test_image)

    # Step 3: Display original image
    print("\n3. Displaying original image...")
    detector.display_image()

    # Step 4: Detect red areas
    print("\n4. Detecting red areas...")
    detector.detect_red_areas(sensitivity=1.2)

    # Step 5: Show comparison
    print("\n5. Showing before/after comparison...")
    detector.show_before_after()

    print("\n=== Demo Complete ===")
    print("Check the 'assets' folder for saved images!")