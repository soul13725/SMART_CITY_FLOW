Write-Host "Exporting Hive Analytics Results..."
if (-not (Get-Command "hive" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Hive CLI not found in PATH. Export is BLOCKED." -ForegroundColor Red
    exit 1
}

$outputDir = "..\output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
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
    $outName = $query.Replace(".hql", ".csv")
    Write-Host "Exporting $query to $outName..."
    hive -S -f "..\queries\$query" > "$outputDir\$outName"
}
Write-Host "Export complete." -ForegroundColor Green
