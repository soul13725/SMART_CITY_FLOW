# 09_time_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_time_analysis <- function(df) {
  cat("[INFO] Performing time analysis...\n")
  
  # Hourly Analysis
  hourly_stats <- df %>%
    group_by(hour) %>%
    summarise(
      event_count = n(),
      total_vehicle_count = sum(vehicle_count, na.rm = TRUE),
      average_vehicle_count = mean(vehicle_count, na.rm = TRUE),
      average_speed = mean(average_speed, na.rm = TRUE)
    ) %>%
    arrange(hour)
  
  write.csv(hourly_stats, file.path(OUTPUT_DIR, "hourly_analysis.csv"), row.names = FALSE)
  
  p1 <- ggplot(hourly_stats, aes(x = hour, y = total_vehicle_count)) +
    geom_line(color="blue", size=1) +
    geom_point(color="red", size=2) +
    theme_minimal() +
    labs(
      title = "Hourly Total Traffic Volume",
      x = "Hour of Day",
      y = "Total Vehicle Count"
    )
    
  ggsave(file.path(PLOT_DIR, "hourly_traffic.png"), plot = p1, width = 8, height = 6)
  
  # Daily Analysis
  daily_stats <- df %>%
    group_by(date) %>%
    summarise(
      event_count = n(),
      total_vehicle_count = sum(vehicle_count, na.rm = TRUE),
      average_speed = mean(average_speed, na.rm = TRUE)
    ) %>%
    arrange(date)
    
  write.csv(daily_stats, file.path(OUTPUT_DIR, "daily_analysis.csv"), row.names = FALSE)
  
  p2 <- ggplot(daily_stats, aes(x = date, y = total_vehicle_count)) +
    geom_line(color="darkgreen", size=1) +
    geom_point(color="orange", size=2) +
    theme_minimal() +
    labs(
      title = "Daily Total Traffic Volume",
      x = "Date",
      y = "Total Vehicle Count"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
  ggsave(file.path(PLOT_DIR, "daily_traffic.png"), plot = p2, width = 8, height = 6)
  
  cat("[INFO] Saved time analysis and plots.\n")
}

if (exists("df")) {
  perform_time_analysis(df)
}
