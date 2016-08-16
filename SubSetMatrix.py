import pandas
from collections import defaultdict


def generate_snp_acc_mapping(table_file):
    """
    Generates a mapping from SNP IDs from a platform to NCBI RS IDs. Based on one Affymetrix GEO dataset, may need
    further tweaking.

    :param table_file: Filename of table-sperated SNP info file
    :return: dictionary mapping platform IDs to RS IDs
    """
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
    """
    Pulls SNP variants for all samples in a GEO variant table file and applies standardized IDs from a mapping.
    Additionally removes any empty-string variants. (Affymetrix array mappings contain no RS ID for control SNPs)

    :param snp_table: Filename of tab-separated table containing SNPs for samples in GEO dataset.
    :param snp_map: Mapping of platform IDs to RS IDs for SNPs. (From generate_snp_acc_mapping()
    :return: Pandas dataframe containing rows representing each sample and columns representing each SNP. No Calls
    are represented by None objects
    """
    snps = pandas.read_table(snp_table, index_col=0).transpose()
    snps = snps.replace('No Call', None)
    snps.columns = [snp_map[c] for c in snps.columns]
    snps = snps.drop('', axis=1).head()
    return snps


def find_clinvar_groups(clinvar_summary, assembly='GRCh37'):
    """
    Seperated ClinVar variants into groups based on their associated phenotype given a genome assembly id.

    :param clinvar_summary: Filename of variant_summary.txt from ClinVar FTP.
    :param assembly: ID of assembly from which to use SNPs. Current GRCh37 or GRCh38
    :return: Dictionary containing keys of each MedGen phenotype ID mapping to lists of SNP RS IDs
    """
    variants = pandas.read_table(clinvar_summary)
    groups = defaultdict(list)
    for i, var in variants[variants.Assembly==assembly].iterrows():
        pheno_ids = {xr.split(':')[0]: xr.split(':')[1] for xr in var.PhenotypeIDs.split(',') if ':' in xr}
        if 'MedGen' in pheno_ids:
            groups[pheno_ids['MedGen']].append(var['RS# (dbSNP)'])
        else:
            groups[None].append(var['RS# (dbSNP)'])
    return groups