import fitz
import os
from pathlib import Path
import logging
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from PIL import Image
import numpy as np

class ImageSplitter:
    def __init__(self, image_path: str, output_dir: str):
        """
        Initialize the splitter with image path and output directory
        """
        self.image_path = image_path
        self.image_name = Path(image_path).stem
        self.output_dir = output_dir
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def detect_split_point(self, image):
        """
        Detect the point where the image should be split by analyzing white space
        or significant changes in pixel values
        """
        # Convert image to grayscale numpy array
        img_array = np.array(image.convert('L'))
        height = img_array.shape[0]
        
        # Look for horizontal line with highest contrast in middle section
        middle_section = img_array[height//3:2*height//3, :]
        row_variances = np.var(middle_section, axis=1)
        split_offset = np.argmin(row_variances) + height//3
        
        return split_offset

    def split_and_save_image(self):
        """
        Split the input image into two separate images and save them
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Open the image
            image = Image.open(self.image_path)
            
            # Get the split point
            split_point = self.detect_split_point(image)
            
            # Split the image
            top_image = image.crop((0, 0, image.width, split_point))
            bottom_image = image.crop((0, split_point, image.width, image.height))
            
            # Save the split images
            top_output_path = os.path.join(self.output_dir, f"{self.image_name}_top.jpg")
            bottom_output_path = os.path.join(self.output_dir, f"{self.image_name}_bottom.jpg")
            
            top_image.save(top_output_path, quality=95)
            bottom_image.save(bottom_output_path, quality=95)
            
            self.logger.info(f"Successfully split {self.image_name} into two images")
            
        except Exception as e:
            self.logger.error(f"Error during image splitting: {e}")
            raise

def find_doubles_images_folders(root_dir: str) -> list:
    """
    Recursively find all folders named 'doubles_images_pages' in the directory tree,
    including those nested within other folders
    """
    doubles_images_folders = []
    target_folder_name = 'doubles_images_pages'
    
    try:
        logging.info(f"Starting search in root directory: {root_dir}")
        for root, dirs, _ in os.walk(root_dir):
            logging.debug(f"Scanning directory: {root}")
            logging.debug(f"Found directories: {dirs}")
            
            # Check each directory in the current level
            for dir_name in dirs:
                if target_folder_name in dir_name.lower():  # Fixed typo and made matching more flexible
                    folder_path = os.path.join(root, dir_name)
                    doubles_images_folders.append(folder_path)
                    logging.info(f"Found matching folder: {folder_path}")
        
        if not doubles_images_folders:
            logging.warning(f"No '{target_folder_name}' folders found in {root_dir}")
        else:
            logging.info(f"Total matching folders found: {len(doubles_images_folders)}")
            
    except Exception as e:
        logging.error(f"Error while searching for folders: {e}")
        raise
    
    return doubles_images_folders

def process_folder(folder_path: str):
    """
    Process all images in a single doubles_images_pages folder
    """
    try:
        # Create output directory next to the input directory
        parent_dir = os.path.dirname(folder_path)
        output_dir = os.path.join(parent_dir, 'split_images')
        
        # Get all image files in the folder
        image_files = [f for f in os.listdir(folder_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print(f"No image files found in {folder_path}")
            return
        
        print(f"Found {len(image_files)} image files to process in {folder_path}")
        
        # Process each image
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            print(f"Processing: {image_file}")
            
            splitter = ImageSplitter(image_path, output_dir)
            splitter.split_and_save_image()
            
        print(f"Completed processing folder: {folder_path}")
        
    except Exception as e:
        print(f"Error processing folder {folder_path}: {e}")

def batch_process_directories(root_dir: str = "."):
    """
    Find and process all doubles_images_pages folders in the directory tree
    """
    try:
        # Find all doubles_images_pages folders
        doubles_images_folders = find_doubles_images_folders(root_dir)
        
        if not doubles_images_folders:
            print("No 'doubles_images_pages' folders found in the directory tree")
            return
        
        print(f"Found {len(doubles_images_folders)} 'doubles_images_pages' folders to process")
        
        # Process each folder
        for folder in doubles_images_folders:
            print(f"\nProcessing folder: {folder}")
            process_folder(folder)
            
        print("\nAll folders processed successfully")
        
    except Exception as e:
        print(f"Error in batch processing: {e}")

if __name__ == "__main__":
    # You can specify a different root directory as an argument
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    batch_process_directories(root_dir)