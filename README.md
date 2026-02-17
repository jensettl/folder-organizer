# 📁 Folder Organizer

Automatic file organization tool with interactive CLI built with Python and Rich.

![Demo](/assets/demo-manual-run.webp)

## Features

- 🚀 **Automatic Mode**: Organize all files automatically based on file extensions
- 🎯 **Interactive Mode**: Review and decide for each file individually
- 📊 **Rich CLI**: Beautiful command-line interface with progress bars and tables
- 📝 **Detailed Logging**: All operations logged with timestamps
- 🔄 **Smart Renaming**: Automatic handling of filename conflicts
- 🎨 **Customizable**: Easy to extend with new file categories

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd folder-organizer

# Install dependencies
uv sync
```

## Usage

### Quick Start

```bash
# Run in interactive mode (default: Downloads folder)
uv run folder-organizer -i

# Run in automatic mode
uv run folder-organizer --auto

# Organize a custom folder
uv run folder-organizer --source /path/to/folder -i

# Preview changes without moving files
uv run folder-organizer --dry-run -i

# Alternative (on windows) add this function to your PowerShell profile ($PROFILE) for quick access

function organizer {
    Set-Location "C:\Users\User\Documents\coding\_python\folder-organizer"
    uv run folder-organizer
}

# then you can just run `organizer` from any PowerShell prompt to launch the app
```

### Command Line Options

```
-h, --help              Show help message
-s, --source PATH       Source directory to organize (default: Downloads)
--dry-run               Preview changes without moving files
--auto                  Run in automatic mode
-i, --interactive       Run in interactive mode
```

## How It Works

The organizer categorizes files based on their extensions:

- **Documents**: .pdf, .docx, .doc, .ppt, .pptx
- **Images**: .jpg, .png, .gif, .heic, .svg
- **Videos**: .mp4, .avi, .mov, .mkv, .wmv
- **Music**: .mp3, .wav, .flac, .aac
- **Scripts**: .py, .js, .html, .css, .json
- **Spreadsheets**: .xlsx, .xls, .csv
- **Executables**: .exe, .msi
- **Zipped**: .zip, .rar, .tar, .7z, .gz
- **Text**: .txt, .md
- **Others**: Any unrecognized file type

Files are moved to subdirectories within the source folder (e.g., `Downloads/Documents/`, `Downloads/Images/`).

## Interactive Mode

In interactive mode, you can choose an action for each file:

- **[a] Auto**: Move to suggested category
- **[m] Manual**: Choose category manually
- **[d] Delete**: Remove the file
- **[s] Skip**: Leave file as is

## Project Structure

```
folder-organizer/
├── src/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── cli.py               # Rich-based CLI
│   ├── organizer.py         # Core organization logic
│   ├── config.py            # Configuration management
│   ├── file_formats.py      # File extension mappings
│   ├── logger.py            # Logging system
│   └── utils.py             # Helper functions
├── tests/                    # Unit tests
├── logs/                     # Log files (auto-created)
├── pyproject.toml
└── README.md
```

## Development

### Running Tests

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src
```

### Adding New File Categories

Edit `src/file_formats.py` and add new extensions:

```python
FILE_FORMAT_FOLDERS: Dict[str, str] = {
    ".txt": "Text",
    ".new_extension": "YourCategory",
    # ... more extensions
}
```



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
