# 04_junction_analysis.R
library(dplyr)
library(ggplot2)

source(file.path("config", "settings.R"))

perform_junction_analysis <- function(df) {
  cat("[INFO] Performing junction analysis...\n")
  
  junc_stats <- df %>%
    group_by(junction_id) %>%
    summarise(
      event_count = n(),
      total_vehicle_count = sum(vehicle_count, na.rm = TRUE),
      average_vehicle_count = mean(vehicle_count, na.rm = TRUE),
      average_speed = mean(average_speed, na.rm = TRUE),
      average_occupancy = mean(occupancy_rate, na.rm = TRUE)
    ) %>%
    arrange(desc(total_vehicle_count))
  
  write.csv(junc_stats, file.path(OUTPUT_DIR, "junction_analysis.csv"), row.names = FALSE)
  
  # Identification of high traffic junctions based on total vehicle count
  highest_vol_junc <- junc_stats$junction_id[1]
  lowest_speed_junc <- junc_stats %>% arrange(average_speed) %>% pull(junction_id) %>% .[1]
  
  cat(sprintf("[INFO] Highest observed vehicle volume at: %s\n", highest_vol_junc))
  cat(sprintf("[INFO] Lowest observed average speed at: %s\n", lowest_speed_junc))
  
  # Plot
  # Take top 20 for readability if there are many
  top_juncs <- junc_stats %>% head(20)
  
  p <- ggplot(top_juncs, aes(x = reorder(junction_id, -total_vehicle_count), y = total_vehicle_count)) +
    geom_bar(stat = "identity", fill="steelblue") +
    theme_minimal() +
    labs(
      title = "Total Vehicle Count by Junction (Top 20)",
      x = "Junction ID",
      y = "Total Vehicle Count"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
  ggsave(file.path(PLOT_DIR, "junction_traffic.png"), plot = p, width = 10, height = 6)
  cat("[INFO] Saved junction analysis and plot.\n")
}

if (exists("df")) {
  perform_junction_analysis(df)
}
