import os
import sys
from io import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from hadoop.mapreduce.jobs import vehicle_count_mapper, vehicle_count_reducer
from hadoop.mapreduce.jobs import junction_traffic_mapper, junction_traffic_reducer

def test_vehicle_count_mapper(monkeypatch, capsys):
    test_input = "event_id,timestamp,sensor_id,junction_id,lane_id,vehicle_type,vehicle_count,average_speed,traffic_density,weather_condition,latitude,longitude,occupancy_rate,road_type,direction,incident_status\n"
    test_input += "evt_1,2026-09-27T08:42:15Z,S001,J001,L1,car,10,45.5,LOW,clear,28.6,77.2,0.5,arterial,N,normal\n"
    test_input += "evt_2,2026-09-27T08:42:16Z,S002,J002,L1,bus,20,30.0,MEDIUM,rain,28.6,77.2,0.6,arterial,N,normal\n"
    test_input += "evt_3,invalid\n" # Should be skipped safely
    
    monkeypatch.setattr('sys.stdin', StringIO(test_input))
    vehicle_count_mapper.main()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert "J001\t10" in lines
    assert "J002\t20" in lines

def test_vehicle_count_reducer(monkeypatch, capsys):
    test_input = "J001\t10\nJ001\t15\nJ002\t20\n"
    
    monkeypatch.setattr('sys.stdin', StringIO(test_input))
    vehicle_count_reducer.main()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert "J001\t25" in lines
    assert "J002\t20" in lines

def test_junction_traffic_mapper(monkeypatch, capsys):
    test_input = "event_id,timestamp,sensor_id,junction_id,lane_id,vehicle_type,vehicle_count,average_speed,traffic_density,weather_condition,latitude,longitude,occupancy_rate,road_type,direction,incident_status\n"
    test_input += "evt_1,2026-09-27T08:42:15Z,S001,J001,L1,car,10,40.0,LOW,clear,28.6,77.2,0.5,arterial,N,normal\n"
    
    monkeypatch.setattr('sys.stdin', StringIO(test_input))
    junction_traffic_mapper.main()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert "J001\t10,40.0,0.5,1" in lines

def test_junction_traffic_reducer(monkeypatch, capsys):
    test_input = "J001\t10,40.0,0.5,1\nJ001\t20,60.0,0.7,1\n"
    
    monkeypatch.setattr('sys.stdin', StringIO(test_input))
    junction_traffic_reducer.main()
    
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert "J001\ttotal_vehicle_count=30,average_speed=50.00,average_occupancy=0.60,event_count=2" in lines
