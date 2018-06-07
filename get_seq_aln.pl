#!/usr/bin/perl
sub distance{return sqrt((($_[0]-$_[3])**2)+(($_[1]-$_[4])**2)+(($_[2]-$_[5])**2));}

# define amino acids
my %AA = (ALA => 'A', ARG => 'R', ASN => 'N', ASP => 'D', CYS => 'C',
	GLU => 'E', GLN => 'Q', GLY => 'G', HIS => 'H', ILE => 'I',
	LEU => 'L', LYS => 'K', MET => 'M', PHE => 'F', PRO => 'P',
	SER => 'S', THR => 'T', TRP => 'W', TYR => 'Y', VAL => 'V');

# hash table for quick heavy atom lookup

sub SR{my $str = $_[0]; $str =~ s/ //g; return $str;}
sub isint{my $val = shift; return ($val =~ m/^\d+$/);}

my @ATOM;
my @LOOK;
my @SEQ;
my $n = 0;
while(exists $ARGV[$n])
{
	my $PDB = $ARGV[$n];
	open(PDB,$PDB) or die("'$PDB' pdb does not exist");
	while($line = <PDB>)
	{
		chomp($line);
		my $record = SR(substr($line,0,6));
		if($record eq "ATOM")
		{
			my $atom = SR(substr($line,12,4));
			my $resn = SR(substr($line,22,5));
			my $resi = $AA{substr($line,17,3)};
			my $c = substr($line,21,1);
			my $RESN = $c."_".$resn."_".$resi;

			my $x = SR(substr($line,30,8));
			my $y = SR(substr($line,38,8));
			my $z = SR(substr($line,46,8));
			if($atom eq "CA")
			{
				push(@{$LOOK[$n]},$RESN);
				$SEQ[$n] .= $resi;
				@{$ATOM[$n]{$RESN}} = ($x,$y,$z);
			}
		}
	}
	close(PDB);
	$n++;
}

my $n = 1;
while(exists $ARGV[$n])
{
	my %MTX;
	my $seq_i;
	my $p = 0;
	for my $i (@{$LOOK[0]})
	{
		my $q = 0;
		for my $j (@{$LOOK[$n]})
		{
			my $dist_ = get_dist(0,$i,$n,$j);
			$MTX[$p][$q] = $dist_;
			$q++;
		}
		$p++;
	}
	my ($seq_a, $seq_b) = NWalign($SEQ[0],$SEQ[$n],\@MTX); 
	print $seq_a."\n".$seq_b."\n";
	$n++;
}
sub get_dist
{
	my ($n,$i,$m,$j) = @_;
	my $dist = distance(@{$ATOM[$n]{$i}},@{$ATOM[$m]{$j}});
	return $dist;
}
sub NWalign
{
	# Needleman-WunschAlgorithm 
	my ($seq1, $seq2, $mtx) = @_;

	#print $seq1."\t".$seq2."\n";

	my $GAP= 0;

	# initialization
	my @matrix;
	$matrix[0][0]{score} = 0;
	$matrix[0][0]{pointer} = "none";
	for(my $j = 1; $j <= length($seq1); $j++)
	{
		$matrix[0][$j]{score} = $GAP * $j;
		$matrix[0][$j]{pointer} = "left";
	}
	for (my $i = 1; $i <= length($seq2); $i++)
	{
		$matrix[$i][0]{score} = $GAP * $i;
		$matrix[$i][0]{pointer} = "up";
	}

	# fill
	for(my $i = 1; $i <= length($seq2); $i++)
	{
		for(my $j = 1; $j <= length($seq1); $j++)
		{
			my ($diagonal_score, $left_score, $up_score);
			# calculate match score
			my $letter1 = substr($seq1, $j-1, 1);
			my $letter2 = substr($seq2, $i-1, 1);

			$diagonal_score = $matrix[$i-1][$j-1]{score} + (-1 * $$mtx[$j-1][$i-1]) + 5;

			# calculate gap scores
			$up_score = $matrix[$i-1][$j]{score} + $GAP;
			$left_score = $matrix[$i][$j-1]{score} + $GAP;

			# choose best score
			if ($diagonal_score >= $up_score)
			{
				if ($diagonal_score >= $left_score)
				{
					$matrix[$i][$j]{score} = $diagonal_score;
					$matrix[$i][$j]{pointer} = "diagonal";
				}
				else
				{
					$matrix[$i][$j]{score} = $left_score;
					$matrix[$i][$j]{pointer} = "left";
				}
			}
			else
			{
				if ($up_score >= $left_score)
				{
					$matrix[$i][$j]{score} = $up_score;
					$matrix[$i][$j]{pointer} = "up";
				}
				else
				{
					$matrix[$i][$j]{score} = $left_score;
					$matrix[$i][$j]{pointer} = "left";
				}
			}
		}
	}
	# trace-back
	my @align1;
	my @align2;

	# start at last cell of matrix
	my $j = length($seq1);
	my $i = length($seq2);

	my $sco = $matrix[$i][$j]{score};
	while (1)
	{
		last if $matrix[$i][$j]{pointer} eq "none"; # ends at first cell of matrix
		if ($matrix[$i][$j]{pointer} eq "diagonal")
		{
			push(@align1,substr($seq1, $j-1, 1));
			push(@align2,substr($seq2, $i-1, 1));
			$i--;
			$j--;
		}
		elsif ($matrix[$i][$j]{pointer} eq "left")
		{
			push(@align1,substr($seq1, $j-1, 1));
			push(@align2,"-");
			$j--;
		}
		elsif ($matrix[$i][$j]{pointer} eq "up")
		{
			push(@align1,"-");
			push(@align2,substr($seq2, $i-1, 1));
			$i--;
		}
	}
	@align1 = reverse(@align1);
	@align2 = reverse(@align2);
	my $seq_a = "@align1"; $seq_a =~ s/ //g;
	my $seq_b = "@align2"; $seq_b =~ s/ //g;
	return($seq_a,$seq_b);
}
