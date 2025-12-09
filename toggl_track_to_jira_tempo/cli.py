import sys
import argparse
from sync import main as sync
from summary import main as get_summary
# Import the individual functions instead of the main function
from sync_records_cli import list_records, delete_record, clear_all, show_stats
from sync_tracker import SyncTracker
from cli_defaults import DEFAULT_SYNC_DB_PATH
# from freezegun import freeze_time


def setup_sync_records_subparser(subparsers):
    """Set up the sync-records subcommand and its subcommands."""
    sync_records_parser = subparsers.add_parser(
        "sync-records",
        help="Manage sync tracking records"
    )
    sync_records_parser.add_argument(
        "--db-path",
        default=DEFAULT_SYNC_DB_PATH,
        help=f"Path to sync records database (default: {DEFAULT_SYNC_DB_PATH})"
    )

    # Create subparsers for sync-records
    sync_records_subparsers = sync_records_parser.add_subparsers(
        dest="sync_records_command",
        help="Sync records management commands"
    )

    # List command
    list_parser = sync_records_subparsers.add_parser("list", help="List sync records")
    list_parser.add_argument("--start-date", help="Filter from date (YYYY-MM-DD)")
    list_parser.add_argument("--end-date", help="Filter to date (YYYY-MM-DD)")

    # Delete command
    delete_parser = sync_records_subparsers.add_parser("delete", help="Delete a sync record")
    delete_parser.add_argument("hash", help="Entry hash to delete")

    # Clear command
    clear_parser = sync_records_subparsers.add_parser("clear", help="Clear all sync records")
    clear_parser.add_argument("--confirm", action="store_true",
                            help="Confirm deletion of all records")

    # Stats command
    stats_parser = sync_records_subparsers.add_parser("stats", help="Show sync statistics")


def handle_sync_records_command(args):
    """Handle sync-records commands."""
    if not args.sync_records_command:
        print("Error: sync-records requires a subcommand")
        print("Available subcommands: list, delete, clear, stats")
        print("Use 'python cli.py sync-records --help' for more information")
        return 1

    # Create a mock args object that matches what the sync_records_cli functions expect
    class MockArgs:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    try:
        if args.sync_records_command == "list":
            mock_args = MockArgs(
                db_path=args.db_path,
                start_date=getattr(args, 'start_date', None),
                end_date=getattr(args, 'end_date', None)
            )
            list_records(mock_args)

        elif args.sync_records_command == "delete":
            mock_args = MockArgs(
                db_path=args.db_path,
                hash=args.hash
            )
            delete_record(mock_args)

        elif args.sync_records_command == "clear":
            mock_args = MockArgs(
                db_path=args.db_path,
                confirm=getattr(args, 'confirm', False)
            )
            clear_all(mock_args)

        elif args.sync_records_command == "stats":
            mock_args = MockArgs(db_path=args.db_path)
            show_stats(mock_args)

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


# @freeze_time("2025-03-31")
def main():
    # Create the main argument parser
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="Toggl to Tempo sync tool"
    )

    # Create subparsers for the main commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync Toggl entries to Tempo")
    sync_parser.add_argument("start_date", nargs="?", help="Start date (YYYY-MM-DD)")
    sync_parser.add_argument("end_date", nargs="?", help="End date (YYYY-MM-DD)")

    # Get-summary command
    summary_parser = subparsers.add_parser("get-summary", help="Generate time tracking summary")
    summary_parser.add_argument("args", nargs="*", help="Summary arguments")

    # Sync-records command (with its own subcommands)
    setup_sync_records_subparser(subparsers)

    # Parse arguments
    args = parser.parse_args()

    # Handle commands
    if not args.command:
        parser.print_help()
        return 1

    if args.command == "sync":
        # Convert to the format expected by the sync function
        sync_args = []
        if args.start_date:
            sync_args.append(args.start_date)
        if args.end_date:
            sync_args.append(args.end_date)
        sync(*sync_args)

    elif args.command == "get-summary":
        get_summary(*args.args)

    elif args.command == "sync-records":
        return handle_sync_records_command(args)

    return 0


if __name__ == '__main__':
    sys.exit(main())
