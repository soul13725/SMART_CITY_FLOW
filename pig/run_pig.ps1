# run_pig.ps1
# Script to execute Pig analytics

$ErrorActionPreference = "Stop"

Write-Host "Checking Pig Environment..."

$pigExe = Get-Command pig -ErrorAction SilentlyContinue

if (-not $pigExe) {
    Write-Host "IMPLEMENTED - PIG RUNTIME BLOCKED (Pig not found in PATH)" -ForegroundColor Yellow
    exit 1
}

Write-Host "Pig is available at: $($pigExe.Source)" -ForegroundColor Green

# Check Hadoop if required
$hadoopExe = Get-Command hadoop -ErrorAction SilentlyContinue
if (-not $hadoopExe) {
    Write-Host "Warning: Hadoop not found in PATH. Pig may only run in local mode." -ForegroundColor Yellow
}

$scripts = @(
    "01_load_traffic.pig",
    "02_filter_traffic.pig",
    "03_vehicle_analytics.pig",
    "04_junction_analytics.pig",
    "05_sensor_analytics.pig",
    "06_density_analytics.pig",
    "07_weather_analytics.pig",
    "08_incident_analytics.pig",
    "09_time_analytics.pig",
    "10_sort_analytics.pig",
    "11_summary_analytics.pig"
)

$scriptDir = Join-Path $PSScriptRoot "scripts"

foreach ($script in $scripts) {
    $scriptPath = Join-Path $scriptDir $script
    Write-Host "Executing $script ..."
    
    # Using local mode for standalone tests if Hadoop is missing, 
    # but actual command depends on cluster. 
    # Try MapReduce mode first, fallback or standard execution.
    try {
        # Using mapreduce mode if Hadoop is there, otherwise could use local mode: -x local
        if ($hadoopExe) {
            pig -x mapreduce $scriptPath
        } else {
            pig -x local $scriptPath
        }
        Write-Host "Successfully executed $script" -ForegroundColor Green
    } catch {
        Write-Host "Failed to execute $script" -ForegroundColor Red
    }
}

Write-Host "Pig execution completed."
