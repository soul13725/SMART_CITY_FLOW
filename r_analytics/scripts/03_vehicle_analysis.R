# 03_vehicle_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_vehicle_analysis <- function(df) {
  cat("[INFO] Performing vehicle analysis...\n")
  
  veh_stats <- df %>%
    group_by(vehicle_type) %>%
    summarise(
      event_count = n(),
      total_vehicle_count = sum(vehicle_count, na.rm = TRUE),
      average_vehicle_count = mean(vehicle_count, na.rm = TRUE),
      average_speed = mean(average_speed, na.rm = TRUE),
      average_occupancy = mean(occupancy_rate, na.rm = TRUE)
    )
  
  write.csv(veh_stats, file.path(OUTPUT_DIR, "vehicle_analysis.csv"), row.names = FALSE)
  
  # Plot
  p <- ggplot(veh_stats, aes(x = reorder(vehicle_type, -total_vehicle_count), y = total_vehicle_count, fill=vehicle_type)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(
      title = "Total Vehicle Count by Vehicle Type",
      x = "Vehicle Type",
      y = "Total Vehicle Count"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
  ggsave(file.path(PLOT_DIR, "vehicle_distribution.png"), plot = p, width = 8, height = 6)
  cat("[INFO] Saved vehicle analysis and plot.\n")
}

if (exists("df")) {
  perform_vehicle_analysis(df)
}
