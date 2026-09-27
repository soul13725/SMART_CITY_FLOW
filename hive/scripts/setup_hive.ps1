Write-Host "Setting up Hive environment..."
if (-not (Get-Command "hive" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Hive CLI not found in PATH. Hive setup is BLOCKED." -ForegroundColor Red
    exit 1
}

Write-Host "Running 01_database.hql"
hive -f "..\queries\01_database.hql"
if ($LASTEXITCODE -ne 0) { Write-Host "Failed to create database" -ForegroundColor Red; exit 1 }

Write-Host "Running 02_external_table.hql"
hive -f "..\queries\02_external_table.hql"
if ($LASTEXITCODE -ne 0) { Write-Host "Failed to create external table" -ForegroundColor Red; exit 1 }

Write-Host "Running 03_internal_table.hql"
hive -f "..\queries\03_internal_table.hql"
if ($LASTEXITCODE -ne 0) { Write-Host "Failed to create internal table" -ForegroundColor Red; exit 1 }

Write-Host "Hive setup completed successfully." -ForegroundColor Green
