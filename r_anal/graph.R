library(tidyverse)
library(ggplot2)

graphify <- function(ftrack_name){
    ftrack <- read.csv(sprintf("sim/%s_ftrack.csv", ftrack_name))
    ftrack <- within(ftrack, {
        sim_id <- factor(sim_id)
    })
    p <- ggplot(data = ftrack,
        aes(x = generation, y = fitness, group = sim_id))
    p + geom_line(aes(color = sim_id)) +
    stat_smooth(aes(group = 1)) +
    stat_summary(aes(group = 1), geom = "point", fun = mean) +
    scale_x_continuous(
        breaks = seq(min(ftrack$generation),
            max(ftrack$generation), by = 1)) +
    labs(x = "Generations", y = "Fitness", col = "Simulation")
    ggsave(sprintf("figures/%s_ftrack.pdf", ftrack_name))
}

map(c("ctrl", "rmg", "umg"), graphify)