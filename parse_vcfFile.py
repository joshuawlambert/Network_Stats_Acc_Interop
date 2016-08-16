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