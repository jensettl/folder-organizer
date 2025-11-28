import logging
import time
from pathlib import Path
from tqdm import tqdm
from assets.file_formats import FILE_FORMAT_FOLDERS
from src.utils import clear_console, invalid_path, not_a_file, sort_file

FOLDER = "Downloads" # Name of the folder to be sorted
FOLDER_PATH = Path.joinpath(Path.home(), FOLDER)  # Path to the folder to be sorted
LOGFILE = Path.joinpath(Path("logs"), f"folder_cleanup_{FOLDER}.log")

SLEEP_TIME = 0.3  # Time to sleep between processing files (in seconds)

if invalid_path(LOGFILE.parent):
    LOGFILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOGFILE), logging.StreamHandler()],
)

def main() -> None:
    """ Main function to sort files in the specified folder. """

    if invalid_path(FOLDER_PATH):
        logging.error(f"FOLDER_PATH Variable is invalid, got: {FOLDER_PATH}")
        return

    clear_console()

    mode = (
            input(
    f"""
    Welcome to Download Organizer!
    You are about to sort files in the folder: {FOLDER_PATH}

        (1) Automatically sort your files
        (2) Manually sort your files

        (q to quit)

    Select mode for sorting files:  """
        )
    )

    clear_console()

    if mode.lower() == "q":
        logging.info("Quitting the program.")
        return

    mode = "auto" if mode == "1" else "manual" if mode == "2" else None
    files = [file for file in FOLDER_PATH.iterdir() if not not_a_file(file)]

    if mode is None:
        logging.error(f"Invalid Input: {mode}")
        return
    
    logging.info(f"START SORTING {len(files)} FILES IN {FOLDER_PATH} (MODE: {mode.upper()})")

    for file in tqdm(files, total=len(files), desc="Sorting files"):
        logging.info(f"Processing file: {file.name} in {FOLDER_PATH}")
        sort_file(file, mode)
        time.sleep(SLEEP_TIME)
        if(mode == "manual"):
            clear_console()

    logging.info("SORTING COMPLETED.\n")
    

if __name__ == "__main__":
    main()
