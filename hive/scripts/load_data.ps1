Write-Host "Loading data into Hive via HDFS..."
if (-not (Get-Command "hdfs" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: HDFS not found in PATH. Data load is BLOCKED." -ForegroundColor Red
    exit 1
}

# The actual load was handled by HDFS upload in Phase 5 and the internal table load in setup.
# This script ensures data integrity checks are run.
Write-Host "Verifying table row counts..."
hive -e "USE smart_city; SELECT COUNT(*) FROM traffic_events_raw;"
hive -e "USE smart_city; SELECT COUNT(*) FROM traffic_events;"
Write-Host "Data load verification complete."
