#!/bin/bash 

OUTPUT_FOLDER="traceLength2/"

function calTimeSpan(){
	# calculate the timespan in days 
	trace=$1; 
	startTime=$(head -n 1 $trace|cut -f 1);
	endTime=$(tail -n 1 $trace|cut -f 1);
	t=$(echo "($endTime - $startTime)/3600/24" | bc -l)
	# using printf instead of echo because of rounding 
	printf "%.2f, %.0f\n" $t $t 
}

function cleanTrace(){
	# output 
	
	# calculate the timespan in days 
	trace=$1; 
	startTime=$(head -n 1 $trace|cut -f 1);
	endTime=$(tail -n 1 $trace|cut -f 1);
	t=$(echo "($endTime - $startTime)/3600/24" | bc -l)
	# using printf instead of echo because of rounding 
	tDay=$(printf "%.0f" $t)

	# output cleaned trace, 1. calibrate timestamp 
	for i in `seq 1 $tDay`; do 
		maxTime=$(($i*24*3600))
		output_file="$OUTPUT_FOLDER/$i/$trace"
		echo "####################### $output_file $maxTime ############################" 
		cat $trace | gawk -v ofile=$output_file -v sTime=$startTime -v maxTime=$maxTime -v OFS="\t" '{if ($1-sTime < maxTime) print $1-sTime, $6 > ofile}'
	done; 
}



# calTimeSpan "185.232.99.68.anon.1"
# cleanTrace "185.232.99.68.anon.1"
# cleanTrace "19.21.108.123.anon.1"
# calTimeSpan $1 
# exit 

for f in `ls -p *.anon* | grep -v /`; do 
	echo -n "$f: "; 
	# calTimeSpan $f; 
	cleanTrace $f; 
done
