#!/usr/bin/Perl
use strict;
my $PF_INET=2;
my $SOCK_DGRAM=2;
my $port=2222;
my $proto=getprotobyname('udp');
my $data;
my $addres=pack('SnC4x8',$PF_INET,$port,127,0,0,1);
socket(SOCKET,$PF_INET,$SOCK_DGRAM,$proto) or die "Can't build a socket";
bind (SOCKET,$addres);
send (SOCKET,$ARGV[0],0,$addres) or die "send false";
recv (SOCKET,$data,200,0);
print "$data\n";
if ($data) {
send (SOCKET,"Test",0,$addres) ;
}