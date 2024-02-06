#!/usr/bin/python3
"""Reads from standard input and computes metrics.

After every ten lines or the input of a keyboard interruption (CTRL + C),
prints the following statistics:
    - Total file size up to that point.
    - Count of read status codes up to that point.
"""

def print_stats(size, status_codes):
    """Print accumulated metrics.

    Args:
        size (int): The accumulated read file size.
        status_codes (dict): The accumulated count of status codes.
    """
    print("File size: {}".format(size))
    for key in sorted(status_codes):
        print("{}: {}".format(key, status_codes[key]))

if __name__ == "__main__":
    import sys

    size = 0
    status_codes = {}
    valid_codes = {'200', '301', '400', '401', '403', '404', '405', '500'}  # Use a set for faster membership checks
    count = 0

    try:
        for line in sys.stdin:
            line = line.split()

            if len(line) >= 2:  # Ensure sufficient elements for size and status code
                try:
                    size += int(line[-1])
                except ValueError:
                    print(f"Warning: Invalid size value in line: {line}")

                if line[-2] in valid_codes:
                    status_codes[line[-2]] = status_codes.get(line[-2], 0) + 1
                else:
                    print(f"Warning: Invalid status code in line: {line}")

            count += 1

            if count == 10:
                print_stats(size, status_codes)
                count = 0

    except KeyboardInterrupt:
        print_stats(size, status_codes)
        raise

    print_stats(size, status_codes)  # Print final stats
