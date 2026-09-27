Write-Host "Running Hadoop Streaming MapReduce Job: Vehicle Count"

# Default fallback if HADOOP_HOME is set
if ($env:HADOOP_HOME) {
    $HADOOP_STREAMING_JAR = "$env:HADOOP_HOME\share\hadoop\tools\lib\hadoop-streaming-*.jar"
} else {
    Write-Host "HADOOP_HOME not set! Runtime is blocked."
    exit 1
}

hadoop jar $HADOOP_STREAMING_JAR `
    -files "..\mapreduce\jobs\vehicle_count_mapper.py,..\mapreduce\jobs\vehicle_count_reducer.py" `
    -mapper "python vehicle_count_mapper.py" `
    -reducer "python vehicle_count_reducer.py" `
    -input "/smartcity/traffic/raw/traffic_events.csv" `
    -output "/smartcity/traffic/output/vehicle_count"

Write-Host "Job Finished. Inspecting Output:"
hdfs dfs -cat /smartcity/traffic/output/vehicle_count/part-00000
