"""Application configuration and settings."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class OrganizerConfig:
    """Configuration for the folder organizer."""
    
    source_dir: Path
    destination_base: Path
    log_dir: Path
    
    @classmethod
    def create_default(cls, source_dir: Optional[Path] = None) -> "OrganizerConfig":
        """Create default configuration.
        
        Args:
            source_dir: Source directory to organize. Defaults to Downloads folder.
            
        Returns:
            OrganizerConfig instance with default settings.
        """
        if source_dir is None:
            # Default to Downloads folder
            source_dir = Path.home() / "Downloads"
        
        # Destination is the same as source by default
        # (creates subdirectories like Downloads/Documents, Downloads/Images, etc.)
        destination_base = source_dir
        
        # Log directory in project root
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        return cls(
            source_dir=source_dir,
            destination_base=destination_base,
            log_dir=log_dir
        )
    
    def validate(self) -> bool:
        """Validate configuration.
        
        Returns:
            True if configuration is valid.
            
        Raises:
            ValueError: If source directory doesn't exist.
        """
        if not self.source_dir.exists():
            raise ValueError(f"Source directory does not exist: {self.source_dir}")
        
        if not self.source_dir.is_dir():
            raise ValueError(f"Source path is not a directory: {self.source_dir}")
        
        return True
    
    def __str__(self) -> str:
        """String representation of config."""
        return (
            f"OrganizerConfig(\n"
            f"  source: {self.source_dir}\n"
            f"  destination: {self.destination_base}\n"
            f"  logs: {self.log_dir}\n"
            f")"
        )
