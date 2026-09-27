param(
    [string]$LocalFile = "..\..\data\generated\traffic_events_large.csv",
    [string]$HdfsDest = "/smartcity/traffic/raw/traffic_events.csv"
)
Write-Host "Uploading $LocalFile to $HdfsDest ..."
hdfs dfs -put -f $LocalFile $HdfsDest
hdfs dfs -du -h $HdfsDest
