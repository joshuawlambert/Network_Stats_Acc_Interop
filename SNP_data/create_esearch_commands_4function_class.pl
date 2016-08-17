#!/usr/bin/env perl
use strict;
use warnings;

# Usage: perl create_esearch_commands_4function_class.pl $file > outputfile.sh
# $file: text file with 'function class' terms + filter to be used as query in esearch, one per line
# Example: perl create_esearch_commands_4function_class.pl function_class.list > esearch_commands.sh
my $file = shift @ARGV;

open (LIST,"<$file") || die "Cannot open file $file";

while (<LIST>) {
	chomp;
	
	my $class = $_;

	my $base_name = $class;
	$base_name =~ s/\s+/\_/g;

	my $cmd = "esearch -db snp -query \"$class\[Function Class\] AND Homo sapiens\[Organism\]\" | esummary | xtract -pattern DocumentSummary -element Id -element SNP_ID -block GENES -element GENE_ID -block GENES -element NAME > snp.$base_name.info.tsv";
	
	print "$cmd\n";

}

close LIST;






















