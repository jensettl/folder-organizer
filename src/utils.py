"""Utility functions for file operations."""

from pathlib import Path


def get_unique_filename(file_path: Path) -> Path:
    """Generate unique filename if file already exists.
    
    If file.txt exists, returns file_1.txt.
    If file_1.txt exists, returns file_2.txt, etc.
    
    Args:
        file_path: Original file path.
        
    Returns:
        Unique file path.
    """
    if not file_path.exists():
        return file_path
    
    stem = file_path.stem
    suffix = file_path.suffix
    parent = file_path.parent
    
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        
        if not new_path.exists():
            return new_path
        
        counter += 1
        
        # Safety check to prevent infinite loop
        if counter > 9999:
            raise ValueError(f"Too many files with same name: {file_path.name}")


def is_hidden_file(file_path: Path) -> bool:
    """Check if file is hidden (starts with dot).
    
    Args:
        file_path: File path to check.
        
    Returns:
        True if file is hidden.
    """
    return file_path.name.startswith('.')


def is_system_file(file_path: Path) -> bool:
    """Check if file is a system file that should be ignored.
    
    Args:
        file_path: File path to check.
        
    Returns:
        True if file should be ignored.
    """
    system_files = {
        '.DS_Store',
        'Thumbs.db',
        'desktop.ini',
        '.localized'
    }
    return file_path.name in system_files


def should_ignore_file(file_path: Path) -> bool:
    """Check if file should be ignored during organization.
    
    Args:
        file_path: File path to check.
        
    Returns:
        True if file should be ignored.
    """
    return is_hidden_file(file_path) or is_system_file(file_path)


def get_file_category(file_path: Path, format_mapping: dict, default: str = "Others") -> str:
    """Get category for a file based on its extension.
    
    Args:
        file_path: Path to the file.
        format_mapping: Dictionary mapping extensions to categories.
        default: Default category for unknown extensions.
        
    Returns:
        Category name.
    """
    extension = file_path.suffix.lower()
    return format_mapping.get(extension, default)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: File size in bytes.
        
    Returns:
        Formatted string (e.g., "1.5 MB").
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def create_destination_dir(base_path: Path, category: str) -> Path:
    """Create destination directory for a category.
    
    Args:
        base_path: Base directory path.
        category: Category name.
        
    Returns:
        Path to category directory.
    """
    dest_dir = base_path / category
    dest_dir.mkdir(exist_ok=True)
    return dest_dir


def safe_delete_file(file_path: Path) -> bool:
    """Safely delete a file.
    
    Args:
        file_path: Path to file to delete.
        
    Returns:
        True if deletion successful, False otherwise.
    """
    try:
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False
