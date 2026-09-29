from bloom_filter.implementation.duplicate_detector import DuplicateDetector

def test_duplicate_detector_basic():
    detector = DuplicateDetector(1000, 0.01)
    
    # First time: new
    is_dup = detector.process("event_001")
    assert is_dup is False
    
    # Second time: duplicate
    is_dup2 = detector.process("event_001")
    assert is_dup2 is True
    
    # Another new item
    is_dup3 = detector.process("event_002")
    assert is_dup3 is False

def test_duplicate_detector_sequence():
    detector = DuplicateDetector(1000, 0.01)
    
    sequence = ["e1", "e2", "e3", "e1", "e4", "e2"]
    results = [detector.process(item) for item in sequence]
    
    # Expected: False, False, False, True, False, True
    assert results == [False, False, False, True, False, True]
    
    stats = detector.statistics()
    assert stats['total_checked'] == 6
    assert stats['new_events'] == 4
    assert stats['duplicates'] == 2
    assert stats['estimated_duplicate_rate'] == 2 / 6

def test_duplicate_detector_reset():
    detector = DuplicateDetector(1000, 0.01)
    
    detector.process("event_1")
    detector.process("event_1")
    
    stats = detector.statistics()
    assert stats['total_checked'] == 2
    assert stats['duplicates'] == 1
    
    detector.reset()
    
    stats2 = detector.statistics()
    assert stats2['total_checked'] == 0
    assert stats2['duplicates'] == 0
    
    # Should be new again
    assert detector.process("event_1") is False
