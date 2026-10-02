# test_r_analytics.R
cat("Running Tests for R Analytics Module...\n")

if (!dir.exists("config") && dir.exists("r_analytics/config")) {
  setwd("r_analytics")
}
source(file.path("config", "settings.R"))

tests_passed <- 0
tests_failed <- 0

assert <- function(condition, test_name) {
  if (isTRUE(condition)) {
    cat(sprintf("[PASS] %s\n", test_name))
    tests_passed <<- tests_passed + 1
  } else {
    cat(sprintf("[FAIL] %s\n", test_name))
    tests_failed <<- tests_failed + 1
  }
}

# Test 1 - Dataset exists
assert(file.exists(DATA_PATH), "Test 1 - Dataset exists")

if (file.exists(DATA_PATH)) {
  df <- read.csv(DATA_PATH, stringsAsFactors = FALSE)
  
  # Test 2 - Schema
  missing_cols <- setdiff(EXPECTED_COLUMNS, colnames(df))
  assert(length(missing_cols) == 0, "Test 2 - Schema (all required columns present)")
  
  # Test 3 - Non-empty dataset
  assert(nrow(df) > 0, "Test 3 - Non-empty dataset")
  
  # Test 4 - Numeric fields
  num_vc <- suppressWarnings(as.numeric(df$vehicle_count))
  num_as <- suppressWarnings(as.numeric(df$average_speed))
  num_or <- suppressWarnings(as.numeric(df$occupancy_rate))
  num_lat <- suppressWarnings(as.numeric(df$latitude))
  num_lon <- suppressWarnings(as.numeric(df$longitude))
  
  assert(!all(is.na(num_vc)) && !all(is.na(num_as)) && !all(is.na(num_or)) && !all(is.na(num_lat)) && !all(is.na(num_lon)), "Test 4 - Numeric fields conversion succeeds")
  
  # Test 5 - Timestamp
  ts <- suppressWarnings(as.POSIXct(df$timestamp, format="%Y-%m-%dT%H:%M:%S", tz="UTC"))
  assert(!all(is.na(ts)), "Test 5 - Timestamp format is parsable")
  
  # Test 6 - Event IDs
  assert(sum(is.na(df$event_id) | df$event_id == "") == 0, "Test 6 - Event IDs are present")
} else {
  cat("[FAIL] Skipping Tests 2-6 because dataset does not exist.\n")
}

# Test 7 - Output generation & Test 8 - Plot generation
# These depend on run_all.R being executed prior to tests, or we just check if the files exist.
expected_csv <- c("descriptive_statistics.csv", "vehicle_analysis.csv", "junction_analysis.csv", "density_analysis.csv", "speed_analysis.csv", "weather_analysis.csv", "incident_analysis.csv", "hourly_analysis.csv", "daily_analysis.csv", "correlation_analysis.csv")
expected_png <- c("vehicle_distribution.png", "junction_traffic.png", "density_distribution.png", "speed_distribution.png", "speed_by_vehicle.png", "weather_distribution.png", "incidents.png", "hourly_traffic.png", "daily_traffic.png", "correlation_matrix.png")

all_csv_exist <- all(sapply(expected_csv, function(x) file.exists(file.path(OUTPUT_DIR, x))))
assert(all_csv_exist, "Test 7 - Output CSV generation")

all_png_exist <- all(sapply(expected_png, function(x) file.exists(file.path(PLOT_DIR, x))))
assert(all_png_exist, "Test 8 - Plot PNG generation")

cat(sprintf("\nTest Summary: %d Passed, %d Failed\n", tests_passed, tests_failed))
if (tests_failed > 0) quit(status = 1)
