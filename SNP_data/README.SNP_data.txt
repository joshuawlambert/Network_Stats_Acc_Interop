##########################################################
##	Getting SNP information from SNP database	##
##########################################################

# Source: NCBI SNP database FTP site
# URL: ftp://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b147_GRCh38p2/database/organism_data/
# Number of entries in file: b147_SNPContigLocusId_107.bcp.gz
584335390
~0.6 T entries

# Number of unique SNP_ID-GeneID pairs
zcat b147_SNPContigLocusId_107.bcp.gz | cut -f 1,6 | sort | uniq > SNP_ID2GENEID.tsv
98579159	# 16.9% of 584335390
~100 M

# File SNP_ID2GENEID.tsv will be used for 'grouping' samples


##################################################################################
##	Using eutils to get 'function class' for SNP_IDs from SNP database	##
##################################################################################

# Dependency: eutils from NCBI
# Run install_eutils.sh to install

# SNP database has 27 distinct possible terms for 'function class'
# All 27 terms saved in file function_class.list
# Some 'function class' terms are redundant. List of terms may be reduced

# Run count_entries_4function_class.pl to get the number of entries for each one of the 27 'function class' terms ay SNP database
perl count_entries_4function_class.pl function_class.list > function_class.counting.tsv

# Create esearch shell script commands to download SNP_ID, "current" SNP_ID, GeneID, GeneName for each one of the 27 'function class' terms
# Some SNP_IDs may have be merged to a "current" SNP_ID
# Some SNPs may be within multiple genes.
# Some SNPs may have multiple associated 'functional class' terms.
perl create_esearch_commands_4function_class.pl function_class.list > esearch_commands.sh

# Run esearch commands in file esearch_commands.sh individually for each 'functional class' term and edit output file to link SNP_ID, "current" SNP_ID, GeneID, GeneName to corresponding 'functional class' term.
# Example for 'stop loss'
esearch -db snp -query "stop loss[Function Class] AND Homo sapiens[Organism]" | esummary | xtract -pattern DocumentSummary -element Id -element SNP_ID -block GENES -element GENE_ID -block GENES -element NAME > snp.stop_loss.info.tsv
# Message:
Retrying esummary, step 2: 
#
# 'stop loss' has 23436 entries, but only 6006 entries were downloaded. There is no error message, but we are not getting all data.
# The same happens for other terms. See file function_class.table.tsv
# Copy file function_class.counting.tsv as a different name and add number of SNPs with downloaded information (column: records downloaded).
# File saved as function_class.table.tsv












