Write-Host "Running Hive Analytics Queries..."
if (-not (Get-Command "hive" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Hive CLI not found in PATH. Query execution is BLOCKED." -ForegroundColor Red
    exit 1
}

$queries = @(
    "04_vehicle_analytics.hql",
    "05_junction_analytics.hql",
    "06_sensor_analytics.hql",
    "07_density_analytics.hql",
    "08_weather_analytics.hql",
    "09_incident_analytics.hql",
    "10_time_analytics.hql",
    "11_summary_analytics.hql"
)

foreach ($query in $queries) {
    Write-Host "Executing $query..."
    hive -f "..\queries\$query"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Query $query failed." -ForegroundColor Red
    }
}
Write-Host "All queries executed." -ForegroundColor Green
