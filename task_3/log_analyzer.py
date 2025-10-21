import sys
from collections import defaultdict
import argparse

LOG_LEVELS = ["INFO", "ERROR", "DEBUG", "WARNING"]

def parse_log_line(line: str) -> dict | None:
    """
    Parses a log line and returns a dictionary with its components.
    Expected format: "Date Time LEVEL Message..."
    """
    try:
        parts = line.strip().split(' ', 3)

        if len(parts) < 4:
            print(f"Incorrect format of line: {line.strip()}", file=sys.stderr)
            return None

        date, time, level, message = parts[0], parts[1], parts[2].upper(), parts[3]

        if level not in LOG_LEVELS:
            print(f"Unknown log level '{level}' in line: '{line.strip()}'", file=sys.stderr)
            return None

        return {
            'date': date,
            'time': time,
            'level': level,
            'message': message.strip()
        }
    except Exception as e:
        print(f"Error parsing line: {line.strip()}. Error: {e}", file=sys.stderr)
        return None


def load_logs(file_path: str) -> list[dict]:
    """
    Loads logs from a file at the specified path, applying parse_log_line to each line.
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parsed_log = parse_log_line(line)
                if parsed_log:
                    logs.append(parsed_log)
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error occurred while reading the file: {e}", file=sys.stderr)
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:
    """
    Filters the list of logs by the specified log level.
    """
    target_level = level.upper()

    return list(filter(lambda log: log['level'] == target_level, logs))


def count_logs_by_level(logs: list[dict]) -> dict[str, int]:
    """
    Counts the number of log entries for each log level.
    """
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return dict(counts)


def display_log_counts(counts: dict[str, int]) -> None:
    """
    Formats and displays the log count results in a table.
    """
    header_level = "Рівень логування"
    header_count = "Кількість"

    # Determine the maximum width for formatting the level column
    max_level_len = max([len(header_level)] + [len(level) for level in counts.keys()])

    print(f"{header_level:<{max_level_len}} | {header_count}")
    print("-" * (max_level_len) + "-|" + "-" * len(header_count))

    for level in sorted(counts.keys(), key=lambda x: LOG_LEVELS.index(x) if x in LOG_LEVELS else float('inf')):
        count = counts[level]
        print(f"{level:<{max_level_len}} | {count}")


def display_filtered_logs(filtered_logs: list[dict], level: str) -> None:
    """
    Prints detailed log entries for a specific level.
    """
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    if filtered_logs:
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")
    else:
        print("Записів цього рівня не знайдено.")

def main():
    """
    Main function to run the script. Handles command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Log Analyzer Script")

    parser.add_argument("log_file_path",
                        help="Path to the log file to be analyzed.")

    parser.add_argument("log_level",
                        nargs='?',
                        default=None,
                        type=str,
                        help="(Optional) Log level to filter detailed logs (INFO, ERROR, DEBUG, WARNING).")

    args = parser.parse_args()

    all_logs = load_logs(args.log_file_path)

    if not all_logs:
        print("No valid logs loaded from the file. Exit.")
        return

    log_counts = count_logs_by_level(all_logs)

    display_log_counts(log_counts)

    if args.log_level:
        target_level = args.log_level.upper()

        if target_level in LOG_LEVELS:
            filtered = filter_logs_by_level(all_logs, target_level)
            display_filtered_logs(filtered, target_level)
        else:
            print(f"Warning: Specified unknown log level '{args.log_level}'. Valid levels are: {', '.join(LOG_LEVELS)}")


if __name__ == "__main__":
    main()
