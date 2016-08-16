##############################################################
## Preliminary function -- will remove when rFSA is fixed
##############################################################
glmFSA2=function(yname,data,fixvar=NULL,quad=F,m=2,numrs=1,save_solutions=F,cores=1,interactions=F,criterion=AIC,minmax="min",fam="binomial",...){
  originalnames<-colnames(data)
  data<-data.frame(data)
  lhsvar<-yname
  
  ypos<-which(colnames(data)==lhsvar)
  startvar<-NULL
  xdata<-data[,-ypos]
  ydata<-data[,ypos]
  newdata<<-data.frame(cbind(ydata,xdata))
  fixpos<-which(colnames(xdata) %in% fixvar)
  if(length(fixpos)==0){fixpos=NULL}
  
  history<-matrix(rep(NA,numrs*(2*m+3)),ncol=((2*m+3)))
  history[,1:m]<-rstart(m=m,nvars=(dim(newdata)[2]-1),numrs=numrs)
  curpos<-which(colnames(xdata) %in% startvar[-1])
  if(length(curpos)!=0){history<-rbind(c(curpos,rep(NA,length(curpos)+2)),history)}
  
  fsa<-function(i,history,...){
    cur<-history[i,1:m]
    last<-rep(NA,m)
    numswap<-0
    memswap<-NULL
    if(minmax=="max"){last.criterion<-(-Inf)}
    if(minmax=="min"){last.criterion<-(Inf)}
    checks<-0
    while(!identical(cur,last)&&!identical(c(cur[2],cur[1]),last)){
      last<-cur
      if(numswap==0){moves<<-swaps(cur = cur,n = dim(xdata)[2],quad=quad)}
      if(numswap>0){moves<<-nextswap(curpos = cur,n = dim(xdata)[2],quad=quad,prevpos =memswap)$nswaps
      }
      vec<-rep(NA,dim(moves)[2])
      for(g in 1:(dim(moves)[2])){
        if(is.factor(xdata[,moves[1,g]]) && is.factor(xdata[,moves[2,g]])){
          int<-(paste(xdata[,moves[1,g]],xdata[,moves[2,g]]))
          int[is.na(xdata[,moves[1,g]])|is.na(xdata[,moves[2,g]])]<-NA
          int<-as.factor(int)
          h <- length(levels(int))
          int1 <- xdata[,moves[1,g]]
          int2 <- xdata[,moves[2,g]]
          l1 <- length(levels(int1))
          l2 <- length(levels(int2))
          if(l1*l2 != h){
            vec[g] <- 1
          }
        }
      }
      if(length(which(vec==1))>0){
        keeps<-(1:(dim(moves)[2]))[-which(vec==1)]
        moves <- moves[,keeps]
      }
      if(interactions==T){form<-function(j) formula(paste0(colnames(newdata)[1],"~",paste0(fixvar,sep="+"),paste(colnames(xdata)[moves[,j]],collapse = "*")),sep="")}
      if(interactions==F){form<-function(j) formula(paste0(colnames(newdata)[1],"~",paste0(fixvar,sep="+"),paste(colnames(xdata)[moves[,j]],collapse = "+")),sep="")}
      tmp<-mclapply(X = 1:dim(moves)[2],FUN = function(k) criterion(glm(form(k),data=newdata,family=fam,...)),mc.cores=cores)
      
      checks<-checks+dim(moves)[2]
      if(minmax=="max"){cur<-moves[,which.max.na(unlist(tmp))[1]]
      cur.criterion<-unlist(tmp[which.max.na(unlist(tmp))[1]])
      if(last.criterion>cur.criterion){cur<-last.pos
      cur.criterion<-last.criterion}
      }
      if(minmax=="min"){cur<-moves[,which.min.na(unlist(tmp))[1]]
      cur.criterion<-unlist(tmp[which.min.na(unlist(tmp))[1]])
      if(last.criterion<cur.criterion){cur<-last.pos
      cur.criterion<-last.criterion}
      }
      
      
      numswap<-numswap+1
      last1<-last
      last.criterion<-cur.criterion
      last.pos<-cur
      memswap<-unique(c(memswap,last1))
    }
    history[i,(1+m):(2*m)]<-cur
    history[i,(dim(history)[2]-2)]<-cur.criterion
    history[i,(dim(history)[2]-1)]<-numswap-1
    history[i,(dim(history)[2])]<-checks
    return(history[i,])
  }
  solutions<-matrix(unlist(lapply(1:numrs,FUN =function(i) fsa(i,history))),ncol=dim(history)[2],byrow = T)
  solutions[,1:(2*m)]<-matrix(colnames(newdata)[c(solutions[,1:(2*m)]+1)],ncol=(2*m))
  solutions<-data.frame(solutions)
  print
  colnames(solutions)[dim(solutions)[2]:(dim(solutions)[2]-2)]=c("checks","swaps","criterion")
  colnames(solutions)[1:m]=paste("start",1:m,sep=".")
  colnames(solutions)[(m+1):(m*2)]=paste("best",1:m,sep=".")
  solutions$criterion<-as.numeric(levels(solutions$criterion))[solutions$criterion]
  solutions$swaps<-as.numeric(levels(solutions$swaps))[solutions$swaps]
  solutions$checks<-as.numeric(levels(solutions$checks))[solutions$checks]
  if(length(fixvar)!=0){solutions<-data.frame(fixvar=matrix(rep(x=fixvar,dim(solutions)[1]),nrow=dim(solutions)[1],byrow=T),solutions)}
  if(save_solutions==T){write.csv(solutions,paste0(getwd(),"/FSAsolutions",".csv"))}
  solutions<<-solutions
  a<-solutions[,(length(fixvar)+m+1):(length(fixvar)+m+1+m)]
  b<-unique(t(apply(a,sort,MARGIN = 1)),MARGIN = 1)
  a<-t(apply(a,sort,MARGIN = 1))
  c<-cbind(b,0)
  for(i in 1:dim(b)[1]){
    for(j in 1:dim(a)[1]){
      c[i,(m+2)]<-sum(as.numeric(c[i,(m+2)])+as.numeric(identical(a[j,],b[i,])))
    }
  }
  tableres<-data.frame(cbind(c,NA),stringsAsFactors = F)
  colnames(tableres)[(dim(tableres)[2]-1)]<-"times"
  colnames(tableres)[2:(dim(tableres)[2]-2)]<-paste("Var",2:(dim(tableres)[2]-2),sep="")
  colnames(tableres)[1] <- "criterion"
  colnames(tableres)[dim(tableres)[2]]<-"warnings"
  withWarnings <- function(expr) {
    myWarnings <- NULL
    wHandler <- function(w) {
      myWarnings <<- c(myWarnings, list(w))
      invokeRestart("muffleWarning")
    }
    val <- withCallingHandlers(expr, warning = wHandler)
    list(value = val, warnings = myWarnings)
  }
  form<-function(j) formula(paste0(colnames(newdata)[1],"~",paste0(fixvar,sep="+"),paste(tableres[j,2:m+1],collapse = "*")),sep="")
  warns<-NULL
  for (i in 1:dim(tableres)[1]){
    ca<-as.character(withWarnings(glm(form(i),data=newdata,family=fam,...))$warnings[[1]])
    if(length(ca)==0){warns<-c(warns,NA)}
    else{warns<-c(warns,ca)}
  }
  tableres$warnings<-warns
  return(list(solutions=solutions,table=tableres,efficiency=paste("You did:",sum(solutions$checks)," model checks compared to ",choose(n = dim(xdata)[2],k = m)," checks you would have done with exahstive search.")))
}
##############################################################
## End of preliminary function
##############################################################


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
  vec[i]<-length(levels(df[,i]))
}

## SNPs that cannot be included becuase they only have one category:
newdf<-df[,-which(vec<=1)]

## Run FSA
fit<-glmFSA2(yname=disname,
            m=2,
            numrs=10,
            interactions = TRUE,
            save_solutions = TRUE,
            minmax = "min",
            criterion = int.p.val,
            data=newdf)

## Results output to 'FSAsolutions.csv'

write.table(fit$table,paste0(filename,'.output'))