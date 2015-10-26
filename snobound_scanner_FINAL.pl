#!/usr/bin/perl
# script by: Hemant/Sara
# File: scans for snoRNAs using sliding window
use strict;
use warnings;
use Getopt::Long;
use String::Approx 'amatch';

my $in;
my $out1;
my $out2;

GetOptions('input=s'        => \$in,
           'outputf=s'       => \$out1,
           'outputg=s'       => \$out2
    );
my %hash;
my $header;

open (IN, '<', $in) or die "provide fasta file: $!\n";
open (OUT1, '>', $out1) or die "$!\n";
open (OUT2, '>', $out2) or die "$!\n";
while (my $line = <IN>){
   chomp $line;
   if ($line =~ /^>(\w+)/){
     $header = $1;
   }
   else{
    $hash{$header}{sequence} .= $line;
   }
   # foreach my $header (keys %hash){
   #   foreach $longseq(keys $hash => {$header}){
    #  print "$hash => {$header}=>{$longseq}";
     # }
   # }
}
foreach my $key (keys %hash){
 my $num;
 my $seq = $hash{$key}{sequence};
 for (my $i = 0; $i < length($seq); $i++){ 
    my $window = substr($seq, $i, 170); 
   if ($window =~ /((\w{4}).[AG]TGATG[ATGC].{30,140}CTGA(\w{4}))/i) {
   my $fiveprime = $2; 
    $fiveprime =~ tr/atgcATGC/tacgTACG/;
    my $revfive = reverse($fiveprime);
    my $compare = amatch($revfive, $3);
  #  my $compare = ($revfive cmp $3); 
      if ($compare == 1){
          my $begin = $i + $-[0];
          my $end   = $i + $+[0] - 1;
          $i = $end;
        # push (@{$hash{$key}{snoseq}}, $1);
          $num++;
          print OUT1 ">",$key, "snoRNA_","$num\n",uc($1),"\n";
#          print OUT1 ">$key","_snoRNA_","$num\n$1\n";
          print OUT2 "$key\tsnoBound\tsnoRD\t$begin\t$end\t.\t+\t.\tID=\"snoRD_$num\"; Name=\"snoRD_$num\"\n";
        }
   }
  else {
    next; # print "no match found\n";
  }
 }
}
__END__
