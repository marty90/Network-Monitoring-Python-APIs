#!/usr/bin/perl
# crea un histogramma...
# Nuova versione Mon May  7 11:00:07 CEST 2001
# 
# bin= indice del bin
# range= punto iniziale del bin
# tot = numero totale contato in questo bin
# dist = probabilita' del bin (distribuzione)
# cum = cumulativa fino a quel punto (=somma delle dist precedenti)
# cum _deve_ arrivare a uno (ovvio...) altrimenti qualcosa non funziona.
# E' possibile usare  "auto" a min o/e max e verra' calcolato
# automaticamente il range minimo e massimo
# 


if($#ARGV!=4)
{
    printf("uso: make_histo.pl <file> <colonna> <min> <max> <bins>\n");
    
    exit(1);
}

$filename=$ARGV[0];
$param=$ARGV[1];
$min=$ARGV[2];
$max=$ARGV[3];
$bins=$ARGV[4];

if($max=~'auto')
{
   $max=-9999999;
   open(IN_file,$filename) or die ("can't open $filename\n");
   while (($line = <IN_file>)) {
        chomp ($line);
    if ($line !~ /#/)
    {
        @data = split(' ', $line);
        $dat=$data[$param-1];
        if($max<$dat)
        {
                $max=$dat;
        }
    }
   }
   close(IN_file);
}

if($min=~'auto')
{
   $min=99999999;
   open(IN_file,$filename) or die ("can't open $filename\n");
   while (($line = <IN_file>)) {
        chomp ($line);
    if ($line !~ /#/)
    {
        @data = split(' ', $line);
        $dat=$data[$param-1];
        if($min>$dat)
        {
                $min=$dat;
        }
    }
   }
   close(IN_file);
}

print "#making histogram $filename $param $min $max $bins\n";
for($i=0;$i<=$bins;$i++)
{
        $tot[$i]=0;
}
#$total++;

$step=($max-$min)/$bins;
$totdat=0;
$totdat2=0;

open(IN_file,$filename) or die ("can't open $filename\n");
while (($line = <IN_file>)) {
        chomp ($line);
    if ($line !~ /#/)
    {
        @data = split(' ', $line);
#        if ($data[114] eq 'mail.google.com')
        {
        $dat=$data[$param-1];
		$totdat += $dat;
		$totdat2 += $dat*$dat;
        $index=int(($dat-$min)/$step);
        if($index<0)
        {
                $index=0;
        }
        if($index>$bins)
        {
                $index=$bins;
        }

        $tot[$index]++;        
        $total++;
     }
   }
}

$average = $totdat/$total;
$std = sqrt(($totdat2-$average*$average)/($average*$average));
print "#average= $average\t#std= $std\n";
$cumul=0;

printf "#bin\t range\ttot\tdist\tcum\n";
for($i=0;$i<=$bins;$i++)
{
        $range=$min+$i*$step;
	$cumul=$cumul + $tot[$i]/$total;
        printf "$i\t %.6f\t$tot[$i]\t%5.6f\t%7.6f\n",$range,$tot[$i]*100/$total, $cumul;
#        printf "$i $range $tot[$i] $tot[$i]*100/$total  $cumul\n";
}

