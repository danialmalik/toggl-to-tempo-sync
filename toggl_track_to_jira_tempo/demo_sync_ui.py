#!/usr/bin/env python3
"""
Demo script to showcase the new animated progress system.
Run this to see the beautiful new sync UI in action!
"""

import time
from animated_progress import AnimatedLoader, SyncProgressDisplay
from animated_progress import create_api_loader


def demo_quick():
    """Quick demo of the new sync interface."""
    print("🎬 TOGGL-TO-TEMPO SYNC UI DEMO")
    print("=" * 50)

    # Demo a typical sync operation
    entries = [
        ("PROJ-123", "2 hours", "2025-08-25", "success"),
        ("PROJ-124", "30 minutes", "2025-08-25", "skip"),
        ("PROJ-125", "1.5 hours", "2025-08-25", "success"),
    ]

    progress = SyncProgressDisplay(len(entries))
    progress.print_header()

    for issue_key, duration, date, result in entries:
        progress.start_entry_processing(issue_key, duration, date)

        if result != "skip":
            with create_api_loader("Validating JIRA issue"):
                time.sleep(0.5)
            progress.show_api_activity(f"Issue: Sample task for {issue_key}")

            with create_api_loader("Syncing to Tempo"):
                time.sleep(0.5)

        if result == "success":
            progress.show_entry_success()
        elif result == "skip":
            progress.show_entry_skipped(issue_key)

    progress.print_summary()

    print("\n🎉 This is how your sync operations will look now!")
    print("✨ Features:")
    print("   • Animated spinners during API calls")
    print("   • Clear progress tracking [current/total]")
    print("   • Emoji status indicators")
    print("   • Rich summary with success rates")
    print("   • Real-time updates")


if __name__ == "__main__":
    demo_quick()
