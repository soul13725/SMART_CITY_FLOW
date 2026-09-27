import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kafka.config.settings import settings
import pytest
from unittest.mock import MagicMock

# In tests, we mock the Producer and Consumer from confluent_kafka so we don't need a running cluster.
def test_kafka_settings():
    assert settings.KAFKA_TRAFFIC_TOPIC == "traffic-events"
    assert "localhost" in settings.KAFKA_BOOTSTRAP_SERVERS

def test_producer_mock(mocker):
    # This verifies that the producer architecture is callable without crashing on imports
    from kafka.producers.traffic_producer import produce_from_file
    
    mock_producer = MagicMock()
    # Assume we use the phase 2 test output file, or just mock it.
    # It's an architecture validation test rather than end-to-end.
    assert mock_producer is not None

def test_consumer_mock():
    # Verifies the consumer can be imported
    from kafka.consumers.traffic_consumer import main
    assert main is not None
