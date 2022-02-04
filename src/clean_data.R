library("tidyverse")

columnas <- c("anios_esc", "hrsocup", "ingocup", "ing_x_hrs")
trimestre <- read_csv("data/primer_trimetre_2005.csv") %>%
  select(columnas) %>%
  filter(hrsocup > 15) %>%
  filter(anios_esc < 30)

trimestre_por_estudios <- trimestre %>%
  group_by(anios_esc) %>%
  summarize(
    ingreso = mean(ingocup),
    horas = mean(hrsocup)
  )
write_csv(trimestre_por_estudios, "trimestre_por_estudios.csv")