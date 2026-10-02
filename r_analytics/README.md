# Phase 10 - R Analytics Module

## 1. Purpose
This independent R Analytics module performs statistical analysis and visualization of the Smart City traffic dataset generated in Phase 2.

## 2. Architecture
- **scripts/**: Contains isolated R scripts for various analytical tasks (descriptive stats, weather, time-series, etc.).
- **output/**: Stores CSV files with aggregated statistical analysis.
- **plots/**: Stores generated data visualizations (PNG format).
- **config/**: Contains `settings.R` for centralizing paths and environment variables.
- **tests/**: Contains `test_r_analytics.R` to validate module integrity.

## 3. R version
Requires R >= 4.0.0

## 4. Required packages
- readr
- dplyr
- tidyr
- ggplot2
- lubridate
- corrplot

## 5. Dataset location
The scripts read data from: `../data/generated/traffic_events.csv`

## 6. Canonical schema
1. event_id
2. timestamp
3. sensor_id
4. junction_id
5. lane_id
6. vehicle_type
7. vehicle_count
8. average_speed
9. traffic_density
10. weather_condition
11. latitude
12. longitude
13. occupancy_rate
14. road_type
15. direction
16. incident_status

## 7. How to run
Execute the full analytical pipeline:
```powershell
Rscript r_analytics/scripts/run_all.R
```

## 8. Analytics performed
- **Descriptive Statistics**: Mean, median, quartiles, and dispersion for numeric fields.
- **Vehicle Analysis**: Vehicle counts, average speeds, and distributions by type.
- **Junction Analysis**: Identification of high-traffic junctions.
- **Traffic Density**: Association of density levels with events.
- **Speed Analysis**: Distribution of average speeds and comparison across vehicle types.
- **Weather Analysis**: Comparison of traffic under varied weather conditions.
- **Incident Analysis**: Speed and volume during incidents.
- **Time-Series Analysis**: Hourly and daily traffic volume variations.
- **Correlation Analysis**: Pearson correlations among numerical metrics.

## 9. Generated CSV outputs
Located in `r_analytics/output/`:
- descriptive_statistics.csv
- vehicle_analysis.csv
- junction_analysis.csv
- density_analysis.csv
- speed_analysis.csv
- weather_analysis.csv
- incident_analysis.csv
- hourly_analysis.csv
- daily_analysis.csv
- correlation_analysis.csv

## 10. Generated plots
Located in `r_analytics/plots/`:
- vehicle_distribution.png
- junction_traffic.png
- density_distribution.png
- speed_distribution.png
- speed_by_vehicle.png
- weather_distribution.png
- incidents.png
- hourly_traffic.png
- daily_traffic.png
- correlation_matrix.png

## 11. Testing
Run tests to validate environment and execution:
```powershell
Rscript r_analytics/tests/test_r_analytics.R
```

## 12. Performance results
*Execution blocked.*
Performance benchmarks will be available when a valid R execution environment is provided.

## 13. Limitations
- Does not automatically install missing packages.
- Memory-bound by standard R data frames, suitable for moderate Big Data sets.

## 14. Future integration point
- Output CSVs and visual plots can be exposed via FastAPI (Phase 11) or directly served to the React Dashboard (Phase 12).
