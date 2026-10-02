# 06_speed_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_speed_analysis <- function(df) {
  cat("[INFO] Performing speed analysis...\n")
  
  speed_stats <- data.frame(
    mean = mean(df$average_speed, na.rm = TRUE),
    median = median(df$average_speed, na.rm = TRUE),
    sd = sd(df$average_speed, na.rm = TRUE),
    min = min(df$average_speed, na.rm = TRUE),
    max = max(df$average_speed, na.rm = TRUE),
    q1 = quantile(df$average_speed, 0.25, na.rm = TRUE),
    q3 = quantile(df$average_speed, 0.75, na.rm = TRUE)
  )
  
  write.csv(speed_stats, file.path(OUTPUT_DIR, "speed_analysis.csv"), row.names = FALSE)
  
  # Plot speed distribution
  p1 <- ggplot(df, aes(x = average_speed)) +
    geom_histogram(binwidth = 5, fill = "lightblue", color = "black", alpha=0.7) +
    geom_density(aes(y = ..count.. * 5), color="red", size=1) +
    theme_minimal() +
    labs(
      title = "Distribution of Average Speed",
      x = "Average Speed",
      y = "Frequency"
    )
    
  ggsave(file.path(PLOT_DIR, "speed_distribution.png"), plot = p1, width = 8, height = 6)
  
  # Plot speed by vehicle type
  p2 <- ggplot(df, aes(x = vehicle_type, y = average_speed, fill=vehicle_type)) +
    geom_boxplot() +
    theme_minimal() +
    labs(
      title = "Speed Distribution by Vehicle Type",
      x = "Vehicle Type",
      y = "Average Speed"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
  ggsave(file.path(PLOT_DIR, "speed_by_vehicle.png"), plot = p2, width = 8, height = 6)
  
  cat("[INFO] Saved speed analysis and plots.\n")
}

if (exists("df")) {
  perform_speed_analysis(df)
}
