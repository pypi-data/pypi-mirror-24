"""
boundary plot 
"""

from matplotlib import pyplot as plt 
from collections import defaultdict
import os, sys, glob 

LATENCY_ORI = 50 
L2_COPY=1


def extract(directory, dataName):
    result_dict = defaultdict(dict)
    for folder in glob.glob("{}/*{}*".format(directory, dataName)): 
        if os.path.isfile(folder):
            continue 

        folder_name = folder 
        if '/' in folder:
            folder_name = folder[folder.rfind("/")+1:]

        folder_split = folder_name.split(".")


        print("{} {} {}".format(folder, folder_name, folder_split))

        if folder_split[0] != dataName:
            raise RuntimeError("data not satisfied: {} != {}, folder {}".format(folder_split[0], dataName, folder))
        size = int(folder_split[1])
        boundary = float("0.{}".format(folder_split[3]))

        # get result 
        latency         =   -1 
        avg_L1_HR       =   0 
        avg_L2_HR       =   0 
        traf_to_origin  =   0 
        traf_bet_layers =   0 
        logname= "akamai_stat"
        if not os.path.exists("{}/{}".format(folder, logname)) or \
                os.path.getsize("{}/{}".format(folder, logname)) == 0:
            logname = "akamai_stat"
        
        count = 0 
        with open("{}/{}".format(folder, logname)) as ifile:
            for line in ifile: 
                line_split = line.split("\t")
                count += 1 
                # use avg 
                # latency += float(line_split[0])
                # avg_L1_HR += float(line_split[1])
                # avg_L2_HR += float(line_split[2])
                # traf_to_origin += float(line_split[3])
                # traf_bet_layers += float(line_split[4]) 

                # use last stat 
                latency = float(line_split[0])
                avg_L1_HR = float(line_split[1])
                avg_L2_HR = float(line_split[2])
                traf_to_origin = float(line_split[3])
                traf_bet_layers = float(line_split[4]) 
        
        # latency = latency / count 
        # avg_L1_HR = avg_L1_HR / count
        # avg_L2_HR = avg_L2_HR / count
        # traf_to_origin = traf_to_origin / count
        # traf_bet_layers = traf_bet_layers / count


        result_dict[size][boundary] = [latency, avg_L1_HR, avg_L2_HR, traf_to_origin, traf_bet_layers]
    return result_dict 


def save_result(d):
    for size, d_boundary in d.items():
        with open("{}".format(size), 'w') as ofile:
            for boundary, l in d_boundary.items(): 
                # print("{}\t{}".format(boundary, l))
                ofile.write("{}\t{}\n".format(boundary, "\t".join(l)))


def plot(d_static, d_dynamic, figname):

    cachesize_to_id_dict = {} 

    for d in [d_static, d_dynamic]: 
        for cache_size, d_boundary in d.items():
            l_boundary = []
            l_latecy = []
            l_L1_HR = []
            l_L2_HR = []
            l_traf_to_origin = []
            l_traf_bet_layers = []         
            for boundary, l in sorted(d_boundary.items(), key=lambda x: float(x[0])): 
                # print(boundary)
                l_boundary.append(boundary)
                l_latecy.append(l[0])
                l_L1_HR.append(l[1])
                l_L2_HR.append(l[2])
                l_traf_to_origin.append(l[3])
                l_traf_bet_layers.append(l[4])
            # print("\n\n\n")

            if cache_size not in cachesize_to_id_dict:
                fig_id = len(cachesize_to_id_dict) 
                cachesize_to_id_dict[cache_size] = fig_id 
            else: 
                fig_id = cachesize_to_id_dict[cache_size]

            plt.figure(fig_id)
            plt.plot(l_boundary, l_latecy, marker="o", label="static" if d==d_static else "dynamic") 
            # plt.ylim([0, LATENCY_ORI])
            # plt.text(0.4, (ylimit[0]+ylimit[1])/2, "cache size {}".format(cache_size))

    for cache_size, fig_id in cachesize_to_id_dict.items(): 
        plt.figure(fig_id)
        plt.grid(True)
        plt.xlabel("Cache Size Boundary/L1 Percentage")
        plt.ylabel("Latency (ms)")
        plt.legend(ncol=2)
        plt.savefig("boundaryPlot_{}_size{}_L2COPY{}.png".format(figname, cache_size, L2_COPY))
        plt.clf()




def run():
    d_static = extract(STATIC_PATH, sys.argv[1])
    d_dynamic = extract(DYNAMIC_PATH, sys.argv[1])
    # save_result(d)
    plot(d_static, d_dynamic, sys.argv[1])


def run_temp():
    i = 8
    d_static = extract("/home/jason/pycharm/mimircache/CExtension/build_sanity_check/0825_COPY{}_sanity_check_{}/3static".format(L2_COPY, i), "sanity")
    d_dynamic = extract("/home/jason/pycharm/mimircache/CExtension/build_sanity_check/0825_COPY{}_sanity_check_{}/dynamic".format(L2_COPY, i), "sanity")
    plot(d_static, d_dynamic, "sanity_{}".format(i))


def run_all(): 
    for i in range(3, 11):
        print("######################### {} ########################".format(i))
        d_static = extract("/home/jason/pycharm/mimircache/CExtension/build_sanity_check/0825_COPY{}_sanity_check_{}/static".format(L2_COPY, i), "sanity")
        d_dynamic = extract("/home/jason/pycharm/mimircache/CExtension/build_sanity_check/0825_COPY{}_sanity_check_{}/dynamic".format(L2_COPY, i), "sanity")
        plot(d_static, d_dynamic, "sanity_{}".format(i))


if __name__ == "__main__":
    # run() 
    # run_temp()
    run_all() 
