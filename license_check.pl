#!/usr/bin/perl -w
# 
# license check: check the file license head
# Copyright Hake Huang 2010, Freescale Semiconductor Inc.
#
# The code contained herein is licensed under the GNU General Public
# License. You may obtain a copy of the GNU General Public License
# Version 2 or later at the following locations:
#
# http://www.opensource.org/licenses/gpl-license.html
# http://www.gnu.org/copyleft/gpl.html
use strict;
use File::Spec::Functions;

my $g_pattern="";
#report file 
my $rFile;
#summary file
my $sFile;
#current file name
my $cfile_name="";
my @marks = ();
my $file_cnt=0;

sub add_summary_head{
open($sFile, ">license_summary.html") || die "can not write report";
print $sFile "<head>\n";
print $sFile "<H2>The license_report summary</H2>";
print $sFile "</head>\n";
print $sFile "<body>\n";
}

sub add_summary_end
{
print $sFile "</body>\n";
close($sFile);
}

sub add_summary{
my ($id, $status) = @_ ;

if($status == 0)
{
print $sFile "<div>";
print $sFile "<font color=\"blue\"><a href=\"license_report.html#$id\">$cfile_name</a></font>";
print $sFile "</div>\n";
}else{
print $sFile "<div>";
print $sFile "<a href=\"license_report.html#$id\"><font color=\"red\">!!!!</font>$cfile_name</a>";
print $sFile "</div>\n";
}

}

sub add_report_head{
open($rFile, ">license_report.html") || die "can not write report";
print $rFile "<head>\n";
print $rFile "<H2>The license_report</H2>";
print $rFile "</head>\n";
print $rFile "<body>\n";
}

sub add_report_end
{
print $rFile "</body>\n";
close($rFile);
}

sub add_report{
my ($file_name, $status) = @_ ;
my $servity = 0;
my $cline = "";

$file_cnt++;

if( $file_name ne $cfile_name )
{
print $rFile "<div>";
print $rFile "<a name=\"$file_cnt\"><font color=\"blue\">$file_name</font></a>";
print $rFile "</div>\n";
$cfile_name = $file_name;
}

my $items = @marks;

if( $items == 0 )
{
$servity=1;
print $rFile "<div>";
  print $rFile "&nbsp;&nbsp;&nbsp;&nbsp <font color=\"red\" >$file_name has not license info </font>";
print $rFile "</div>\n";

}

if ( $status == -1)
{
$servity=1;
print $rFile "<div>";
  print $rFile "&nbsp;&nbsp;&nbsp;&nbsp <font color=\"red\" >can not open file $file_name </font>";
print $rFile "</div>\n";
}elsif( $status == -2)
{
$servity=1;
print $rFile "<div>";
  print $rFile "&nbsp;&nbsp;&nbsp;&nbsp <font color=\"red\" >properitary licnese found in $file_name </font>";
print $rFile "</div>\n";

}elsif( $status == -10)
{
$servity=1;
print $rFile "<div>";
  print $rFile "&nbsp;&nbsp;&nbsp;&nbsp <font color=\"red\" >binary file found in $file_name </font>";
print $rFile "</div>\n";
}elsif( $status == -11)
{
$servity=1;
print $rFile "<div>";
  print $rFile "&nbsp;&nbsp;&nbsp;&nbsp <font color=\"red\" >swap file found in $file_name </font>";
print $rFile "</div>\n";
}

while($cline=pop(@marks))
{
print $rFile "<div>";
  print $rFile "&nbsp;&nbsp;&nbsp;&nbsp $cline";
print $rFile "</div>\n";
}
add_summary($file_cnt,$servity);
}

#should be txt file
sub check_file_license{
my($file_name) = @_ ;
my $rt = 0;
my $line = "";
my $count=0;
my $hFile;

open($hFile,"<$file_name") or $rt=-1 ;

while(<$hFile>)
{
  $line = $_;
  $count++;
  $line = $count."   ".$line;
  if( $line =~ /GPL/i )
  {
   $rt++;
   push(@marks, $line);
   next;
  }
  if ( $line =~ /COPYRIGHT/i )
  {
     push(@marks, $line);
     next;
  }
  if ( $line =~ /LICENSE/i )
  {
   push(@marks, $line);
   next;
  }
  if ( $line =~ /PROPRIETARY/i )
  {
   $rt=-2;
   push(@marks, $line);
   next;
  } 
}
close($hFile);
add_report($file_name, $rt);
}

sub search_dir
{
     my ($dirpath)=@_;
		 my $rt = 0;
     die "Error: $dirpath not exsit\n" if !$dirpath;
     print "Starting search in $dirpath  ... \n";
     my @list_dirs=();
     if (-d $dirpath)
     {
         push @list_dirs,$dirpath;
     }
     while($dirpath=pop(@list_dirs))
     {
         opendir(my $hDir, $dirpath) || (print "Can not open $dirpath" && next);
         for my $file_index (readdir($hDir))
         {
             my $tmp=catfile($dirpath,$file_index);
             if (-d $tmp )
             {
							 if($file_index ne '.' && $file_index ne '..')
							 {
                 push(@list_dirs,$tmp);
								 $rt=0;
               }
             }else{
								if ( -T $tmp)
             		{
	          			if( $tmp =~ /\.swap/i )
		  						{
	            			push(@marks, $tmp);
		    						$rt=-11;
		    						add_report($tmp, $rt);
		  						}else{
                   search_file($tmp);
									}
             		}else{
	        				push(@marks, $tmp);
									$rt=-10;
									add_report($tmp, $rt);
	     			 		}
						 }
         }
     }
     add_report_end;
     add_summary_end;
}


sub search_file
{
     my ($filepath)=@_;
     if( -T "$filepath" )
     {
             print "$filepath \n";
	     &check_file_license($filepath);
     }
}


add_report_head;
add_summary_head;
search_dir($ARGV[0]);


