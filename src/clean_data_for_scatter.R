library(tidyverse)

players <- read_csv("data/LigaMX.csv", show_col_types = FALSE) |>
  janitor::clean_names() |>
  filter(minutes_played > 900) |>
  write_csv("data/player_for_scatter.csv")
