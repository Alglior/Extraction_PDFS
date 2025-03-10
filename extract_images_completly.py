import cv2
import numpy as np
import os
from pathlib import Path
import logging

class ImageContentExtractor:
    def __init__(self, base_output_dir: str = "output_images"):
        self.base_output_dir = base_output_dir
        self.min_area = 5000  # Minimum area for image content
        self.subfolder_name = "image_sans_texte"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('image_extraction.log', encoding='utf-8'), 
                     logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)

    def find_image_folders(self):
        """Find all 'split_images' and 'une_image_page' folders recursively"""
        target_folders = []
        for root, dirs, _ in os.walk(str(Path(self.base_output_dir))):
            if 'split_images' in dirs:
                target_folders.append(str(Path(root) / 'split_images'))
            if 'une_image_page' in dirs:
                target_folders.append(str(Path(root) / 'une_image_page'))
        return target_folders

    def find_jpg_files(self, folder_path):
        """Find all jpg files containing 'page' in the filename"""
        folder_path = Path(folder_path)
        return [f.name for f in folder_path.glob('*.jpg') 
                if 'page' in f.name.lower()]

    def create_extraction_subfolder(self, source_folder: str) -> str:
        """Create image_sans_texte subfolder in the source directory"""
        subfolder_path = Path(source_folder) / self.subfolder_name
        subfolder_path.mkdir(exist_ok=True)
        return str(subfolder_path)

    def extract_image_content(self, image_path: str, output_folder: str):
        try:
            # Convert paths to Path objects
            image_path = Path(image_path)
            output_folder = Path(output_folder)
            
            # Read the image using cv2.imdecode for Unicode support
            img_array = np.fromfile(str(image_path), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError(f"Cannot read image: {image_path}")

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Binary threshold to separate content from background
            _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

            # Find contours in the binary image
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the largest contour (likely the main image content)
            main_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(main_contour)

            # Add a small padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(img.shape[1] - x, w + 2 * padding)
            h = min(img.shape[0] - y, h + 2 * padding)

            # Extract the region
            image_content = img[y:y+h, x:x+w]

            # Save the extracted content with the same filename
            output_path = output_folder / image_path.name
            cv2.imencode('.jpg', image_content)[1].tofile(str(output_path))
            self.logger.info(f"Extracted content saved to: {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Error processing {image_path}: {e}")
            raise

def main():
    try:
        extractor = ImageContentExtractor()
        image_folders = extractor.find_image_folders()
        
        if not image_folders:
            print("No split_images or une_image_page folders found!")
            return
            
        print(f"Found {len(image_folders)} folders to process")
        
        for folder in image_folders:
            print(f"\nProcessing folder: {folder}")
            
            # Find jpg files in the folder
            images = extractor.find_jpg_files(folder)
            
            if not images:
                print(f"No jpg files found in {folder}")
                continue
                
            print(f"Found {len(images)} images to process")
            
            # Create image_sans_texte subfolder
            extraction_folder = extractor.create_extraction_subfolder(folder)
            print(f"Using extraction folder: {extraction_folder}")
            
            for i, image_file in enumerate(images, 1):
                image_path = Path(folder) / image_file
                print(f"Processing {image_file} ({i}/{len(images)})...")
                extractor.extract_image_content(str(image_path), extraction_folder)
                print(f"→ Image content extracted")
        
        print("\nProcessing complete. Check image_extraction.log for details.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()