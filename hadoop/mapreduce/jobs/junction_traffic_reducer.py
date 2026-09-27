#!/usr/bin/env python
import sys

def main():
    current_junction = None
    total_v = 0
    total_speed = 0.0
    total_occ = 0.0
    total_events = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            junction, vals = line.split('\t', 1)
            v_count, avg_speed, occ_rate, e_count = vals.split(',')
            v_count = int(v_count)
            avg_speed = float(avg_speed)
            occ_rate = float(occ_rate)
            e_count = int(e_count)
        except ValueError:
            continue

        if current_junction == junction:
            total_v += v_count
            total_speed += avg_speed
            total_occ += occ_rate
            total_events += e_count
        else:
            if current_junction is not None:
                print(f"{current_junction}\ttotal_vehicle_count={total_v},average_speed={total_speed/total_events:.2f},average_occupancy={total_occ/total_events:.2f},event_count={total_events}")
            current_junction = junction
            total_v = v_count
            total_speed = avg_speed
            total_occ = occ_rate
            total_events = e_count

    if current_junction is not None:
        print(f"{current_junction}\ttotal_vehicle_count={total_v},average_speed={total_speed/total_events:.2f},average_occupancy={total_occ/total_events:.2f},event_count={total_events}")

if __name__ == "__main__":
    main()
