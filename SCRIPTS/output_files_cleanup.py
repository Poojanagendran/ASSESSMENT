import os
import glob
from SCRIPTS.COMMON.io_user_directory import *

# Specify the parent folder path
folder_path = output_common_dir
print(folder_path)

# Use glob to recursively find .xls and .xlsx files in all subfolders
files_to_delete = glob.glob(os.path.join(folder_path, '**', '*.xls*'), recursive=True)

# Loop through the files and delete them
for file in files_to_delete:
    try:
        os.remove(file)
        print(f"Deleted: {file}")
    except Exception as e:
        print(f"Could not delete {file}: {e}")
