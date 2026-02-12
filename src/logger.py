"""Logging system for file operations."""

import logging
from pathlib import Path
from datetime import datetime
from enum import Enum


class ActionType(Enum):
    """Types of file operations."""
    MOVED = "MOVED"
    RENAMED = "RENAMED"
    DELETED = "DELETED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


class FileOperationLogger:
    """Logger for file operations with structured output."""
    
    def __init__(self, log_dir: Path):
        """Initialize logger.
        
        Args:
            log_dir: Directory to store log files.
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"organizer_{timestamp}.log"
        
        # Configure logger
        self.logger = logging.getLogger("folder_organizer")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler (optional, for debugging)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.log_file = log_file
        self._log_session_start()
    
    def _log_session_start(self) -> None:
        """Log session start."""
        self.logger.info("=" * 80)
        self.logger.info("File Organization Session Started")
        self.logger.info("=" * 80)
    
    def log_move(self, source: Path, destination: Path, category: str) -> None:
        """Log file move operation.
        
        Args:
            source: Source file path.
            destination: Destination file path.
            category: File category.
        """
        self.logger.info(
            f"{ActionType.MOVED.value} | {category:15s} | {source.name:40s} -> {destination}"
        )
    
    def log_rename(self, original: Path, renamed: Path, reason: str = "conflict") -> None:
        """Log file rename operation.
        
        Args:
            original: Original file path.
            renamed: New file path.
            reason: Reason for rename.
        """
        self.logger.info(
            f"{ActionType.RENAMED.value} | {reason:15s} | {original.name} -> {renamed.name}"
        )
    
    def log_delete(self, file_path: Path, reason: str = "user request") -> None:
        """Log file deletion.
        
        Args:
            file_path: Path of deleted file.
            reason: Reason for deletion.
        """
        self.logger.warning(
            f"{ActionType.DELETED.value} | {reason:15s} | {file_path.name}"
        )
    
    def log_skip(self, file_path: Path, reason: str) -> None:
        """Log skipped file.
        
        Args:
            file_path: Path of skipped file.
            reason: Reason for skipping.
        """
        self.logger.info(
            f"{ActionType.SKIPPED.value} | {reason:15s} | {file_path.name}"
        )
    
    def log_error(self, file_path: Path, error: Exception) -> None:
        """Log error during file operation.
        
        Args:
            file_path: Path of file that caused error.
            error: Exception that occurred.
        """
        self.logger.error(
            f"{ActionType.ERROR.value} | {type(error).__name__:15s} | {file_path.name} | {str(error)}"
        )
    
    def log_summary(self, stats: dict) -> None:
        """Log session summary.
        
        Args:
            stats: Dictionary with operation statistics.
        """
        self.logger.info("=" * 80)
        self.logger.info("Session Summary:")
        self.logger.info(f"  Files processed: {stats.get('total', 0)}")
        self.logger.info(f"  Moved: {stats.get('moved', 0)}")
        self.logger.info(f"  Renamed: {stats.get('renamed', 0)}")
        self.logger.info(f"  Deleted: {stats.get('deleted', 0)}")
        self.logger.info(f"  Skipped: {stats.get('skipped', 0)}")
        self.logger.info(f"  Errors: {stats.get('errors', 0)}")
        self.logger.info("=" * 80)
    
    def get_log_path(self) -> Path:
        """Get path to current log file.
        
        Returns:
            Path to log file.
        """
        return self.log_file
