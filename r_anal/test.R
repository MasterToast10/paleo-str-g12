library(dplyr)
library(ggplot2)

gen_counts <- read.csv("sim/r_prep.csv")
sample_n(gen_counts, 10)
levels(gen_counts$group)
bartlett.test(generations ~ group, gen_counts)
p <- ggplot(gen_counts, aes(x = group, y = generations, color = group)) + 
  geom_boxplot(notch = TRUE) + theme(legend.position = "none") +
  labs(x = "Treatment", y = "Number of Generations") +
  scale_x_discrete(labels = c("Control", "RMG", "UMG")) +
  scale_y_continuous(breaks = seq(min(gen_counts$generation),
            max(gen_counts$generation), by = 2))
ggsave("figures/boxplot.pdf")
group_by(gen_counts, group) %>%
    summarise(
        count = n(),
        mean = mean(generations, na.rm = TRUE),
        sd = sd(generations, na.rm = TRUE)
    )
res_aov <- aov(generations ~ group, gen_counts)
summary(res_aov)
TukeyHSD(res_aov)