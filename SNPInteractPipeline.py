import argparse

from parse import read_vcf, parse_snps_geo, read_phenotypes, generate_snp_acc_mapping, rename_snps, extract_geo_phenotypes
from SubSetMatrix import subset_wrap
from Grouping import method_map
from FSA import fsa_wrapper

def main(args):
    snp_map = generate_snp_acc_mapping(args.snpmap_file, args.snp_id_label)

    if args.ftype=='VCF':
        snps = read_vcf(args.fname)
        phenotypes = read_phenotypes(args.pheno).iloc[:,0]
        print("Parsed phenotypes")    
    elif args.ftype=='GEO':
        snps = parse_snps_geo(args.fname)
        phenotypes = extract_geo_phenotypes(args.fname)
        print("Parse phenotypes")
        
    snps = rename_snps(snps, snp_map)
    print("Parsed SNPs")
    #snps contains DataFrame with SNP columns and sample rows

    group_method = method_map[args.group_method]

    groups = group_method(snps.columns.tolist(), *args.group_method_args)
    print("Generated Groups")

    subsets = subset_wrap(snps, groups, phenotypes, *args.subset_method_args)

    for group, subset in subsets.items():
        #call FSA here
        print(fsa_wrapper(subset, group))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Associate SNP pair interactions with phenotype.')

    class M():
        fname = '../myeloma/GSE66903_series_matrix.txt'
        ftype = 'GEO'
        pheno = 'phenos.txt'
        snp_id_label = 'SNP_ID'
        snpmap_file = '../myeloma/GPL6801-4019.txt'
        group_method = 'all'
        group_method_args = []
        subset_method_args = []

    args = M()
    main(args)