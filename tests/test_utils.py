"""Unit tests for utility functions."""

import pytest
from pathlib import Path
import tempfile
import shutil

from src.utils import (
    get_unique_filename,
    is_hidden_file,
    is_system_file,
    should_ignore_file,
    get_file_category,
    format_file_size,
)


class TestGetUniqueFilename:
    """Tests for get_unique_filename function."""
    
    def test_unique_filename_no_conflict(self, tmp_path):
        """Test when file doesn't exist."""
        file_path = tmp_path / "test.txt"
        result = get_unique_filename(file_path)
        assert result == file_path
    
    def test_unique_filename_with_conflict(self, tmp_path):
        """Test when file exists."""
        # Create original file
        file_path = tmp_path / "test.txt"
        file_path.touch()
        
        # Get unique name
        result = get_unique_filename(file_path)
        assert result == tmp_path / "test_1.txt"
    
    def test_unique_filename_multiple_conflicts(self, tmp_path):
        """Test with multiple existing files."""
        # Create multiple files
        (tmp_path / "test.txt").touch()
        (tmp_path / "test_1.txt").touch()
        (tmp_path / "test_2.txt").touch()
        
        # Get unique name
        result = get_unique_filename(tmp_path / "test.txt")
        assert result == tmp_path / "test_3.txt"


class TestFileChecks:
    """Tests for file checking functions."""
    
    def test_is_hidden_file(self):
        """Test hidden file detection."""
        assert is_hidden_file(Path(".hidden"))
        assert is_hidden_file(Path(".DS_Store"))
        assert not is_hidden_file(Path("visible.txt"))
    
    def test_is_system_file(self):
        """Test system file detection."""
        assert is_system_file(Path(".DS_Store"))
        assert is_system_file(Path("Thumbs.db"))
        assert is_system_file(Path("desktop.ini"))
        assert not is_system_file(Path("normal.txt"))
    
    def test_should_ignore_file(self):
        """Test combined ignore check."""
        assert should_ignore_file(Path(".hidden"))
        assert should_ignore_file(Path(".DS_Store"))
        assert not should_ignore_file(Path("normal.txt"))


class TestGetFileCategory:
    """Tests for get_file_category function."""
    
    def test_known_extension(self):
        """Test categorization of known extensions."""
        mapping = {
            ".pdf": "Documents",
            ".jpg": "Images",
            ".mp3": "Music"
        }
        
        assert get_file_category(Path("test.pdf"), mapping) == "Documents"
        assert get_file_category(Path("photo.jpg"), mapping) == "Images"
        assert get_file_category(Path("song.mp3"), mapping) == "Music"
    
    def test_unknown_extension(self):
        """Test default category for unknown extensions."""
        mapping = {".pdf": "Documents"}
        
        assert get_file_category(Path("test.xyz"), mapping, "Others") == "Others"
    
    def test_case_insensitive(self):
        """Test case-insensitive extension matching."""
        mapping = {".pdf": "Documents"}
        
        assert get_file_category(Path("test.PDF"), mapping) == "Documents"
        assert get_file_category(Path("test.Pdf"), mapping) == "Documents"


class TestFormatFileSize:
    """Tests for format_file_size function."""
    
    def test_bytes(self):
        """Test byte formatting."""
        assert format_file_size(500) == "500.0 B"
    
    def test_kilobytes(self):
        """Test kilobyte formatting."""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1536) == "1.5 KB"
    
    def test_megabytes(self):
        """Test megabyte formatting."""
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 2.5) == "2.5 MB"
    
    def test_gigabytes(self):
        """Test gigabyte formatting."""
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"
