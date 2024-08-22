import os
import argparse

def list_files_in_directory(directory_path):
    """
    List all files in a directory and its subdirectories.
    """
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def filter_video_files(file_paths):
    """
    Filter video files from a list of file paths.
    """
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']
    video_file_paths = [
        path for path in file_paths
        if any(path.lower().endswith(ext) for ext in video_extensions)
    ]
    return video_file_paths

def get_video_files(root_folder):
    """
    Main function to extract video file paths.
    """
    file_paths = list_files_in_directory(root_folder)
    video_file_paths = filter_video_files(file_paths)
    return video_file_paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract video file paths from a parent folder.")
    parser.add_argument('root_folder', type=str, help="Root folder to search for video files.")
    
    args = parser.parse_args()
    video_file_paths = get_video_files(args.root_folder)
    
    for video_path in video_file_paths:
        print(f"Video file path: {video_path}")
