import os
import glob
import re

def test_query_files_exist():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    queries_dir = os.path.join(base_dir, "queries")
    
    expected_files = [
        "01_database.hql",
        "02_external_table.hql",
        "03_internal_table.hql",
        "04_vehicle_analytics.hql",
        "05_junction_analytics.hql",
        "06_sensor_analytics.hql",
        "07_density_analytics.hql",
        "08_weather_analytics.hql",
        "09_incident_analytics.hql",
        "10_time_analytics.hql",
        "11_summary_analytics.hql"
    ]
    
    for file in expected_files:
        assert os.path.exists(os.path.join(queries_dir, file)), f"Missing {file}"

def test_schema_correctness():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    schema_file = os.path.join(base_dir, "queries", "02_external_table.hql")
    
    with open(schema_file, 'r') as f:
        content = f.read()
        
    canonical_fields = [
        "event_id", "timestamp", "sensor_id", "junction_id",
        "lane_id", "vehicle_type", "vehicle_count", "average_speed",
        "traffic_density", "weather_condition", "latitude", "longitude",
        "occupancy_rate", "road_type", "direction", "incident_status"
    ]
    
    for field in canonical_fields:
        # Check if the field is present (backticks handled for timestamp)
        assert re.search(fr'\b{field}\b', content), f"Schema missing canonical field: {field}"

def test_analytics_dimensions():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    queries_dir = os.path.join(base_dir, "queries")
    
    def check_file_for_keyword(filename, keyword):
        with open(os.path.join(queries_dir, filename), 'r') as f:
            return keyword.lower() in f.read().lower()
            
    assert check_file_for_keyword("04_vehicle_analytics.hql", "vehicle_type")
    assert check_file_for_keyword("05_junction_analytics.hql", "junction_id")
    assert check_file_for_keyword("06_sensor_analytics.hql", "sensor_id")
    assert check_file_for_keyword("07_density_analytics.hql", "traffic_density")
    assert check_file_for_keyword("08_weather_analytics.hql", "weather_condition")
    assert check_file_for_keyword("09_incident_analytics.hql", "incident_status")
    assert check_file_for_keyword("10_time_analytics.hql", "hour")
    assert check_file_for_keyword("10_time_analytics.hql", "to_date")

def test_no_hardcoded_absolute_paths_in_hql():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    queries_dir = os.path.join(base_dir, "queries")
    for file in glob.glob(os.path.join(queries_dir, "*.hql")):
        with open(file, 'r') as f:
            content = f.read()
            # Windows drive paths like C:\ or E:\
            assert not re.search(r'[a-zA-Z]:\\', content), f"Hardcoded Windows path found in {file}"
