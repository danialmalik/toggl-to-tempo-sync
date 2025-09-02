import time
import threading
import sys
from typing import Optional
from utils import Logger


class AnimatedLoader:
    """
    A simple animated loader for terminal operations.
    """

    def __init__(self, message: str = "Loading", spinner_chars: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
        self.message = message
        self.spinner_chars = spinner_chars
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.spinner_index = 0

    def _spin(self):
        """Internal method to handle the spinning animation."""
        while self.running:
            char = self.spinner_chars[self.spinner_index % len(self.spinner_chars)]
            sys.stdout.write(f'\r{char} {self.message}...')
            sys.stdout.flush()
            self.spinner_index += 1
            time.sleep(0.1)

    def start(self):
        """Start the animated loader."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._spin, daemon=True)
            self.thread.start()

    def stop(self, success_message: Optional[str] = None, clear_line: bool = True):
        """Stop the animated loader."""
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()

            if clear_line:
                # Clear the current line
                sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
                sys.stdout.flush()

            if success_message:
                Logger.log_success(success_message)

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


class SyncProgressDisplay:
    """
    Enhanced progress display for sync operations with colors.
    """

    def __init__(self, total_entries: int):
        self.total_entries = total_entries
        self.current_entry = 0
        self.synced_count = 0
        self.skipped_count = 0
        self.failed_count = 0

        # Unicode symbols with colors
        self.symbols = {
            'success': '✅',
            'skip': '⏭️',
            'fail': '❌',
            'processing': '🔄',
            'info': 'ℹ️',
        }

    def print_header(self):
        """Print the sync operation header with colors."""
        border = "=" * 60

        Logger.log_info(f"\n")
        Logger.log_info("🚀 STARTING TOGGL TO TEMPO SYNC")
        Logger.log_info(f"{border}")

        total_text = f"📊 Total entries to process: {str(self.total_entries)}"
        Logger.log_info(total_text)

        Logger.log_info(f"{'-' * 60}")

    def start_entry_processing(self, issue_key: str, duration_str: str, date_str: str):
        """Show that we're starting to process an entry with colors."""
        self.current_entry += 1
        entry_num = f"[{self.current_entry}/{self.total_entries}]"

        # Color the components
        entry_num_colored = Logger.format_message(entry_num, Logger.INFO_SECONDARY)
        issue_key_colored = Logger.format_message(issue_key, Logger.INFO)
        duration_colored = Logger.format_message(f"({duration_str})", Logger.SUCCESS)
        date_colored = Logger.format_message(date_str, Logger.INFO_SECONDARY)

        Logger.log_info_raw(f"\n{self.symbols['processing']} {entry_num_colored} Processing: {issue_key_colored} {duration_colored} on {date_colored}")

    def show_entry_skipped(self, issue_key: str, reason: str = "already synced"):
        """Show that an entry was skipped with colors."""
        self.skipped_count += 1
        reason_colored = Logger.format_message(reason, Logger.WARNING)
        Logger.log_info_raw(f"   {self.symbols['skip']} SKIPPED: {reason_colored}")

    def show_entry_success(self, message: str = "Successfully synced"):
        """Show that an entry was successfully synced with colors."""
        self.synced_count += 1
        message_colored = Logger.format_message(message, Logger.SUCCESS)
        Logger.log_info_raw(f"   {self.symbols['success']} {message_colored}")

    def show_entry_failed(self, error: str):
        """Show that an entry failed to sync with colors."""
        self.failed_count += 1
        error_colored = Logger.format_message(f"FAILED: {error}", Logger.ERROR)
        Logger.log_info_raw(f"   {self.symbols['fail']} {error_colored}")

    def show_entry_user_skipped(self, reason: str = "user choice"):
        """Show that an entry was skipped by user choice with colors."""
        reason_colored = Logger.format_message(reason, Logger.WARNING)
        Logger.log_info_raw(f"   {self.symbols['skip']} SKIPPED: {reason_colored}")

    def show_api_activity(self, activity: str):
        """Show API activity with colors."""
        activity_colored = Logger.format_message(activity, Logger.INFO_SECONDARY)
        Logger.log_info_raw(f"   {self.symbols['info']} {activity_colored}")

    def print_summary(self):
        """Print the final sync summary with colors."""
        border = "=" * 60

        Logger.log_info_raw(f"\n{Logger.format_message(border, Logger.INFO)}")
        Logger.log_info_raw(f"{Logger.format_message('📋 SYNC SUMMARY', Logger.INFO)}")
        Logger.log_info_raw(f"{Logger.format_message(border, Logger.INFO)}")

        # Summary with colored numbers and emojis
        synced_text = f"{self.symbols['success']} Successfully synced: {Logger.format_message(str(self.synced_count), Logger.SUCCESS)} entries"
        skipped_text = f"{self.symbols['skip']} Skipped (already synced): {Logger.format_message(str(self.skipped_count), Logger.WARNING)} entries"

        Logger.log_info_raw(synced_text)
        Logger.log_info_raw(skipped_text)

        if self.failed_count > 0:
            failed_text = f"{self.symbols['fail']} Failed: {Logger.format_message(str(self.failed_count), Logger.ERROR)} entries"
            Logger.log_info_raw(failed_text)

        total_processed = self.synced_count + self.skipped_count + self.failed_count
        total_text = f"📊 Total processed: {Logger.format_message(f'{total_processed}/{self.total_entries}', Logger.INFO)} entries"
        Logger.log_info_raw(total_text)

        # Success rate with colors
        if total_processed > 0:
            success_rate = ((self.synced_count + self.skipped_count) / total_processed) * 100
            rate_color = Logger.SUCCESS if success_rate >= 90 else Logger.WARNING if success_rate >= 70 else Logger.ERROR
            rate_text = f"📈 Success rate: {Logger.format_message(f'{success_rate:.1f}%', rate_color)}"
            Logger.log_info_raw(rate_text)

        Logger.log_info_raw(f"{Logger.format_message(border, Logger.INFO)}")

                # Final status message with colors
        if self.failed_count == 0:
            Logger.log_info_raw(f"{Logger.format_message('🎉 All entries processed successfully!', Logger.SUCCESS)}")
        else:
            Logger.log_info_raw(f"{Logger.format_message('⚠️  Some entries failed to sync. Check the logs above for details.', Logger.WARNING)}")


def create_api_loader(operation: str) -> AnimatedLoader:
    """Create a loader for API operations."""
    spinners = {
        'fetching': "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        'syncing': "🔄⚡🔄⚡",
        'validating': "🔍🔎🔍🔎",
        'default': "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    }

    spinner_char = spinners.get(operation.lower(), spinners['default'])
    return AnimatedLoader(message=operation, spinner_chars=spinner_char)
