import pandas
import numpy as np

def generate_snp_acc_mapping(table_file):
    with open(table_file) as snps:
        header = False
        snp_map = {}
        for snp in (l for l in snps if not l.startswith('#')):
            if not header:
                header = snp
            snp = snp.split('\t')
            snp_map[snp[0]] = snp[2] if snp[2].startswith('rs') else snp[1]
    return snp_map

def pull_snp_variants(snp_table, snp_map):
    snps = pandas.read_table(snp_table, index_col=0).transpose()
    #snps = snps.replace('No Call', '')
    snps.columns = [snp_map[c] for c in snps.columns]
    snps = snps.drop('', axis=1).head()
    return snps