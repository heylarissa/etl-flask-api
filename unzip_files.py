import zipfile
import os
import shutil

ZIP_FILENAME = "dados.zip"
OUTPUT_DIR = f"{os.getcwd()}/data"
BACKUP_DIR = os.path.join(OUTPUT_DIR, "backup")


def create_backup_folder(backup_dir: str = BACKUP_DIR):
    """Ensures the backup folder exists."""
    os.makedirs(backup_dir, exist_ok=True)


def extract_zip(zip_path, destination):
    """Extracts the ZIP file to the specified directory."""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destination)
    print(f"Files extracted to: {destination}")


def move_file(source, destination):
    """Moves a file to a new location."""
    if os.path.exists(source):
        shutil.move(source, destination)
        print(f"'{os.path.basename(source)}' moved to {destination}")
    else:
        print(f"Error: '{os.path.basename(source)}' not found.")


def unzip_files(
    zip_filename: str = ZIP_FILENAME,
    backup_dir: str = BACKUP_DIR,
    output_dir: str = OUTPUT_DIR,
):
    """Executes the extraction and file moving process."""
    if not os.path.exists(zip_filename):
        print(f"Error: {zip_filename} not found.")
        return

    create_backup_folder()
    extract_zip(zip_filename, output_dir)
    move_file(zip_filename, os.path.join(backup_dir, zip_filename))


if __name__ == "__main__":
    unzip_files()
