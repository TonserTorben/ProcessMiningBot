args <- commandArgs(TRUE)
log <- args[1]
pic <- args[2]

library(bupaR)

data <- read_xes(log)
dc <- data %>% dotted_chart(x = "absolute", y = "start")
dc <- log %>% filter_resource_frequency(perc = 0.80) %>% resources()
png(filename=pic)
plot(dc)
dev.off() 