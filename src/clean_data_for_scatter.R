library(tidyverse)

players <- read_csv("/workdir/data/atacantes_femenil.csv", show_col_types = FALSE) |>
  janitor::clean_names() |>
  filter(minutes_played > 900) |>
  filter(position != "GK") |>
  mutate(radio = sqrt(assists_per_90^2 + goals_per_90^2)) |>
  mutate(radio = 0.004 + (radio*0.012)/max(radio)) |>
  write_csv("data/femenil_player_for_scatter.csv")
