# Load Library
library(rFSA)

args <- commandArgs(trailingOnly = TRUE)
filename <- args[1]


# Import file
df <- read.table(filename,sep=',',header=TRUE)
disname<-colnames(df)[dim(df)[2]]

## Remove columns with SNPs showing only one state
vec<-rep(NA,dim(df)[2]-1)
for(i in 1:(dim(df)[2]-1)){
  snp<-df[,i]
  vec[i]<-length(levels(snp))
}

## Remove SNPs that only have one genotype
if (length(which(vec<=1))>0){ 
  keeps<-(1:(dim(df)[2]-1))[-which(vec<=1)]
  df<-df[,c(keeps,dim(df)[2])]
}



## Run FSA
fit<-genFSA(yname=disname,
            m=2,
            numrs=10,
            interactions = TRUE,
            save_solutions = TRUE,
            minmax = "min",
            criterion = int.p.val,
            checknum=100,
            data=df)

## Results output to 'FSAsolutions.csv'

write.table(fit$table,paste0(filename,'.output'))
