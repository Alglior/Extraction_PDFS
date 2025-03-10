import os
from PIL import Image

def convert_png_to_jpg(src_root, dst_root):
    for root, dirs, files in os.walk(src_root):
        print(f"Processing directory: {root}")
        for file in files:
            if file.lower().endswith('.png'):
                src_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, src_root)
                dst_dir = os.path.join(dst_root, relative_path)
                os.makedirs(dst_dir, exist_ok=True)
                dst_file_path = os.path.join(dst_dir, os.path.splitext(file)[0] + '.jpg')
                
                with Image.open(src_file_path) as img:
                    rgb_img = img.convert('RGB')
                    rgb_img.save(dst_file_path, 'JPEG')

# Example usage
convert_png_to_jpg('extracted_pages', 'output_images')
