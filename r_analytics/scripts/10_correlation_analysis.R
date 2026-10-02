# 10_correlation_analysis.R
library(dplyr)

source(file.path("config", "settings.R"))

perform_correlation_analysis <- function(df) {
  cat("[INFO] Performing correlation analysis...\n")
  
  # Select appropriate numeric variables
  numeric_df <- df %>%
    select(vehicle_count, average_speed, occupancy_rate, latitude, longitude) %>%
    na.omit()
  
  if (nrow(numeric_df) > 1) {
    corr_matrix <- cor(numeric_df, method = "pearson")
    write.csv(corr_matrix, file.path(OUTPUT_DIR, "correlation_analysis.csv"), row.names = TRUE)
    
    # Try to plot with corrplot if available, else use base R or ggplot workaround
    if (requireNamespace("corrplot", quietly = TRUE)) {
      library(corrplot)
      png(file.path(PLOT_DIR, "correlation_matrix.png"), width = 800, height = 600)
      corrplot(corr_matrix, method = "color", addCoef.col = "black", tl.col="black", tl.srt=45)
      dev.off()
    } else {
      cat("[WARN] corrplot package not available. Using base R heatmap for correlation plot.\n")
      png(file.path(PLOT_DIR, "correlation_matrix.png"), width = 800, height = 600)
      heatmap(corr_matrix, Rowv = NA, Colv = NA, margins = c(10,10), main="Correlation Matrix")
      dev.off()
    }
    
    cat("[INFO] Saved correlation analysis and plot.\n")
  } else {
    cat("[WARN] Not enough numeric data for correlation analysis.\n")
  }
}

if (exists("df")) {
  perform_correlation_analysis(df)
}
