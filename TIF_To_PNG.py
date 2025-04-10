# import os
# from PIL import Image

# def convert_tif_to_png(input_folder, output_folder):
#     # Ensure output folder exists
#     os.makedirs(output_folder, exist_ok=True)
    
#     # Loop through all .tif files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith(".tif"):
#             input_path = os.path.join(input_folder, filename)
#             output_path = os.path.join(output_folder, filename.replace(".tif", ".png"))
            
#             # Open and convert to PNG
#             with Image.open(input_path) as img:
#                 img.save(output_path, format="PNG")
#                 print(f"Converted: {filename} -> {output_path}")

# input_folder = "Input_Images"
# output_folder = "Compatible_Input"  # Replace with your actual output folder path
# convert_tif_to_png(input_folder, output_folder)

import os
import shutil
from PIL import Image

def convert_tif_to_png(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Skip non-image files
        if not os.path.isfile(input_path):
            continue

        lower_filename = filename.lower()
        
        if lower_filename.endswith(".png"):
            # Directly copy PNG file
            output_path = os.path.join(output_folder, filename)
            shutil.copy2(input_path, output_path)
            print(f"Copied PNG: {filename} -> {output_path}")
        
        elif lower_filename.endswith(".tif") or lower_filename.endswith(".tiff"):
            # Convert TIF to PNG
            output_path = os.path.join(output_folder, filename.replace(".tif", ".png").replace(".tiff", ".png"))
            with Image.open(input_path) as img:
                img.save(output_path, format="PNG")
                print(f"Converted: {filename} -> {output_path}")

# Example usage
input_folder = "Input_Images"
output_folder = "Compatible_Input"
convert_tif_to_png(input_folder, output_folder)
