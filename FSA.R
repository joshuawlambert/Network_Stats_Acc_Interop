# Load Library
library(rFSA)


# Import file
df <- read.table(filename,sep=',',header=TRUE)
disname<-colnames(df)[dim(df)[2]]

## Remove columns with SNPs showing only one state
vec<-rep(NA,dim(df)[2]-1)
for(i in 1:(dim(df)[2]-1)){
  vec[i]<-length(unique(df[,i]))
}

## Remove SNPs that only have one genotype
if (length(which(vec<=1))>0){ print('yes')
  keeps<-(1:(dim(df)[2]-1))[-which(vec<=1)]
  df<-df[,c(keeps,dim(df)[2])]
}

## Run FSA
fit<-glmFSA(yname=disname,
            m=2,
            numrs=10,
            interactions = TRUE,
            save_solutions = FALSE,
            minmax = "min",
            criterion = int.p.val,
            data=df)

write.table(fit$table,paste0(filename,'.output'))
