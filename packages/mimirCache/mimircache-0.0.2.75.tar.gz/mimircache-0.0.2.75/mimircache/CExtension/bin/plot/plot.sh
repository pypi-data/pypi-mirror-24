




function extractServer(){ 
	echo "time req hit OverallHR layer1Req layer1Hit layer1HR layer2Req layer2Hit layer2HR layer1Size layer2Size layer1SizePercentage" > $1.dat
	gawk -F '\t' '{print $1, $3, $4, $5, $8, $9, $10, $13, $14, $15, $7, $12, $7/($7+$12)}' $1 >> $1.dat
} 

function plotServer(){
	./plotServer.sh $1; 
}

function extractLayer(){ 
	# obtain number of servers 
	num_servers=$(head -n 1 $1 | cut -f 9 |gawk '{print NF}')
	echo -n "time req hit OverallHR " > $1.dat
	for i in `seq 0 $(($num_servers-1))`; do 
		echo -n "server$i " >> $1.dat; 
	done 
	echo "" >> $1.dat
	gawk -F '\t' '{print $1, $3, $5, $7, $9}' $1 >> $1.dat
} 

function plotLayer(){
	./plotLayer.sh $1; 
}

function plotAkamaiStat(){
	./plotAkamaiStat.sh $1; 
}


function plot(){ 
	rm server*.png server*.dat 2>/dev/null
	rm layer*.png layer*.dat 2>/dev/null 
	for f in `ls server*`; do 
		extractServer $f; 
		plotServer $f.dat; 
	done; 

	for f in `ls layer*`; do 
		extractLayer $f; 
		plotLayer $f.dat; 
	done; 
	rm *.dat

	if [ -e akamai_stat ]; then 
		plotAkamaiStat akamai_stat
	fi 
} 



plot 

