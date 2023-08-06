# for f in `ls`; do echo $(pwd)/$f; done > trace.config; 


function run(){ 
	folder="akamaiData1"
	config=$1 
	size=$2
	echo "########################### $config $size $folder/log$config$size #################################"
	./akamaiSimulatorBin -c $config -s $size; cp ../bin/*.sh log && cd log && ./plot.sh && cd .. && mv log $folder/log$config$size; 
}



for size in 2000 20000 200000 2000000 20000000; do 
	for config in `ls trace*.config`; do 
		run $config $size 
	done 
done 


