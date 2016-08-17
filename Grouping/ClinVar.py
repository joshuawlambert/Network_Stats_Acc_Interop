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
            groups[pheno_ids['MedGen']].append('rs' + str(var['RS# (dbSNP)']))
        else:
            groups[None].append('rs' + str(var['RS# (dbSNP)']))
    return groups # {C12345: [rs1234, rs1234], ...}

def generate_groups(snplist, clinvar_summary_file='/media/sf_ubuntuVbox/hackathon/clinvar_variant_summary.txt'):
    '''
    clinvar_summary_file is the absolute path to to the clinvar summary file (downloadable from...???)
    
    returns a list, snps that are in clinvar that are also in phenotype groups
    '''
    cv_groups = find_clinvar_groups(clinvar_summary_file)
    
    for k,v in cv_groups.items():
        cv_groups[k] = list(set(v).intersection(snplist))
        
    return cv_groups