function plot_comparison(){ 

	traceName=$1
	dat_static="/home/jason/pycharm/mimircache/CExtension/build/akamaiData3/$traceName/akamai_stat"
	dat_dynamic="/home/jason/pycharm/mimircache/CExtension/build_dynamic/akamaiData3/$traceName/akamai_stat"
	n_lines_static=$(wc -l $dat_static|awk '{print $1}')
	n_lines_dynamic=$(wc -l $dat_dynamic|awk '{print $1}')
	echo "$traceName n_lines1 $n_lines_static, n_lines2 $n_lines_dynamic"

	echo '
		my_font = "SVBasic Manual, 12"
		red_000 = "#F9B7B0"
		red_025 = "#F97A6D"
		red_050 = "#E62B17"
		red_075 = "#8F463F"
		red_100 = "#6D0D03"

		blue_000 = "#A9BDE6"
		blue_025 = "#7297E6"
		blue_050 = "#1D4599"
		blue_075 = "#2F3F60"
		blue_100 = "#031A49" 

		green_000 = "#A6EBB5"
		green_025 = "#67EB84"
		green_050 = "#11AD34"
		green_075 = "#2F6C3D"
		green_100 = "#025214"

		brown_000 = "#F9E0B0"
		brown_025 = "#F9C96D"
		brown_050 = "#E69F17"
		brown_075 = "#8F743F"
		brown_100 = "#6D4903"

		grid_color = "#d5e0c9"
		text_color = "#6a6a6a"



		# set default point size
		set pointsize 1.2

		# set the style for the set 1, 2, 3...
		set style line 1 linecolor rgbcolor blue_025 linewidth 2 pt 7
		set style line 2 linecolor rgbcolor green_025 linewidth 2 pt 5
		set style line 3 linecolor rgbcolor red_025 linewidth 2 pt 9
		set style line 4 linecolor rgbcolor brown_025 linewidth 2 pt 13
		set style line 5 linecolor rgbcolor blue_050 linewidth 2 pt 11
		set style line 6 linecolor rgbcolor green_050 linewidth 2 pt 7
		set style line 7 linecolor rgbcolor red_050 linewidth 2 pt 5
		set style line 8 linecolor rgbcolor brown_050 linewidth 2 pt 9
		set style line 9 linecolor rgbcolor blue_075 linewidth 2 pt 13
		set style line 10 linecolor rgbcolor green_075 linewidth 2 pt 11
		set style line 11 linecolor rgbcolor red_075 linewidth 2 pt 7
		set style line 12 linecolor rgbcolor brown_075 linewidth 2 pt 5
		set style line 13 linecolor rgbcolor blue_100 linewidth 2 pt 9
		set style line 14 linecolor rgbcolor green_100 linewidth 2 pt 13
		set style line 15 linecolor rgbcolor red_100 linewidth 2 pt 11
		set style line 16 linecolor rgbcolor brown_100 linewidth 2 pt 7
		set style line 17 linecolor rgbcolor "#224499" linewidth 2 pt 5

		# this is to use the user-defined styles we just defined.
		set style increment user

		# set the color and font of the text of the axis
		set xtics textcolor rgb text_color font my_font
		set ytics textcolor rgb text_color font my_font
		set ztics textcolor rgb text_color font my_font

		# set the color and font (and a default text) for the title and each axis
		set title "Latency" textcolor rgb text_color font my_font
		set xlabel "Time" textcolor rgb text_color font my_font
		set ylabel "Latency(ms)" textcolor rgb text_color font my_font

		# set the text color and font for the label
		set label textcolor rgb text_color font my_font

		# set the color and width of the axis border
		set border 31 lw 2 lc rgb text_color

		# set key options
		set key box enhanced 		# width 2 height 2 enhanced spacing 2		# outside 

		# set grid color
		set grid lc rgb grid_color



		# set yrange 15:25


		# set terminal postscript portrait enhanced color dashed lw 1 "DejaVuSans" 12
		# set output "temp.ps"

		set terminal png size 800,600 enhanced font my_font # "Helvetica,20"
		set output "'$traceName'.latency.png"


		set format x "%.0f%%" 
		set auto x 

		# set datafile separator ","

		
		# unset key 
		# set key bottom right
		# set samples 50
		set style data points

		plot "'$dat_static'" using ($0*100/'$n_lines_static'):1 w line title "static", \
		"'$dat_dynamic'" using ($0*100/'$n_lines_dynamic'):1 w line title "dynamic"



	' | gnuplot -persist- 

}

if [[ $1 == "runall" ]]; then 
	for configID in `seq 1 8`; do 
		for size in 2000 20000 200000 2000000; do
			for boundary in 0.001 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.999; do 
				plot_comparison logtrace$configID.$size.$boundary; 
			done 
		done 
	done 
else 
	plot_comparison $1 

	if [[ $(hostname) == *mathcs* ]] || [[ $(hostname) == *jason* ]]; then 
		sleep 0.2; 
		open latency.png 
		open traffic_to_origin.png 
		open traffic_between_layers.png 
	fi 
fi 