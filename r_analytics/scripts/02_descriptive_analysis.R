# 02_descriptive_analysis.R
library(dplyr)
library(tidyr)

source(file.path("config", "settings.R"))

perform_descriptive_analysis <- function(df) {
  cat("[INFO] Performing descriptive analysis...\n")
  
  calc_stats <- function(x) {
    c(
      count = length(na.omit(x)),
      mean = mean(x, na.rm = TRUE),
      median = median(x, na.rm = TRUE),
      minimum = min(x, na.rm = TRUE),
      maximum = max(x, na.rm = TRUE),
      sd = sd(x, na.rm = TRUE),
      q1 = quantile(x, 0.25, na.rm = TRUE),
      q3 = quantile(x, 0.75, na.rm = TRUE)
    )
  }
  
  # Note: occupancy_rate might not have quartiles in the requested calculate list, but adding them doesn't hurt.
  stats_vc <- calc_stats(df$vehicle_count)
  stats_as <- calc_stats(df$average_speed)
  stats_or <- calc_stats(df$occupancy_rate)
  
  # Combine into a dataframe
  desc_stats <- data.frame(
    Metric = c("count", "mean", "median", "minimum", "maximum", "standard_deviation", "q1", "q3"),
    vehicle_count = stats_vc,
    average_speed = stats_as,
    occupancy_rate = stats_or
  )
  
  write.csv(desc_stats, file.path(OUTPUT_DIR, "descriptive_statistics.csv"), row.names = FALSE)
  cat("[INFO] Saved descriptive statistics.\n")
}

if (exists("df")) {
  perform_descriptive_analysis(df)
}
