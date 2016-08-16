from collections import defaultdict

import pandas as pd


def find_clinvar_groups(clinvar_summary, assembly='GRCh37'):
    """
    Seperated ClinVar variants into groups based on their associated phenotype given a genome assembly id.

    :param clinvar_summary: Filename of variant_summary.txt from ClinVar FTP.
    :param assembly: ID of assembly from which to use SNPs. Current GRCh37 or GRCh38
    :return: Dictionary containing keys of each MedGen phenotype ID mapping to lists of SNP RS IDs
    """
    variants = pd.read_table(clinvar_summary)
    groups = defaultdict(list)
    for i, var in variants[variants.Assembly==assembly].iterrows():
        pheno_ids = {xr.split(':')[0]: xr.split(':')[1] for xr in var.PhenotypeIDs.split(',') if ':' in xr}
        if 'MedGen' in pheno_ids:
            groups[pheno_ids['MedGen']].append(var['RS# (dbSNP)'])
        else:
            groups[None].append(var['RS# (dbSNP)'])
    return groups
