import os
import glob

def test_pig_scripts_exist():
    """Verify all 11 scripts exist."""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    scripts = glob.glob(os.path.join(scripts_dir, '*.pig'))
    assert len(scripts) == 11, f"Expected 11 scripts, found {len(scripts)}"

def test_schema_usage():
    """Verify required canonical fields appear where appropriate."""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    with open(os.path.join(scripts_dir, '01_load_traffic.pig'), 'r') as f:
        content = f.read()
        assert 'event_id:chararray' in content
        assert 'timestamp:chararray' in content
        assert 'sensor_id:chararray' in content
        assert 'vehicle_count:int' in content
        assert 'average_speed:double' in content

def test_required_pig_operations():
    """Verify use of Pig operations across scripts."""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    
    all_content = ""
    for script in glob.glob(os.path.join(scripts_dir, '*.pig')):
        with open(script, 'r') as f:
            all_content += f.read()
            
    assert 'LOAD ' in all_content
    assert 'FILTER ' in all_content
    assert 'FOREACH ' in all_content
    assert 'GENERATE ' in all_content
    assert 'GROUP ' in all_content
    assert 'COUNT(' in all_content
    assert 'SUM(' in all_content
    assert 'AVG(' in all_content
    assert 'ORDER ' in all_content
    assert 'STORE ' in all_content

def test_input_output_paths():
    """Verify that scripts use configured HDFS paths."""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    
    for script in glob.glob(os.path.join(scripts_dir, '*.pig')):
        with open(script, 'r') as f:
            content = f.read()
            assert '/smartcity/traffic/raw/traffic_events.csv' in content, f"Source path missing in {script}"
            assert '/smartcity/traffic/pig_output' in content, f"Output path missing in {script}"

def test_no_future_phase_contamination():
    """Check that Pig scripts do not import or depend on future phases."""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    
    for script in glob.glob(os.path.join(scripts_dir, '*.pig')):
        with open(script, 'r') as f:
            content = f.read()
            assert 'FastAPI' not in content
            assert 'React' not in content
            assert 'Bloom Filter' not in content
            assert 'R Analytics' not in content
            assert 'MongoDB' not in content
            assert 'Kafka' not in content

if __name__ == '__main__':
    print("Run with pytest.")
