# 08_incident_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_incident_analysis <- function(df) {
  cat("[INFO] Performing incident analysis...\n")
  
  total_events <- nrow(df)
  
  incident_stats <- df %>%
    group_by(incident_status) %>%
    summarise(
      event_count = n(),
      percentage = (n() / total_events) * 100,
      average_speed = mean(average_speed, na.rm = TRUE),
      average_vehicle_count = mean(vehicle_count, na.rm = TRUE)
    )
  
  write.csv(incident_stats, file.path(OUTPUT_DIR, "incident_analysis.csv"), row.names = FALSE)
  
  # Plot
  p <- ggplot(incident_stats, aes(x = incident_status, y = percentage, fill=incident_status)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(
      title = "Distribution of Incident Status",
      x = "Incident Status",
      y = "Percentage of Events (%)"
    )
    
  ggsave(file.path(PLOT_DIR, "incidents.png"), plot = p, width = 8, height = 6)
  cat("[INFO] Saved incident analysis and plot.\n")
}

if (exists("df")) {
  perform_incident_analysis(df)
}
