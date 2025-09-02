#!/usr/bin/env python3
"""
Demo script to showcase the new animated progress system.
"""

import time
from animated_progress import AnimatedLoader, SyncProgressDisplay, create_api_loader


def demo_loaders():
    """Demo the different types of loaders."""
    print("🎬 DEMO: Animated Loaders")
    print("=" * 40)

    # Demo different spinner types
    operations = [
        ("Fetching Toggl entries", 2),
        ("Validating JIRA issue", 1.5),
        ("Syncing to Tempo", 2.5)
    ]

    for operation, duration in operations:
        print(f"\n📡 {operation}...")
        with create_api_loader(operation) as loader:
            time.sleep(duration)
        print(f"✅ {operation} completed!")

    print("\n🎉 All operations completed!")


def demo_sync_progress():
    """Demo the sync progress display."""
    print("\n\n🎬 DEMO: Sync Progress Display")
    print("=" * 40)

    # Simulate a sync operation
    entries = [
        ("PROJ-123", "2 hours", "2025-08-25", "success"),
        ("PROJ-124", "30 minutes", "2025-08-25", "skip"),
        ("PROJ-125", "1.5 hours", "2025-08-25", "success"),
        ("PROJ-126", "45 minutes", "2025-08-25", "fail"),
        ("PROJ-127", "1 hour", "2025-08-25", "success"),
    ]

    progress = SyncProgressDisplay(len(entries))
    progress.print_header()

    for issue_key, duration, date, result in entries:
        progress.start_entry_processing(issue_key, duration, date)

        if result != "skip":
            # Simulate API calls with loaders
            with create_api_loader("Validating JIRA issue"):
                time.sleep(0.5)
            progress.show_api_activity(f"Issue: Sample task for {issue_key}")

            if result != "fail":
                with create_api_loader("Syncing to Tempo"):
                    time.sleep(0.8)

        time.sleep(0.3)  # Brief pause for visibility

        if result == "success":
            progress.show_entry_success()
        elif result == "skip":
            progress.show_entry_skipped(issue_key)
        elif result == "fail":
            progress.show_entry_failed("Network timeout")

    progress.print_summary()


def demo_error_scenarios():
    """Demo error handling scenarios."""
    print("\n\n🎬 DEMO: Error Scenarios")
    print("=" * 40)

    progress = SyncProgressDisplay(2)

    # Demo a failed API call
    progress.start_entry_processing("PROJ-ERROR", "1 hour", "2025-08-25")

    try:
        with create_api_loader("Attempting problematic API call"):
            time.sleep(1)
            raise Exception("Simulated API failure")
    except Exception as e:
        progress.show_entry_failed(str(e))

    # Demo a successful retry
    progress.start_entry_processing("PROJ-RETRY", "30 minutes", "2025-08-25")

    with create_api_loader("Retrying after error"):
        time.sleep(1)
    progress.show_entry_success("Retry successful!")


if __name__ == "__main__":
    print("🎭 TOGGL-TO-TEMPO ANIMATED PROGRESS DEMO")
    print("=" * 50)

    demo_loaders()
    demo_sync_progress()
    demo_error_scenarios()

    print("\n\n🏁 Demo completed! The sync command now has beautiful animated progress!")
