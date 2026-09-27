#!/usr/bin/env python
import sys

def main():
    current_junction = None
    total_vehicles = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            junction, count_str = line.split('\t', 1)
            count = int(count_str)
        except ValueError:
            continue

        if current_junction == junction:
            total_vehicles += count
        else:
            if current_junction is not None:
                print(f"{current_junction}\t{total_vehicles}")
            current_junction = junction
            total_vehicles = count

    # Print the last junction
    if current_junction is not None:
        print(f"{current_junction}\t{total_vehicles}")

if __name__ == "__main__":
    main()
