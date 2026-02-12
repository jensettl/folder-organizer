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

## Project Architecture

### Clean Code Principles Applied:

1. **Separation of Concerns**
   - `organizer.py`: Business logic only
   - `cli.py`: User interface only
   - `logger.py`: Logging concerns only
   - `config.py`: Configuration management

2. **Single Responsibility Principle**
   - Each class has one clear purpose
   - Functions do one thing well

3. **Dependency Injection**
   - Config and Logger injected into Organizer and CLI
   - Makes testing easy

4. **Type Hints**
   - All functions have type annotations
   - Better IDE support and catching errors early

5. **Dataclasses**
   - FileInfo and OrganizerConfig as data containers
   - Clean, readable data structures

6. **Error Handling**
   - Graceful error handling throughout
   - All errors logged with context

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

## Development Workflow

```bash
# 1. Make changes to code
# 2. Run tests
uv run pytest

# 3. Test manually with dry-run
uv run folder-organizer --dry-run -i

# 4. Test on real directory
uv run folder-organizer --source /path/to/test/folder -i
```

## Logs Location

All operations are logged to: `logs/organizer_YYYYMMDD_HHMMSS.log`

Example log entry:
```
2024-02-12 14:30:15 | INFO     | MOVED   | Documents      | report.pdf                                -> /Users/you/Downloads/Documents/report.pdf
2024-02-12 14:30:16 | INFO     | RENAMED | name conflict  | photo.jpg -> photo_1.jpg
```
