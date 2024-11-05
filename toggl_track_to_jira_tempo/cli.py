import sys
from sync import main as sync
from summary import main as get_summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [<args>]")
        print("Commands:")
        print("  sync")
        print("  get-summary")
        return 1
    command = sys.argv[1]
    command_args = sys.argv[2:]

    if command == "sync":
        sync(*command_args)

    elif command == "get-summary":
        get_summary(*command_args)

    else:
        print("Invalid command")
        return 1


if __name__ == '__main__':
    sys.exit(main())
