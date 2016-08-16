#!python parse_csv.py

import sys

SNPs = {};
rsIndex = 2;
first_sample = 9;


for line in sys.stdin:
        if not line.startswith('##'):
                if line.startswith('#'):
                        header = line.split('\t')
                else:
                        fields = line.split('\t')
                        samples = []
                        for index in range(first_sample, len(fields)):

                                ret = "AB"
                                if(fields[index][0] == '0' and fields[index][2] == '0'):
                                        ret = "AA"
                                elif(fields[index][2] == '1'):
                                        ret = "BB"
                                
                                        
                                samples.append(ret)
                                        
                        SNPs[fields[rsIndex]] = samples;

line =  header[rsIndex]

for index in range(first_sample, len(header)):
        line = line + "\t" + header[index];
print line

        
for rsID in SNPs:
        print str(rsID) + "\t" + "\t".join(SNPs[rsID]) + "\n"
print len(SNPs);
