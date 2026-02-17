# Folder Organizer - Setup & Quick Start

## Installation

```bash
# 1. Navigate to project directory
cd folder-organizer

# 2. Sync dependencies with uv
uv sync

# Optional: Install dev dependencies for testing
uv sync --dev
```

## Quick Start Examples

### 1. Interactive Mode (Recommended for first use)
```bash
uv run folder-organizer -i
```
This will:
- Scan your Downloads folder
- Show you each file
- Let you decide: Auto, Manual, Delete, or Skip

### 2. Automatic Mode
```bash
uv run folder-organizer --auto
```
Automatically organizes all files without prompting.

### 3. Custom Source Directory
```bash
uv run folder-organizer --source ~/Desktop --auto
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_utils.py -v
```


## Extending the Project

### Add New File Category

Edit `src/file_formats.py`:
```python
FILE_FORMAT_FOLDERS: Dict[str, str] = {
    # ... existing mappings
    ".new": "YourCategory",
}
```

### Add New Feature to CLI

Edit `src/cli.py` and add methods to the `CLI` class.

### Modify Logging Format

Edit `src/logger.py` to customize log format or add new log methods.


## Logs Location

All operations are logged to: `logs/organizer_YYYYMMDD_HHMMSS.log`

Example log entry:
```
2024-02-12 14:30:15 | INFO     | MOVED   | Documents      | report.pdf                                -> /Users/you/Downloads/Documents/report.pdf
2024-02-12 14:30:16 | INFO     | RENAMED | name conflict  | photo.jpg -> photo_1.jpg
```
