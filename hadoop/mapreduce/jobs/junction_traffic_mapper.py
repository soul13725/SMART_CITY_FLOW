#!/usr/bin/env python
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or row[0] == "event_id":
            continue
        try:
            junction_id = row[3]
            v_count = int(row[6])
            avg_speed = float(row[7])
            occ_rate = float(row[12]) if row[12] else 0.0
            print(f"{junction_id}\t{v_count},{avg_speed},{occ_rate},1")
        except (IndexError, ValueError):
            pass

if __name__ == "__main__":
    main()
