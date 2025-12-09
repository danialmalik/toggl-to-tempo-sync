#!/usr/bin/env python3
"""
Sync Records Management CLI

This script provides utilities to manage sync records, useful for debugging
and manually handling sync tracking.
"""

import argparse
import sys
from datetime import datetime
from sync_tracker import SyncTracker
from cli_defaults import DEFAULT_SYNC_DB_PATH
from utils import Logger


def list_records(args):
    """List all sync records, optionally filtered by date range."""
    tracker = SyncTracker(args.db_path)

    records = tracker.list_synced_entries(
        start_date=args.start_date,
        end_date=args.end_date
    )

    if not records:
        Logger.log_info("No sync records found.")
        return

    Logger.log_info(f"Found {len(records)} sync records:")
    Logger.log_info("=" * 80)

    for record in records:
        toggl_ids_str = ", ".join(map(str, record['toggl_ids']))
        duration_mins = record['duration'] // 60

        Logger.log_info(f"Hash: {record['entry_hash'][:12]}...")
        Logger.log_info(f"Issue: {record['issue_key']}")
        Logger.log_info(f"Date: {record['start_date']}")
        Logger.log_info(f"Duration: {duration_mins} minutes ({record['duration']} seconds)")
        Logger.log_info(f"Description: {record['description']}")
        Logger.log_info(f"Toggl IDs: [{toggl_ids_str}]")
        Logger.log_info(f"Synced: {record['sync_timestamp']}")
        if record['tempo_worklog_id']:
            Logger.log_info(f"Tempo Worklog ID: {record['tempo_worklog_id']}")
        Logger.log_info("-" * 40)


def delete_record(args):
    """Delete a specific sync record."""
    tracker = SyncTracker(args.db_path)

    if tracker.delete_sync_record(args.hash):
        Logger.log_success(f"Successfully deleted sync record: {args.hash}")
    else:
        Logger.log_error(f"Sync record not found: {args.hash}")


def clear_all(args):
    """Clear all sync records."""
    tracker = SyncTracker(args.db_path)

    if not args.confirm:
        Logger.log_warning("This will delete ALL sync records. Use --confirm to proceed.")
        return

    count = tracker.clear_all_records()
    Logger.log_success(f"Cleared {count} sync records.")


def show_stats(args):
    """Show statistics about sync records."""
    tracker = SyncTracker(args.db_path)

    records = tracker.list_synced_entries()

    if not records:
        Logger.log_info("No sync records found.")
        return

    # Calculate statistics
    total_records = len(records)
    total_duration = sum(record['duration'] for record in records)
    total_hours = total_duration / 3600

    # Group by date
    dates = {}
    for record in records:
        date = record['start_date']
        if date not in dates:
            dates[date] = {'count': 0, 'duration': 0}
        dates[date]['count'] += 1
        dates[date]['duration'] += record['duration']

    # Group by issue
    issues = {}
    for record in records:
        issue = record['issue_key']
        if issue not in issues:
            issues[issue] = {'count': 0, 'duration': 0}
        issues[issue]['count'] += 1
        issues[issue]['duration'] += record['duration']

    Logger.log_info("SYNC RECORDS STATISTICS")
    Logger.log_info("=" * 50)
    Logger.log_info(f"Total Records: {total_records}")
    Logger.log_info(f"Total Duration: {total_hours:.2f} hours ({total_duration} seconds)")
    Logger.log_info(f"Date Range: {min(dates.keys())} to {max(dates.keys())}")
    Logger.log_info(f"Unique Dates: {len(dates)}")
    Logger.log_info(f"Unique Issues: {len(issues)}")

    Logger.log_info("\nTop Issues by Duration:")
    Logger.log_info("-" * 30)
    sorted_issues = sorted(issues.items(), key=lambda x: x[1]['duration'], reverse=True)
    for issue, data in sorted_issues[:10]:
        hours = data['duration'] / 3600
        Logger.log_info(f"{issue}: {hours:.2f}h ({data['count']} entries)")


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(description="Manage Toggl-to-Tempo sync records")
    parser.add_argument("--db-path", default=DEFAULT_SYNC_DB_PATH,
                       help=f"Path to sync records database (default: {DEFAULT_SYNC_DB_PATH})")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List sync records")
    list_parser.add_argument("--start-date", help="Filter from date (YYYY-MM-DD)")
    list_parser.add_argument("--end-date", help="Filter to date (YYYY-MM-DD)")
    list_parser.set_defaults(func=list_records)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a sync record")
    delete_parser.add_argument("hash", help="Entry hash to delete")
    delete_parser.set_defaults(func=delete_record)

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear all sync records")
    clear_parser.add_argument("--confirm", action="store_true",
                            help="Confirm deletion of all records")
    clear_parser.set_defaults(func=clear_all)

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show sync statistics")
    stats_parser.set_defaults(func=show_stats)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        Logger.log_error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
