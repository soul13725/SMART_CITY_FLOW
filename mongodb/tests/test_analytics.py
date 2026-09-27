import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from mongodb.analytics.junction_analytics import run_junction_analytics
from mongodb.analytics.incident_analytics import run_incident_analytics

class MockCollection:
    def __init__(self, data):
        self.data = data
        self.pipeline_received = None
        
    def count_documents(self, filter_query):
        return len(self.data)
        
    def aggregate(self, pipeline):
        self.pipeline_received = pipeline
        # Return mock cursor/list
        return [{"_id": "MOCK", "result": "ok"}]

def test_junction_analytics_pipeline():
    mock_coll = MockCollection([])
    res = run_junction_analytics(mock_coll)
    pipeline = mock_coll.pipeline_received
    
    assert len(pipeline) == 2
    assert "$group" in pipeline[0]
    assert pipeline[0]["$group"]["_id"] == "$junction_id"
    assert "$sort" in pipeline[1]

def test_incident_analytics_pipeline():
    mock_coll = MockCollection([])
    res = run_incident_analytics(mock_coll)
    pipeline = mock_coll.pipeline_received
    
    assert len(pipeline) == 2
    assert "$group" in pipeline[0]
    assert pipeline[0]["$group"]["_id"] == "$incident_status"
    assert "$project" in pipeline[1]
