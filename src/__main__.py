"""Main entry point for the folder organizer application."""

import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

from .config import OrganizerConfig
from .logger import FileOperationLogger
from .cli import CLI


def parse_arguments() -> dict:
    """Parse command line arguments (simplified).
    
    Returns:
        Dictionary with parsed arguments.
    """
    args = {
        'source': None,
        'mode': None
    }
    
    # Simple argument parsing
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    
    if '--auto' in sys.argv:
        args['mode'] = 'auto'
    
    if '--interactive' in sys.argv or '-i' in sys.argv:
        args['mode'] = 'interactive'
    
    # Source directory
    for i, arg in enumerate(sys.argv):
        if arg in ['--source', '-s'] and i + 1 < len(sys.argv):
            args['source'] = Path(sys.argv[i + 1])
    
    return args


def print_help() -> None:
    """Print help message."""
    help_text = """
Folder Organizer - Automatic file organization tool

USAGE:
    folder-organizer [OPTIONS]

OPTIONS:
    -h, --help              Show this help message
    -s, --source PATH       Source directory to organize (default: Downloads)
    --auto                  Run in automatic mode
    -i, --interactive       Run in interactive mode

EXAMPLES:
    # Organize Downloads folder interactively
    folder-organizer -i

    # Organize custom folder automatically
    folder-organizer --source /path/to/folder --auto
    """
    print(help_text)


def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code (0 for success, 1 for error).
    """
    console = Console()
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create configuration
        config = OrganizerConfig.create_default(args['source'])
        
        # Validate configuration
        config.validate()
        
        # Create CLI
        cli = CLI(config)
        
        # Show banner
        cli.show_banner()
        
        # Show configuration
        cli.show_config()
        
        # Select or use provided mode
        mode = args['mode']
        if mode is None:
            mode = cli.select_mode()
        
        # Run selected mode
        if mode == 'auto':
            cli.run_automatic_mode()
        else:
            cli.run_interactive_mode()
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        return 1
    
    except Exception as e:
        console.print(f"\n[red bold]Error:[/red bold] {str(e)}")
        if '--debug' in sys.argv:
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main())
