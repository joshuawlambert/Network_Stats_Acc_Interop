import argparse

from parse import read_vcf, parse_snps_geo, read_phenotypes
from SubSetMatrix import subset_wrap
from Grouping import method_map

def main(args):
    if args.ftype=='VCF':
        snps = read_vcf(args.fname)
    elif args.ftype=='GEO':
        snps = parse_snps_geo(args.fname)

    #snps contains DataFrame with SNP columns and sample rows
    phenotypes = read_phenotypes(args.pheno)

    group_method = method_map[args.group_method]

    groups = group_method(args.group_method_args)

    subsets = subset_wrap(snps, groups, phenotypes)

    for subset in subsets:
        #call FSA here



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Associate SNP pair interactions with phenotype.')

