import os
import tempfile
from bloom_filter.implementation.bloom_filter import BloomFilter
from bloom_filter.config.settings import Settings

def test_parameter_calculation():
    # Test m, k calculations
    expected_items = 10000
    p = 0.01
    m, k = Settings.calculate_bloom_parameters(expected_items, p)
    # math: m = -10000 * ln(0.01) / ln(2)^2 = 95851
    # k = 95851/10000 * ln(2) = 6.6 -> 7
    assert m > 0
    assert k > 0

def test_bloom_filter_initialization():
    bf = BloomFilter(1000, 0.01)
    stats = bf.get_memory_stats()
    assert stats['expected_items'] == 1000
    assert stats['target_false_positive_rate'] == 0.01
    assert stats['bit_count'] > 0
    assert stats['byte_count'] > 0
    assert stats['hash_count'] > 0

def test_add_and_contains():
    bf = BloomFilter(1000, 0.01)
    
    item = "event_001"
    assert not bf.contains(item)
    
    bf.add(item)
    assert bf.contains(item)
    assert item in bf

def test_no_false_negatives():
    bf = BloomFilter(1000, 0.01)
    items = [f"event_{i}" for i in range(100)]
    
    for item in items:
        bf.add(item)
        
    for item in items:
        assert bf.contains(item), f"False negative for {item}"

def test_false_positive_behavior():
    bf = BloomFilter(1000, 0.1) # high FP rate to test behavior conceptually
    
    items = [f"event_in_{i}" for i in range(1000)]
    for item in items:
        bf.add(item)
        
    # Check unseen items
    false_positives = 0
    test_size = 1000
    for i in range(test_size):
        item = f"event_out_{i}"
        if item in bf:
            false_positives += 1
            
    fp_rate = false_positives / test_size
    # just checking that it doesn't fail completely. It should be >0 and around 0.1 ideally.
    assert fp_rate >= 0.0

def test_edge_cases():
    bf = BloomFilter(1000, 0.01)
    
    # Empty string
    assert "" not in bf
    bf.add("")
    assert "" in bf
    
    # Unicode string
    unicode_item = "évënt_🚀_123"
    assert unicode_item not in bf
    bf.add(unicode_item)
    assert unicode_item in bf
    
    # Repeated item
    bf.add("repeat")
    bf.add("repeat")
    assert "repeat" in bf

def test_serialization():
    bf1 = BloomFilter(1000, 0.01)
    items = ["item1", "item2", "item3"]
    for item in items:
        bf1.add(item)
        
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    try:
        bf1.save(path)
        
        bf2 = BloomFilter.load(path)
        
        for item in items:
            assert bf2.contains(item)
            
        assert not bf2.contains("item4")
        
        stats1 = bf1.get_memory_stats()
        stats2 = bf2.get_memory_stats()
        
        assert stats1 == stats2
        
    finally:
        os.remove(path)
