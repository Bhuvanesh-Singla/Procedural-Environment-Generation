import os
import glob

def rename(new_name):
    # Get the list of files in the specified directory
    path = r'C:\Users\singl\Desktop\Bhuvanesh\NITK\Procedural Environment Generation\Dataset\skydark\trial3'
    files = os.listdir(path)
    old = 'heightmap.png'
    old_path = os.path.join(path, old)
    # Iterate through the files
    for file_name in files:
        # Check if the file name starts with the old prefix
        if file_name == old:
            # Construct the full paths for the old and new files
            old_path = os.path.join(path, file_name)
            new_path = os.path.join(path, new_name)
            # Rename the file
            os.rename(old_path, new_path)
            print('renamed')

            pattern = os.path.join(path, 'heightmap(*).png')
            matching_files = glob.glob(pattern)
            for file_path in matching_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            print("duplicate clr")
            return True
    return False
            
