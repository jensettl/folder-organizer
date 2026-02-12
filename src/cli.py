"""Command-line interface with rich library."""

from pathlib import Path
from typing import List, Optional
from enum import Enum

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.tree import Tree
from rich import box

from .config import OrganizerConfig
from .logger import FileOperationLogger
from .organizer import FileOrganizer, FileInfo


class UserAction(Enum):
    """User actions in interactive mode."""
    AUTO = "auto"
    MANUAL = "manual"
    DELETE = "delete"
    SKIP = "skip"


class CLI:
    """Command-line interface for folder organizer."""
    
    def __init__(self, config: OrganizerConfig):
        """Initialize CLI.
        
        Args:
            config: Organizer configuration.
        """
        self.config = config
        self.console = Console()
        self.logger = None
        self.organizer = None
    
    def _ensure_logger(self) -> None:
        """Ensure logger is initialized (lazy initialization)."""
        if self.logger is None:
            self.logger = FileOperationLogger(self.config.log_dir)
            self.organizer = FileOrganizer(self.config, self.logger)
    
    def show_banner(self) -> None:
        """Display application banner."""
        banner = """
╔═══════════════════════════════════════════╗
║     📁 Folder Organizer                   ║
║     Organize your files automatically     ║
╚═══════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")
    
    def show_config(self) -> None:
        """Display current configuration."""
        config_table = Table(title="Configuration", box=box.ROUNDED)
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="yellow")
        
        config_table.add_row("Source Directory", str(self.config.source_dir))
        config_table.add_row("Destination Base", str(self.config.destination_base))
        config_table.add_row("Log Directory", str(self.config.log_dir))
        
        self.console.print(config_table)
        self.console.print()
    
    def scan_and_preview(self) -> List[FileInfo]:
        """Scan files and show preview.
        
        Returns:
            List of FileInfo objects.
        """
        self._ensure_logger()
        
        self.console.print("[bold]Scanning files...[/bold]")
        files = self.organizer.scan_files()
        
        if not files:
            self.console.print("[yellow]No files found to organize.[/yellow]")
            return []
        
        # Show summary by category
        categories = {}
        for file_info in files:
            categories[file_info.category] = categories.get(file_info.category, 0) + 1
        
        preview_table = Table(title=f"Found {len(files)} files", box=box.ROUNDED)
        preview_table.add_column("Category", style="cyan")
        preview_table.add_column("Count", style="magenta", justify="right")
        
        for category, count in sorted(categories.items()):
            preview_table.add_row(category, str(count))
        
        self.console.print(preview_table)
        self.console.print()
        
        return files
    
    def run_automatic_mode(self) -> None:
        """Run automatic organization mode."""
        self.console.print("[bold green]Automatic Mode[/bold green]")
        self.console.print()
        
        files = self.scan_and_preview()
        if not files:
            return
        
        # Confirm before proceeding
        if not Confirm.ask("Proceed with automatic organization?", default=False):
            self.console.print("[yellow]Operation cancelled.[/yellow]")
            return
        
        # Process files with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("Organizing files...", total=len(files))
            
            for file_info in files:
                self.organizer.move_file(file_info)
                progress.update(task, advance=1)
        
        self._show_summary()
    
    def run_interactive_mode(self) -> None:
        """Run interactive organization mode."""
        self.console.print("[bold blue]Interactive Mode[/bold blue]")
        self.console.print()
        
        files = self.scan_and_preview()
        if not files:
            return
        
        self.console.print("[dim]For each file, choose an action:[/dim]")
        self.console.print("[dim]  [a] Auto - move to suggested category[/dim]")
        self.console.print("[dim]  [m] Manual - choose category manually[/dim]")
        self.console.print("[dim]  [d] Delete - remove file[/dim]")
        self.console.print("[dim]  [s] Skip - leave file as is[/dim]")
        self.console.print()
        
        self.organizer.stats['total'] = len(files)
        
        for i, file_info in enumerate(files, 1):
            self._process_file_interactive(file_info, i, len(files))
        
        self._show_summary()
    
    def _process_file_interactive(self, file_info: FileInfo, index: int, total: int) -> None:
        """Process single file in interactive mode.
        
        Args:
            file_info: File information.
            index: Current file index.
            total: Total number of files.
        """
        # Show file info
        panel = Panel(
            f"[bold]{file_info.name}[/bold]\n"
            f"Category: [cyan]{file_info.category}[/cyan]\n"
            f"Size: [yellow]{file_info.size_formatted}[/yellow]",
            title=f"File {index}/{total}",
            border_style="blue"
        )
        self.console.print(panel)
        
        # Get user choice
        choice = Prompt.ask(
            "Action",
            choices=["a", "m", "d", "s"],
            default="a"
        )
        
        if choice == "a":
            # Auto move
            success, _ = self.organizer.move_file(file_info)
            if success:
                self.console.print(f"[green]✓ Moved to {file_info.category}[/green]")
        
        elif choice == "m":
            # Manual category selection
            self._manual_category_selection(file_info)
        
        elif choice == "d":
            # Delete
            if Confirm.ask("Are you sure you want to delete this file?", default=False):
                if self.organizer.delete_file(file_info):
                    self.console.print("[red]✓ Deleted[/red]")
            else:
                self.organizer.skip_file(file_info, "delete cancelled")
                self.console.print("[yellow]✓ Skipped[/yellow]")
        
        elif choice == "s":
            # Skip
            self.organizer.skip_file(file_info)
            self.console.print("[yellow]✓ Skipped[/yellow]")
        
        self.console.print()
    
    def _manual_category_selection(self, file_info: FileInfo) -> None:
        """Let user manually select category.
        
        Args:
            file_info: File information.
        """
        from .file_formats import FILE_FORMAT_FOLDERS
        
        # Get unique categories
        categories = sorted(set(FILE_FORMAT_FOLDERS.values()))
        categories.append("Others")
        
        # Show categories
        self.console.print("[bold]Available categories:[/bold]")
        for i, cat in enumerate(categories, 1):
            self.console.print(f"  [{i}] {cat}")
        
        # Get choice
        choice = Prompt.ask(
            "Select category number",
            choices=[str(i) for i in range(1, len(categories) + 1)],
            default="1"
        )
        
        selected_category = categories[int(choice) - 1]
        
        # Update category and move
        file_info.category = selected_category
        success, _ = self.organizer.move_file(file_info)
        if success:
            self.console.print(f"[green]✓ Moved to {selected_category}[/green]")
    
    def _show_summary(self) -> None:
        """Show operation summary."""
        stats = self.organizer.get_stats()
        
        summary_table = Table(title="Summary", box=box.ROUNDED, style="bold")
        summary_table.add_column("Operation", style="cyan")
        summary_table.add_column("Count", style="magenta", justify="right")
        
        summary_table.add_row("Total Files", str(stats['total']))
        summary_table.add_row("Moved", f"[green]{stats['moved']}[/green]")
        summary_table.add_row("Renamed (conflicts)", f"[yellow]{stats['renamed']}[/yellow]")
        summary_table.add_row("Deleted", f"[red]{stats['deleted']}[/red]")
        summary_table.add_row("Skipped", f"[dim]{stats['skipped']}[/dim]")
        summary_table.add_row("Errors", f"[red]{stats['errors']}[/red]")
        
        self.console.print()
        self.console.print(summary_table)
        
        # Show log file location
        self.console.print()
        self.console.print(
            f"[dim]Log file: {self.logger.get_log_path()}[/dim]"
        )
    
    def select_mode(self) -> str:
        """Let user select organization mode.
        
        Returns:
            Selected mode ('auto' or 'interactive').
        """
        self.console.print("[bold]Select Mode:[/bold]")
        self.console.print("  [1] Automatic - organize all files automatically")
        self.console.print("  [2] Interactive - review each file individually")
        self.console.print()
        
        choice = Prompt.ask(
            "Mode",
            choices=["1", "2"],
            default="1"
        )
        
        return "auto" if choice == "1" else "interactive"
