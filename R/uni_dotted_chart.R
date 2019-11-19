args <- commandArgs(TRUE)
log <- args[1]
pic <- args[2]
type <- args[3]
start <- args[4]

library(bupaR)

data <- read_xes(log)
dc <- data %>% dotted_chart(x = type, y = start)
png(filename=pic)
plot(dc)
dev.off()