import time
import os
import csv
from bloom_filter.implementation.duplicate_detector import DuplicateDetector

def benchmark(dataset_path: str, size_limit: int):
    if not os.path.exists(dataset_path):
        print(f"Dataset {dataset_path} not found. Skipping benchmark for limit {size_limit}.")
        return

    # Assuming false positive rate of 0.01
    detector = DuplicateDetector(expected_items=size_limit, false_positive_rate=0.01)

    print(f"\n--- Benchmarking {size_limit} events ---")
    
    start_time = time.time()
    count = 0
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if count >= size_limit:
                break
            event_id = row.get('event_id')
            if event_id:
                detector.process(event_id)
                count += 1
                
    end_time = time.time()
    
    stats = detector.statistics()
    
    processing_time = end_time - start_time
    items_per_sec = count / processing_time if processing_time > 0 else 0
    
    print(f"Items processed: {count}")
    print(f"New items: {stats['new_events']}")
    print(f"Duplicates: {stats['duplicates']}")
    print(f"Processing time: {processing_time:.4f} seconds")
    print(f"Items/second: {items_per_sec:.2f}")
    print(f"Memory size (bytes): {stats['byte_count']}")
    print(f"Hash count: {stats['hash_count']}")
    print(f"False-positive target: {stats['target_false_positive_rate']}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    dataset = os.path.join(base_dir, 'data', 'generated', 'traffic_events.csv')
    dataset_large = os.path.join(base_dir, 'data', 'generated', 'traffic_events_large.csv')
    
    benchmark(dataset, 1000)
    
    if os.path.exists(dataset_large):
        benchmark(dataset_large, 10000)
        benchmark(dataset_large, 100000)
    else:
        # Fallback to whatever is available
        benchmark(dataset, 10000)
        benchmark(dataset, 100000)
