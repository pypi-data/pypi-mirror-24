"""
boundary plot 
"""

from matplotlib import pyplot as plt 
from collections import defaultdict
import os, sys, glob 

LATENCY_ORI = 50 


def extract(dataName):
    result_dict = defaultdict(dict)
    for folder in glob.glob("*{}*".format(dataName)): 
        if os.path.isfile(folder):
            continue 
        print(folder)
        folder_split = folder.split(".")
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
                latency += float(line_split[0])
                avg_L1_HR += float(line_split[1])
                avg_L2_HR += float(line_split[2])
                traf_to_origin += float(line_split[3])
                traf_bet_layers += float(line_split[4]) 
        
        latency = latency / count 
        avg_L1_HR = avg_L1_HR / count
        avg_L2_HR = avg_L2_HR / count
        traf_to_origin = traf_to_origin / count
        traf_bet_layers = traf_bet_layers / count

        result_dict[size][boundary] = [latency, avg_L1_HR, avg_L2_HR, traf_to_origin, traf_bet_layers]
    return result_dict 


def save_result(d):
    for size, d_boundary in d.items():
        with open("{}".format(size), 'w') as ofile:
            for boundary, l in d_boundary.items(): 
                # print("{}\t{}".format(boundary, l))
                ofile.write("{}\t{}\n".format(boundary, "\t".join(l)))


def plot(d, figname):

    for cache_size, d_boundary in d.items():
        # l_boundary = [0] * len(d_boundary) 
        # l_latecy = [0] * len(d_boundary)  
        # l_L1_HR = [0] * len(d_boundary) 
        # l_L2_HR = [0] * len(d_boundary) 
        # l_traf_to_origin = [0] * len(d_boundary) 
        # l_traf_bet_layers = [0] * len(d_boundary) 
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

        plt.figure(4)
        plt.plot(l_boundary, l_latecy, marker="o", label="cache size {}".format(cache_size))
        # plt.ylim([0, LATENCY_ORI])
        plt.grid(True)
        # ylimit = plt.ylim()
        # plt.text(0.4, (ylimit[0]+ylimit[1])/2, "cache size {}".format(cache_size))
        plt.xlabel("Cache Size Boundary/L1 Percentage")
        plt.ylabel("Latency (ms)")
        plt.legend(ncol=2)
        plt.savefig("latency_{}_size{}.png".format(figname, cache_size))
        plt.clf()



        # latency
        plt.figure(1)
        plt.plot(l_boundary, l_latecy, marker="o", label="cache size {}".format(cache_size))
        plt.ylim([0, LATENCY_ORI])
        plt.grid(True)
        # ylimit = plt.ylim()
        # plt.text(0.4, (ylimit[0]+ylimit[1])/2, "cache size {}".format(cache_size))
        plt.xlabel("Cache Size Boundary/L1 Percentage")
        plt.ylabel("Latency (ms)")
        plt.legend(ncol=2)
        # plt.savefig("latency_{}_size{}.png".format(figname, cache_size))
        # plt.clf()

        plt.figure(2)
        plt.plot(l_boundary, l_traf_to_origin, marker="o", label="cache size {}".format(cache_size))
        plt.ylim([0, 1])
        plt.grid(True)
        # plt.text(0.4, 0.2, "cache size {}".format(cache_size))
        plt.xlabel("Cache Size Boundary/L1 Percentage")
        plt.ylabel("Traffic to Origin")
        plt.legend(ncol=2)
        # plt.savefig("traf_ori_{}_size{}.png".format(figname, cache_size))
        # plt.clf()
        #

        plt.figure(3)
        plt.plot(l_boundary, l_traf_bet_layers, marker="o", label="cache size {}".format(cache_size))
        plt.ylim([0, 1])
        plt.grid(True)
        # plt.text(0.4, 0.2, "cache size {}".format(cache_size))
        plt.xlabel("Cache Size Boundary/L1 Percentage")
        plt.ylabel("Traffic between Tiers")
        plt.legend(ncol=2)
        # plt.savefig("traf_tier_{}_size{}.png".format(figname, cache_size))
        # # plt.clf()

    # plt.figure(1)
    # plt.savefig("latency_{}.png".format(figname))
    # plt.figure(2)
    # plt.savefig("traf_ori_{}.png".format(figname))
    # plt.figure(3)
    # plt.savefig("traf_tier_{}.png".format(figname))



def run():
    d = extract(sys.argv[1])
    # save_result(d)
    plot(d, sys.argv[1])


if __name__ == "__main__":
    run() 
