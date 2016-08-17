#!

curl ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/All/$1.assembly.txt | grep -v ^# | python replace_accesssion.py $2 $3 $4

