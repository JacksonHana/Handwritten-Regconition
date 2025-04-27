import os
import shutil

# Set your source and destination folders
src_folder = '../datasets/IAM_sentences/dataset'    # where all images are now
dst_folder = '../datasets/dataset'         # where you want the new structure

# Loop through all files in the source folder
for filename in os.listdir(src_folder):
    if filename.endswith('.png'):
        # Example filename: a01-000u-s00-00.png

        parts = filename.split('-')  # split by '-'
        if len(parts) >= 2:
            first_folder = parts[0]      # a01
            second_folder = parts[0] + '-' + parts[1]  # a01-000u

            # Build the full path
            target_dir = os.path.join(dst_folder, first_folder, second_folder)
            os.makedirs(target_dir, exist_ok=True)  # Create folders if not exist

            # Copy the file
            src_path = os.path.join(src_folder, filename)
            dst_path = os.path.join(target_dir, filename)
            shutil.copy2(src_path, dst_path)

print('Done!')
