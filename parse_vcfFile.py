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

def parse_snps_geo(snp_table, snp_map, bad_data='No Call'):
    """
    Pulls SNP variants for all samples in a GEO variant table file and applies standardized IDs from a mapping.
    Additionally removes any empty-string variants. (Affymetrix array mappings contain no RS ID for control SNPs)

    :param snp_table: Filename of tab-separated table containing SNPs for samples in GEO dataset.
    :param snp_map: Mapping of platform IDs to RS IDs for SNPs. (From generate_snp_acc_mapping()
    :return: Pandas dataframe containing rows representing each sample and columns representing each SNP. No Calls
    are represented by None objects
    """
    snps = pandas.read_table(snp_table, index_col=0).T
    snps = snps.replace(bad_data, None)
    snps.columns = [snp_map[c] for c in snps.columns]
    snps = snps.drop('', axis=1).head()
    return snps