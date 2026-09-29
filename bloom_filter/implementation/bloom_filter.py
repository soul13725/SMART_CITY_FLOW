import json
from .hash_functions import HashFunctions

class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float):
        from ..config.settings import Settings
        self.expected_items = expected_items
        self.target_false_positive_rate = false_positive_rate
        
        self.num_bits, self.num_hashes = Settings.calculate_bloom_parameters(
            expected_items, false_positive_rate
        )
        
        # Determine number of bytes needed
        self.num_bytes = (self.num_bits + 7) // 8
        self.bit_array = bytearray(self.num_bytes)

    def add(self, item: str):
        for i in range(self.num_hashes):
            position = HashFunctions.get_hash(item, i, self.num_bits)
            byte_index = position // 8
            bit_index = position % 8
            self.bit_array[byte_index] |= (1 << bit_index)

    def contains(self, item: str) -> bool:
        for i in range(self.num_hashes):
            position = HashFunctions.get_hash(item, i, self.num_bits)
            byte_index = position // 8
            bit_index = position % 8
            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False
        return True

    def __contains__(self, item: str) -> bool:
        return self.contains(item)
        
    def get_memory_stats(self):
        return {
            "bit_count": self.num_bits,
            "byte_count": self.num_bytes,
            "hash_count": self.num_hashes,
            "expected_items": self.expected_items,
            "target_false_positive_rate": self.target_false_positive_rate
        }

    def save(self, path: str):
        with open(path, 'wb') as f:
            # Save metadata as a short JSON string followed by a newline, then raw bytes
            metadata = json.dumps({
                "expected_items": self.expected_items,
                "false_positive_rate": self.target_false_positive_rate
            })
            f.write(metadata.encode('utf-8') + b'\n')
            f.write(self.bit_array)

    @classmethod
    def load(cls, path: str) -> 'BloomFilter':
        with open(path, 'rb') as f:
            metadata_line = f.readline().decode('utf-8').strip()
            metadata = json.loads(metadata_line)
            bf = cls(metadata['expected_items'], metadata['false_positive_rate'])
            bf.bit_array = bytearray(f.read())
            return bf
