#!/usr/bin/env python3
"""
Test script to verify that colors are working in the animated progress system.
"""

from animated_progress import SyncProgressDisplay, AnimatedLoader
from utils import Logger
import time

def test_colors():
    """Test all the color codes."""
    print("🎨 Testing ANSI color codes:")
    print(f"   {Logger.format_message('INFO message', Logger.INFO)}")
    print(f"   {Logger.format_message('SUCCESS message', Logger.SUCCESS)}")
    print(f"   {Logger.format_message('WARNING message', Logger.WARNING)}")
    print(f"   {Logger.format_message('ERROR message', Logger.ERROR)}")
    print(f"   {Logger.format_message('INFO_SECONDARY message', Logger.INFO_SECONDARY)}")
    print(f"   {Logger.format_message('DEBUG message', Logger.DEBUG)}")
    print()

def test_animated_progress():
    """Test the animated progress with colors."""
    print("🚀 Testing colored animated progress:")

    # Create progress display
    progress = SyncProgressDisplay(total_entries=3)
    progress.print_header()

    # Test API loader with colors
    with AnimatedLoader("Fetching data from API") as loader:
        time.sleep(2)

    # Test different status methods
    progress.show_api_activity("Issue: Sample task for PROJ-123")
    progress.show_entry_success("Successfully synced PROJ-123")

    progress.show_api_activity("Issue: Another task for PROJ-124")
    progress.show_entry_skipped("PROJ-124", "already synced")

    progress.show_api_activity("Issue: Final task for PROJ-125")
    progress.show_entry_failed("Connection timeout")

    # Show final summary
    progress.print_summary()

if __name__ == "__main__":
    test_colors()
    test_animated_progress()
