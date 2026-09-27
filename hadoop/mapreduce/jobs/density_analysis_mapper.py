#!/usr/bin/env python
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or row[0] == "event_id":
            continue
        try:
            density = row[8]
            v_count = int(row[6])
            avg_speed = float(row[7])
            print(f"{density}\t{v_count},{avg_speed},1")
        except (IndexError, ValueError):
            pass

if __name__ == "__main__":
    main()
