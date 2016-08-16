# Load Library
library(rFSA)

args <- commandArgs(trailingOnly = TRUE)
filename <- commandArgs[1]

# Import file
df <- read.table(filename,sep=',',header=TRUE)
disname<-colnames(df)[dim(df)[2]]

## Remove columns with SNPs showing only one state
vec<-rep(NA,dim(df)[2]-1)
for(i in 1:(dim(df)[2]-1)){
  vec[i]<-length(levels(df[,i]))
}

## SNPs that cannot be included becuase they only have one category:
newdf<-df[,-which(vec<=1)]

## Run FSA
fit<-glmFSA(yname=disname,
            m=2,
            numrs=10,
            interactions = TRUE,
            save_solutions = TRUE,
            minmax = "min",
            criterion = int.p.val,
            data=newdf)

## Results output to 'FSAsolutions.csv'