import os
from pathlib import Path
import logging

# List of files to create
files_to_create = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trials.ipynb",
]

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Loop through the list and ensure directories and files exist
for file_path in files_to_create:
    path = Path(file_path)
    directory, file_name = os.path.split(path)

    # Create directory if it doesn't exist
    if directory:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Directory created: {directory} for file: {file_name}")

    # Create the file if it doesn't exist or if it's empty
    if not path.exists() or path.stat().st_size == 0:
        with open(path, "w") as file:
            pass
        logging.info(f"Empty file created: {path}")
    else:
        logging.info(f"File already exists: {file_name}")
