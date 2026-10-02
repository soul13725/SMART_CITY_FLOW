# run_all.R
cat("Starting Smart City Traffic Analytics Platform - Phase 10 (R Analytics)\n")

# Start timer
start_time <- Sys.time()

# Ensure we are in the correct directory. Assuming it's run from project root or r_analytics.
if (!dir.exists("scripts") && dir.exists("r_analytics/scripts")) {
  setwd("r_analytics")
}

cat("[1/13] Loading data...\n")
source(file.path("scripts", "01_load_validate.R"))

cat("[2/13] Validating schema... (Handled in step 1)\n")

cat("[3/13] Prepare data... (Handled in step 1)\n")

cat("[4/13] Descriptive statistics...\n")
source(file.path("scripts", "02_descriptive_analysis.R"))

cat("[5/13] Vehicle analysis...\n")
source(file.path("scripts", "03_vehicle_analysis.R"))

cat("[6/13] Junction analysis...\n")
source(file.path("scripts", "04_junction_analysis.R"))

cat("[7/13] Density analysis...\n")
source(file.path("scripts", "05_density_analysis.R"))

cat("[8/13] Speed analysis...\n")
source(file.path("scripts", "06_speed_analysis.R"))

cat("[9/13] Weather analysis...\n")
source(file.path("scripts", "07_weather_analysis.R"))

cat("[10/13] Incident analysis...\n")
source(file.path("scripts", "08_incident_analysis.R"))

cat("[11/13] Time analysis...\n")
source(file.path("scripts", "09_time_analysis.R"))

cat("[12/13] Correlation analysis...\n")
source(file.path("scripts", "10_correlation_analysis.R"))

cat("[13/13] Analytics complete.\n")

end_time <- Sys.time()
execution_time <- round(as.numeric(difftime(end_time, start_time, units = "secs")), 2)

cat(sprintf("\n--- R Analytics Summary ---\nRecords: %d\nExecution time: %.2f seconds\n", nrow(df), execution_time))
