# 01_load_validate.R
library(readr)
library(dplyr)
library(lubridate)

source(file.path("config", "settings.R"))

load_and_validate <- function() {
  cat("[INFO] Loading data from:", DATA_PATH, "\n")
  
  if (!file.exists(DATA_PATH)) {
    stop(paste("Data file not found at", DATA_PATH))
  }
  
  # Read dataset
  df <- read_csv(DATA_PATH, show_col_types = FALSE)
  
  # Validate columns
  missing_cols <- setdiff(EXPECTED_COLUMNS, colnames(df))
  if (length(missing_cols) > 0) {
    stop(paste("Missing required columns:", paste(missing_cols, collapse = ", ")))
  }
  
  # Validation summary
  total_records <- nrow(df)
  total_columns <- ncol(df)
  missing_values <- sum(is.na(df))
  duplicate_events <- sum(duplicated(df$event_id))
  
  # Data type conversion and time-derived fields
  df <- df %>%
    mutate(
      timestamp = as.POSIXct(timestamp, format="%Y-%m-%dT%H:%M:%S", tz="UTC"),
      vehicle_count = as.numeric(vehicle_count),
      average_speed = as.numeric(average_speed),
      occupancy_rate = as.numeric(occupancy_rate),
      latitude = as.numeric(latitude),
      longitude = as.numeric(longitude),
      
      # Derived fields
      date = as.Date(timestamp),
      hour = hour(timestamp),
      day = day(timestamp),
      day_of_week = wday(timestamp, label=TRUE),
      month = month(timestamp, label=TRUE)
    )
  
  invalid_timestamps <- sum(is.na(df$timestamp))
  invalid_numeric <- sum(
    df$vehicle_count < 0 | 
    df$average_speed < 0 | 
    df$occupancy_rate < 0 | 
    df$occupancy_rate > 100, na.rm = TRUE
  )
  
  invalid_categorical <- sum(!df$traffic_density %in% c("LOW", "MEDIUM", "HIGH", "SEVERE", "JAM"))
  
  cat("--- Validation Summary ---\n")
  cat("Total records:", total_records, "\n")
  cat("Total columns:", total_columns, "\n")
  cat("Missing values:", missing_values, "\n")
  cat("Duplicate event IDs:", duplicate_events, "\n")
  cat("Invalid timestamps:", invalid_timestamps, "\n")
  cat("Invalid numeric records:", invalid_numeric, "\n")
  cat("Invalid categorical values:", invalid_categorical, "\n")
  cat("--------------------------\n")
  
  return(df)
}

df <- load_and_validate()
