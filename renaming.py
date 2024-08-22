import os
import argparse

def create_full_tutorial_folder(parent_folder):
    """
    Creates a new folder with '_full_tutorial_video' appended to the parent folder name
    inside the parent folder, without affecting existing files.
    
    :param parent_folder: The path to the parent folder where the new folder will be created.
    """
    # Ensure the parent folder exists
    if not os.path.exists(parent_folder):
        raise FileNotFoundError(f"Parent folder does not exist: {parent_folder}")
    
    # Get the name of the new folder
    parent_folder_name = os.path.basename(parent_folder)
    new_folder_name = f"{parent_folder_name}_full_tutorial_video"
    new_folder_path = os.path.join(parent_folder, new_folder_name)
    
    # Create the new folder if it does not already exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Successfully created new folder: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Create a new folder in the parent directory with '_full_tutorial_video' appended.")
    parser.add_argument('parent_folder', type=str, help="Path to the parent folder where the new folder will be created.")
    
    args = parser.parse_args()
    
    # Create the new folder
    create_full_tutorial_folder(args.parent_folder)
