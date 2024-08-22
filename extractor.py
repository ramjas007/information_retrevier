import os
import zipfile
import rarfile
import argparse

def extract_archive(archive_path, extract_to_path):
    """
    Extracts a ZIP or RAR archive to the specified directory.

    :param archive_path: Path to the archive file (ZIP or RAR).
    :param extract_to_path: Directory where files should be extracted.
    """
    # Ensure the output directory exists
    os.makedirs(extract_to_path, exist_ok=True)
    
    # Check the file extension and use the appropriate method
    if archive_path.lower().endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(path=extract_to_path)
            print(f"Successfully extracted ZIP file: {archive_path} to {extract_to_path}")
    elif archive_path.lower().endswith('.rar'):
        with rarfile.RarFile(archive_path, 'r') as rf:
            rf.extractall(path=extract_to_path)
            print(f"Successfully extracted RAR file: {archive_path} to {extract_to_path}")
    else:
        raise ValueError("Unsupported archive format. Please provide a .zip or .rar file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ZIP or RAR archives.")
    
    # Define the command-line arguments
    parser.add_argument('archive_path', type=str, help="Path to the archive file (.zip or .rar).")
    parser.add_argument('extract_to_path', type=str, help="Directory where files should be extracted.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Extract the archive using the provided paths
    extract_archive(args.archive_path, args.extract_to_path)
