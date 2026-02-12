"""Core file organization logic."""

import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from .config import OrganizerConfig
from .logger import FileOperationLogger
from .file_formats import FILE_FORMAT_FOLDERS, DEFAULT_CATEGORY
from .utils import (
    get_unique_filename,
    should_ignore_file,
    get_file_category,
    create_destination_dir,
    safe_delete_file,
    format_file_size
)


@dataclass
class FileInfo:
    """Information about a file to be organized."""
    path: Path
    category: str
    size: int
    
    @property
    def name(self) -> str:
        """Get file name."""
        return self.path.name
    
    @property
    def extension(self) -> str:
        """Get file extension."""
        return self.path.suffix.lower()
    
    @property
    def size_formatted(self) -> str:
        """Get formatted file size."""
        return format_file_size(self.size)


class FileOrganizer:
    """Organizes files into categorized folders."""
    
    def __init__(self, config: OrganizerConfig, logger: FileOperationLogger):
        """Initialize organizer.
        
        Args:
            config: Organizer configuration.
            logger: Logger for file operations.
        """
        self.config = config
        self.logger = logger
        self.stats = {
            'total': 0,
            'moved': 0,
            'renamed': 0,
            'deleted': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def scan_files(self) -> List[FileInfo]:
        """Scan source directory for files to organize.
        
        Returns:
            List of FileInfo objects for files that need organization.
        """
        files = []
        
        for item in self.config.source_dir.iterdir():
            # Skip directories
            if item.is_dir():
                continue
            
            # Skip hidden and system files
            if should_ignore_file(item):
                continue
            
            # Get file info
            try:
                category = get_file_category(item, FILE_FORMAT_FOLDERS, DEFAULT_CATEGORY)
                size = item.stat().st_size
                
                files.append(FileInfo(
                    path=item,
                    category=category,
                    size=size
                ))
            except Exception as e:
                self.logger.log_error(item, e)
                self.stats['errors'] += 1
        
        return files
    
    def move_file(self, file_info: FileInfo) -> Tuple[bool, Optional[Path]]:
        """Move file to its category folder.
        
        Args:
            file_info: Information about file to move.
            
        Returns:
            Tuple of (success, destination_path).
        """
        try:
            # Create destination directory
            dest_dir = create_destination_dir(
                self.config.destination_base,
                file_info.category
            )
            
            # Calculate destination path
            dest_path = dest_dir / file_info.name
            
            # Handle name conflicts
            if dest_path.exists():
                original_dest = dest_path
                dest_path = get_unique_filename(dest_path)
                self.logger.log_rename(original_dest, dest_path, "name conflict")
                self.stats['renamed'] += 1
            
            # Move file
            shutil.move(str(file_info.path), str(dest_path))
            
            # Log operation
            self.logger.log_move(file_info.path, dest_path, file_info.category)
            self.stats['moved'] += 1
            
            return True, dest_path
            
        except Exception as e:
            self.logger.log_error(file_info.path, e)
            self.stats['errors'] += 1
            return False, None
    
    def delete_file(self, file_info: FileInfo) -> bool:
        """Delete a file.
        
        Args:
            file_info: Information about file to delete.
            
        Returns:
            True if deletion successful.
        """
        try:
            success = safe_delete_file(file_info.path)
            if not success:
                raise FileNotFoundError(f"Could not delete {file_info.path}")
            
            self.logger.log_delete(file_info.path, "user request")
            self.stats['deleted'] += 1
            return True
            
        except Exception as e:
            self.logger.log_error(file_info.path, e)
            self.stats['errors'] += 1
            return False
    
    def skip_file(self, file_info: FileInfo, reason: str = "user choice") -> None:
        """Skip organizing a file.
        
        Args:
            file_info: Information about file to skip.
            reason: Reason for skipping.
        """
        self.logger.log_skip(file_info.path, reason)
        self.stats['skipped'] += 1
    
    def organize_all(self) -> Dict[str, int]:
        """Organize all files automatically.
        
        Returns:
            Statistics dictionary.
        """
        files = self.scan_files()
        self.stats['total'] = len(files)
        
        for file_info in files:
            self.move_file(file_info)
        
        self.logger.log_summary(self.stats)
        return self.stats
    
    def get_stats(self) -> Dict[str, int]:
        """Get current operation statistics.
        
        Returns:
            Statistics dictionary.
        """
        return self.stats.copy()
