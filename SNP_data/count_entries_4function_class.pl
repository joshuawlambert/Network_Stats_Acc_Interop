#!/usr/bin/env perl
use strict;
use warnings;

# Usage: perl count_entries_4function_class.pl $file > outputfile.tsv
# $file: text file with 'function class' terms to be used as query in esearch, one per line
# Example: perl count_entries_4function_class.pl function_class.list > function_class.counting.tsv
my $file = shift @ARGV;

open (LIST,"<$file") || die "Cannot open file $file";

print "#Function Class Term\t# of Entries\n";
while (<LIST>) {
	chomp;
	my $cmd = "esearch -db snp -query \"$_ \[Function Class\]\"";
	
	my $res = `$cmd`;

	#print "$res\n";

	$_ =~ s/\[Function Class\]//;
	my $class = $_;

	if ($res =~ /<Count>(\d+?)<\/Count>/) {
		my $count = $1;
		print "$_\t$count\n";
	}


}

close LIST;






















