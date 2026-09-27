Write-Host "Running MongoDB Data Import"
python -m mongodb.ingestion.import_traffic --input data/generated/traffic_events.csv
