# settings.R
# Configuration for R Analytics

DATA_PATH <- file.path("..", "data", "generated", "traffic_events.csv")
OUTPUT_DIR <- file.path("output")
PLOT_DIR <- file.path("plots")

# Ensure output directories exist
if (!dir.exists(OUTPUT_DIR)) {
  dir.create(OUTPUT_DIR, recursive = TRUE)
}

if (!dir.exists(PLOT_DIR)) {
  dir.create(PLOT_DIR, recursive = TRUE)
}

EXPECTED_COLUMNS <- c(
  "event_id", "timestamp", "sensor_id", "junction_id", "lane_id",
  "vehicle_type", "vehicle_count", "average_speed", "traffic_density",
  "weather_condition", "latitude", "longitude", "occupancy_rate",
  "road_type", "direction", "incident_status"
)
