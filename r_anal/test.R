library(dplyr)

gen_counts <- read.csv("sim/r_prep.csv")
sample_n(gen_counts, 10)
levels(gen_counts$group)
bartlett.test(generations ~ group, gen_counts)
boxplot(generations ~ group, gen_counts)
group_by(gen_counts, group) %>%
    summarise(
        count = n(),
        mean = mean(generations, na.rm = TRUE),
        sd = sd(generations, na.rm = TRUE)
    )
res.aov <- aov(generations ~ group, gen_counts)
summary(res.aov)
TukeyHSD(res.aov)