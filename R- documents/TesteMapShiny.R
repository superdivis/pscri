#load libraries
library(shiny)
library(leaflet)
library(dplyr)
library(leaflet.extras)

#import data
data <- read.csv("E:/Alex/Livano/IPEA/ipea-promob/Calculadora_Insumo_Produto/Calculadora/worldearthquakes.csv")


#categorize earthquake depth
data$depth_type <- ifelse(data$depth <= 70, "shallow", ifelse(data$depth <= 300 | data$depth >70, "intermediate", ifelse(data$depth > 300, "deep", "other")))

