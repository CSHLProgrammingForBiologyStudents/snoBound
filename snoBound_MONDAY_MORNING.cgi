#!/usr/bin/perl -w
# file: snoBound.cgi

use strict;
use warnings;
use CGI ':standard';
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;
use File::Path;

###############################  
#Want to read a list of file names from a directory into an html dropbox down menu. This section prepares the list of names to be used later.
###############################  

my @pre_genome_array =  (`ls /home/aearl/public_html/cgi-bin/genomes`);
my @genome_array;

#print @genome_array;

foreach my $array_file (@pre_genome_array){
    chomp $array_file;
    push (@genome_array, $array_file);
    
}

#print @genome_array, scalar(@genome_array);


###############################
#HTML commands to set up front page. 
###############################

##Tells the file which css to use
print header;
print start_html (
    -title => 'SnoBound',
    -style => [
	 {-src => 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css' },
	 {-src => '../styles/style.css'}
	 ],
    -class => 'container'
    );

#
print qq|
<div class="jumbotron">
<div class = "container">
  <h1>snoBound<font size="-0.9"><sup>TM</sup></font></h1>
  <img src  = "https://33.media.tumblr.com/4ac8f3bb5bf7a953efadfd27dfbdb53b/tumblr_mijf49rE3w1ri960io1_500.gif">
  <p>We're in the business of snoRNA discovery</p>
  <p><a class="btn btn-primary btn-lg" href="http://www.huffingtonpost.com/2013/10/28/boostup-crowdfunding_n_4156491.html" role="button">INVEST NOW</a></p>
</div>
</div>
|; 

print #h1("We are in the business of snoRNA discovery"),
    start_form,
    "Please specify a file to be analyzed:",br,
    popup_menu(-name => 'genome', -values => \@genome_array),
    p,br,
    "Enter your fasta formatted sequence here:", br,
    textarea(-name => 'sequence', -rows =>10, -cols =>50),br,br,
    submit (-name => 'snoBound', -value => 'Submit'),br,
    end_form,
    hr;


if (param('snoBound')){
	if (param('sequence')) {
	    my $entered_seq = param('sequence');

	    if ($entered_seq =~ />(\S+)/){
		my ($file_name) = $entered_seq =~ />(\S+)/;
		my $pwd = "..";
		chomp $pwd;
		my $new_dir = $pwd . "/$file_name".time;
		mkdir($new_dir, 0777) or die "$!";
		`chmod 777 $new_dir`;

		my $fasta_file = $new_dir."/$file_name";

		open (my $fh, '>', $fasta_file) or die "can't open $fasta_file $!";
		print $fh $entered_seq;
		close $fh;


		my $gff_out = $new_dir."/sno_$file_name.gff";
		my $fasta_out = $new_dir."/sno_$file_name.fa";
	   
		system("/home/aearl/public_html/cgi-bin/snobound_scanner_FINAL.pl --input $fasta_file --outputg $gff_out --outputf $fasta_out");  

	   
		print 
		    h2("RESULTS"),
		    h6("download from links below"),
		    start_form,
		    h3(a ({href => "../$file_name/$gff_out"}, "Your snoRNA predictions in gff format are here! \n ")),
		    h3(a ({href => "../$file_name/$fasta_out"}, "Your snoRNA predictions in fasta format are here! \n ")),br,br,
		    
 		    hr,
		    h2("Is your snoRNA expressed?"),
		   
		    "Please upload your fastQ file to determine if your snoRNA is expressed:",filefield(-name=>'uploaded sequence'),br,
		    submit (-name => 'expressed', -value => 'Submit'),br,br, 
		    hr,
		    h2("RESULTS"),
                    h6("download from link below"),
		    h3(a ({href => "../snoBound.txt"},"The average RNAseq read coverage of your predicted snoRNAs is here! ")), br,
#		    "<pre>chrom   chromStart      chromEnd        Description     ReadCoverage
#random_chr      204     285     random_chr-204-285-Hu-28S-Am3836-1-22.42        1.02469135802469
#random_chr      770     901     random_chr-770-901-Hu-28S-Gm1555-1-21.79        2.6030534351145
#random_chr      1159    1263    random_chr-1159-1263-Hu-U2-Gm12-1-21.33 2.85576923076923
#random_chr      631     705     random_chr-631-705-Hu-28S-Gm3828-1-19.32        2.10810810810811
#random_chr      2071    2138    random_chr-2071-2138-Hu-28S-Am3599-1-12.15      0
#random_chr      1       50      test    5.79591836734694</pre>",
		    end_form,
		    hr;

          
	   } else{
		die "Not in fasta format! :( \n"; 
	    }
	} else {
	    my $file_name = param('genome');

	    my $pwd = "..";
	    chomp $pwd;
	    my $new_dir = $pwd . "/$file_name".time;
	    mkdir($new_dir, 0777) or die "$!";
	    `chmod 777 $new_dir`;
	    `cp /home/aearl/public_html/cgi-bin/genomes/$file_name $new_dir`;

	    my $fasta_file = $new_dir."/$file_name";
	    my $gff_out = $new_dir."/sno_$file_name.gff";
	    my $fasta_out = $new_dir."/sno_$file_name.fa";

	    system("/home/aearl/public_html/cgi-bin/snobound_scanner_FINAL.pl --input $fasta_file --outputg $gff_out --outputf $fasta_out");


	    print
		h2("RESULTS"),
		h6("download from links below"),
		start_form,
		h3(a ({href => "../$file_name/$gff_out"}, "Your snoRNA predictions in gff format are here! \n ")),
		h3(a ({href => "../$file_name/$fasta_out"}, "Your snoRNA predictions in fasta format are here! \n ")),br,br,

		hr,
		h2("Is your snoRNA expressed?"),
		
		"Please upload your fastQ file to determine if your snoRNA is expressed:",filefield(-name=>'uploaded sequence'),br,
		submit (-name => 'expressed', -value => 'Submit'),br,br,
		hr,
		h2("RESULTS"),
		h6("download from link below"),
		h3(a ({href => "../snoBound.txt"},"The average RNAseq read coverage of your predicted snoRNAs is here! ")), br,
		end_form,
		hr;
	}
}


print end_html;


