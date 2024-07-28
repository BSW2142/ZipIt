import os
import zipfile
import subprocess
import sys

# Function to check and install tqdm if not present
def install_tqdm():
    try:
        import tqdm
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tqdm'])
        import tqdm

# Call the function to ensure tqdm is installed
install_tqdm()
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_zip(zip_file, destination):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)

def unzip_all_files_in_directory():
    current_directory = os.getcwd()
    zip_files = [file for file in os.listdir(current_directory) if file.endswith('.zip')]

    with ThreadPoolExecutor() as executor:
        futures = []
        for zip_file in zip_files:
            destination = os.path.join(current_directory, os.path.splitext(zip_file)[0])
            futures.append(executor.submit(extract_zip, zip_file, destination))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Extracting"):
            future.result()  # we can handle exceptions here if needed

if __name__ == "__main__":
    unzip_all_files_in_directory()
