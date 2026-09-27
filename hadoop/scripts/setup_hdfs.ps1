Write-Host "Creating HDFS Directories..."
hdfs dfs -mkdir -p /smartcity/traffic/raw
hdfs dfs -mkdir -p /smartcity/traffic/processed
hdfs dfs -mkdir -p /smartcity/traffic/output
Write-Host "Verification:"
hdfs dfs -ls /smartcity/traffic
