

import os 
import sys 
import matplotlib 
from collections import defaultdict 
import pickle 
matplotlib.use("Agg")
import matplotlib.pyplot as plt 


def cal_similarity(dat1, dat2):
	N1, s1 = get_info_for_one_file(dat1) 		 
	N2, s2 = get_info_for_one_file(dat2) 		 

	si = s1.intersection(s2)
	su = s1.union(s2)
	return len(si)/len(su), len(si)/len(s1), len(si)/len(s2)


def get_info_for_one_file(dat):
	s = set() 		# contain all the objects in dat 
	N = 0 			# number of total requests in dat 
	with open(dat) as ifile: 
		for line in ifile: 
			line_split = line.strip().split("\t")
			N += 1
			s.add(line_split[1])
			# print(line_split[1])
	return N, s


def get_info_for_one_file_dict(dat):
	s = defaultdict(int)	 		# contain all the objects->count in dat 
	N = 0 			# number of total requests in dat 
	with open(dat) as ifile: 
		for line in ifile: 
			line_split = line.strip().split("\t")
			N += 1
			s[line_split[1]] += 1 
	return N, s



def run(directory): 
	pickle_name = "similarity_score_{}.pickle".format(directory if directory != "./" else "")
	figname = "similarity_{}.png".format(directory if directory != "./" else "")

	sscores_intersection_in_union = []
	sscores_intersection_in_dat = []

	scanned_set = set()


	for f1 in os.listdir(directory): 
		for f2 in os.listdir(directory): 
			if f1 == f2 or (f1, f2) in scanned_set or (f2, f1) in scanned_set: 
				continue 
			scanned_set.add((f1, f2))
			s1, s2, s3 = cal_similarity("{}/{}".format(directory, f1), 
												"{}/{}".format(directory, f2))

			print("{}:\t{}:\t{:.2g} \t{:.2g} \t{:.2g}".format(f1, f2, s1, s2, s3))
			sscores_intersection_in_union.append(s1) 
			sscores_intersection_in_dat.extend([s2, s3]) 

			if os.path.exists(pickle_name): 
				os.remove(pickle_name)
			with open(pickle_name, "wb") as pickle_ofile:
				pickle.dump([sscores_intersection_in_union, sscores_intersection_in_dat], pickle_ofile) 

	plt.xlabel("similarity score")
	plt.ylabel("count")
	plt.title("similarity score between any two dat\npercent of intersection in union")
	plt.hist(sscores_intersection_in_union)
	plt.savefig("union_" + figname)
	plt.clf()

	plt.xlabel("similarity score")
	plt.ylabel("count")
	plt.title("similarity score between any two dat\npercent of intersection in dat")
	plt.hist(sscores_intersection_in_dat)
	plt.savefig("dat_" + figname)
	plt.clf()


def run2(directory, Ns=[10, 100, 1000, 10000]):
	""" pick the top N most popular obj, check how many dat have them  
	
	Arguments:
		directory {[type]} -- [description]
	""" 

	obj_dicts = []
	dict_all = defaultdict(int)


	for f in os.listdir(directory): 
		num, d = get_info_for_one_file_dict("{}/{}".format(directory, f))
		obj_dicts.append(d)
		for k, v in d.items(): 
			dict_all[k] += v 

	print("get dict ready")
	l = sorted(list(dict_all.items()), key=lambda x: x[1], reverse=True)
	
	count_list = []
	for N in Ns:
		for i in range(N):
			count = 0 
			obj, req_count = l[i]
			for dict_per_dat in obj_dicts: 
				if obj in dict_per_dat: 
					count += 1
			count_list.append((float)(count)/len(obj_dicts))
			# print("{}: \t{}: \t{}: \t{}".format(i, obj, req_count, count))

		plt.xlabel("percentage of dat has the top {} popular obj".format(N))
		plt.ylabel("count")
		# plt.title("similarity score between any two dat\npercent of intersection in union")
		plt.hist(count_list)
		figname = "top_" + str(N) + "_{}.png".format(directory if directory != "./" else "")
		plt.savefig(figname)
		plt.clf()






def run_all():
	for i in range(1, 9): 
		print("################# {} ################".format(i))
		run("{}".format(i)) 


def run2_all(): 
	for i in range(1, 9): 
		print("################# {} ################".format(i))
		run2("{}".format(i)) 




if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] != "all": 
			run2(sys.argv[1])
		else: 
			run2_all() 
	else: 
		run2("./")


