from .bloom_filter import BloomFilter
from ..config.settings import settings

class DuplicateDetector:
    def __init__(self, expected_items=None, false_positive_rate=None):
        if expected_items is None:
            expected_items = settings.BLOOM_EXPECTED_ITEMS
        if false_positive_rate is None:
            false_positive_rate = settings.BLOOM_FALSE_POSITIVE_RATE
            
        self.bloom_filter = BloomFilter(expected_items, false_positive_rate)
        
        self.total_checked = 0
        self.new_events = 0
        self.duplicates = 0

    def is_duplicate(self, event_id: str) -> bool:
        """
        Check if an event ID is already in the Bloom filter.
        """
        return event_id in self.bloom_filter

    def process(self, event_id: str) -> bool:
        """
        Process an event ID: check for duplication, and add if new.
        Returns True if DUPLICATE, False if NEW.
        """
        self.total_checked += 1
        if self.is_duplicate(event_id):
            self.duplicates += 1
            return True
        else:
            self.bloom_filter.add(event_id)
            self.new_events += 1
            return False

    def reset(self):
        """
        Reset the Bloom filter and statistics.
        """
        self.bloom_filter = BloomFilter(
            self.bloom_filter.expected_items,
            self.bloom_filter.target_false_positive_rate
        )
        self.total_checked = 0
        self.new_events = 0
        self.duplicates = 0

    def statistics(self):
        duplicate_rate = 0.0
        if self.total_checked > 0:
            duplicate_rate = self.duplicates / self.total_checked
            
        stats = {
            "total_checked": self.total_checked,
            "new_events": self.new_events,
            "duplicates": self.duplicates,
            "estimated_duplicate_rate": duplicate_rate
        }
        stats.update(self.bloom_filter.get_memory_stats())
        return stats
