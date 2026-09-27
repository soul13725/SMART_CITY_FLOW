#!/usr/bin/env python
import sys

def main():
    current_density = None
    total_v = 0
    total_speed = 0.0
    total_events = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            density, vals = line.split('\t', 1)
            v_count, avg_speed, e_count = vals.split(',')
            v_count = int(v_count)
            avg_speed = float(avg_speed)
            e_count = int(e_count)
        except ValueError:
            continue

        if current_density == density:
            total_v += v_count
            total_speed += avg_speed
            total_events += e_count
        else:
            if current_density is not None:
                print(f"{current_density}\ttotal_vehicle_count={total_v},event_count={total_events},average_speed={total_speed/total_events:.2f}")
            current_density = density
            total_v = v_count
            total_speed = avg_speed
            total_events = e_count

    if current_density is not None:
        print(f"{current_density}\ttotal_vehicle_count={total_v},event_count={total_events},average_speed={total_speed/total_events:.2f}")

if __name__ == "__main__":
    main()
