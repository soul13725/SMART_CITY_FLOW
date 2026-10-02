# 05_density_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_density_analysis <- function(df) {
  cat("[INFO] Performing density analysis...\n")
  
  total_events <- nrow(df)
  
  density_stats <- df %>%
    group_by(traffic_density) %>%
    summarise(
      event_count = n(),
      percentage = (n() / total_events) * 100,
      average_vehicle_count = mean(vehicle_count, na.rm = TRUE),
      average_speed = mean(average_speed, na.rm = TRUE),
      average_occupancy = mean(occupancy_rate, na.rm = TRUE)
    )
  
  write.csv(density_stats, file.path(OUTPUT_DIR, "density_analysis.csv"), row.names = FALSE)
  
  # Plot
  p <- ggplot(density_stats, aes(x = traffic_density, y = percentage, fill=traffic_density)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(
      title = "Distribution of Traffic Density",
      x = "Traffic Density",
      y = "Percentage of Events (%)"
    )
    
  ggsave(file.path(PLOT_DIR, "density_distribution.png"), plot = p, width = 8, height = 6)
  cat("[INFO] Saved density analysis and plot.\n")
}

if (exists("df")) {
  perform_density_analysis(df)
}
