> simple script to organize your downloads folder based on file types

# download-organizer

The **download-organizer** is a Python script that automatically sorts files into different folders based on their file format. The script uses the _Downloads folder_ by default (this can be adjusted by changing the _PATH_ constant)
The script has two modes of operation: automatic sorting or an assisted manual sorting. It also includes logging functionality to keep track of the sorting process.

This simple script helped me to unclutter my Downloads folder. It might help you too! Installation and usage instructions are provided below.

### How it works

In assets folder, the user can define which file formats should be sorted into which folders. The file maps each file format to a specific folder name. If a file format is not defined in the mapping, the file will be moved to an "Other" folder. 

Code snippet demonstrating the file format to folder mapping:

```python
   # Get the file format of the file and determine destination folder
    file_type = file.suffix.lower()
    target_folder : str = FILE_FORMAT_FOLDERS.get(file_type, "Other")
    target_path : Path = Path.joinpath(file.parent, target_folder)

   # Move the file to the corresponding folder in automatic mode
    if mode == "auto":
        try:
            logging.info(f"Moving {file.name} to {target_folder} folder")
            file.rename(Path.joinpath(target_path, file.name))
        except Exception as e:
            logging.error(f"Error moving {file.name}: {e}")
```

### How i use it on my machine

I have the repository cloned on my local machine and created a simple batch script to run it straight from my desktop:

```bash
@echo off
cd /d "<PATH TO REPOSITORY>\download-organizer"
uv run main.py
pause
```

### Requirements

- last tested with Python 3.14
- logging>=0.4.9.6
- pathlib>=1.0.1
- tqdm>=4.67.1

The repository is developed with `uv`. So you can install all the necessary dependencies with `uv sync`.

### Usage

1. Clone the repository to your local machine.
2. Adjust the `PATH` variable in `main.py` to the path of the directory you want to sort.
3. Add any file formats you want to sort to the `assets` dictionary in `file_formats.py`.
3. Run the script using `uv run main.py` and follow the CLI instructions.

# Contributing

I have more features planned, such as scheduling the script, adding a GUI, or add context-based sorting by analyzing file names and contents.
If you would like to contribute, please fork the repository and submit a pull request.
