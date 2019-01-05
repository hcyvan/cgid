
args <- commandArgs(T)

if(length(args) < 3){
    message('Rscript merge_csv.R <DATA_DIR> <CITY> <WEEK>')
    q()
}


data_dir <- args[1]
city <- args[2]
week <-args[3]



library(data.table)
library(rjson)

data_dir <- './data'
city <- 'V0110000'
week <- '20180903'

setwd(data_dir)

tables <- c('stay', 'insight', 'humanTraffic', 'consumption', 'mobilePhone')
files <- paste0(paste(city, week, tables, sep = '_'), '.csv')

stay <- fread(files[1])

apply(stay, 1, function(row){
    row[1]
})->tmp



