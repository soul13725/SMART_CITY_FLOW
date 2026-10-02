# 07_weather_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_weather_analysis <- function(df) {
  cat("[INFO] Performing weather analysis...\n")
  
  total_events <- nrow(df)
  
  weather_stats <- df %>%
    group_by(weather_condition) %>%
    summarise(
      event_count = n(),
      percentage = (n() / total_events) * 100,
      average_speed = mean(average_speed, na.rm = TRUE),
      average_vehicle_count = mean(vehicle_count, na.rm = TRUE),
      average_occupancy = mean(occupancy_rate, na.rm = TRUE)
    )
  
  write.csv(weather_stats, file.path(OUTPUT_DIR, "weather_analysis.csv"), row.names = FALSE)
  
  # Plot
  p <- ggplot(weather_stats, aes(x = weather_condition, y = percentage, fill=weather_condition)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(
      title = "Distribution of Weather Conditions",
      x = "Weather Condition",
      y = "Percentage of Events (%)"
    )
    
  ggsave(file.path(PLOT_DIR, "weather_distribution.png"), plot = p, width = 8, height = 6)
  cat("[INFO] Saved weather analysis and plot.\n")
}

if (exists("df")) {
  perform_weather_analysis(df)
}
