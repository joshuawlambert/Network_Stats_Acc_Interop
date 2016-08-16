import pandas


def read_vcf(filename):
    """
    Reads an input VCF file containing lines for each SNP and columns with genotype info for each sample.

    :param filename: Path to VCF file
    :return: Pandas DataFrame representing VCF file with columns as SNPs and rows with samples
    """
    vcf = open(filename)
    for l in vcf:
        if not l.startswith('##'):
            header = l.strip().split('\t')
            break
    snps = pandas.read_table(vcf, names=header)
    snps.index = snps.ID
    snps = snps.iloc[:,9:].T
    return snps

def parse_snps_geo(snp_table, bad_data='No Call'):
    """
    Pulls SNP variants for all samples in a GEO variant table file and applies standardized IDs from a mapping.
    Additionally removes any empty-string variants. (Affymetrix array mappings contain no RS ID for control SNPs)

    :param snp_table: Filename of tab-separated table containing SNPs for samples in GEO dataset.
    :param snp_map: Mapping of platform IDs to RS IDs for SNPs. (From generate_snp_acc_mapping()
    :return: Pandas dataframe containing rows representing each sample and columns representing each SNP. No Calls
    are represented by None objects
    """
    snps = pandas.read_table(snp_table, index_col=0, comment='!').T
    snps = snps.replace(bad_data, '')
    return snps


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


def rename_snps(snp_df, snp_map):
    """
    Applies a SNP ID mapping to a SNP DataMatrix

    :param snp_df: Parsed DataFrame containing SNPs (columns) for samples (rows)
    :param snp_map: Dictionary mapping column labels to new column labels (hopefully RS IDs)
    :return: DataFrame with renamed columns
    """
    snps = snp_df
    snps.columns = [snp_map[c] for c in snps.columns]
    snps = snps.drop('', axis=1).head()
    return snps


def read_phenotypes(pheno_file):
    with open(pheno_file) as ph:
        return [line.strip() for line in ph]