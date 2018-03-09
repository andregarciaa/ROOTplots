#!/usr/bin/env python
# writen in Python, so look for command interpreter in this path

# Script which creates ROOT plots from a ROOT file. Modified for particular case of 
# charge distribution of 3D sensors from May 2017 SPS TB.

from os import listdir

#----------------------------------------------------------------------------

# First method (quite simple) from path, check there is a root file in the directory and 
# saves two strings with the type of the sensor and the run number (useful for plot titles or legends):

read_path():

    # list path content in a list:
    path_content = listdir(path_with_root_file) 

    # if no elements in the list contain "beam_analysis_cluster" in the name, the root file is not in 
    # the given directory
    check = 0 

    for thing in path_content:
        if("beam_analysis_cluster" in thing == "TRUE"): check=1 

    if(check == 0): raise IOError("\033[1;35mThe given directory does not contain the necessary ROOT file\033[1;m")

    read path_with_root_file
    # example of path_with_root_file: 
    # /eos/user/d/duarte/alibavas_data_root/N1-7_7e15_b2/run000391/
    #           391_2017-05-21_15-26_gerva_MBV3_N1-7_-200V_-31d2uA_-25C_lat132_beam_analysis_cluster.root

    sensor_type = substring of path_with_root_file after "data_root/"

    run_number = substring of path_with_root_file after "/run000"

    return sensor_type, run_number

#----------------------------------------------------------------------------

# 2nd method look for the branch name given by the user, checking the tree "alibava_clusters" inside the ROOT file:

plot_branch(path_with_root_file, branch_to_plot, sensor_type, run_number):

    # open ROOT loading the ROOT file:
    root -l path_with_root_file
    .ls
    check there is a tree called alibava_clusters
    # Plot the branch (like: cluster_calibrate_charge) with the nicest limits, colors, titles, etc:
    alibava_clusters.Draw(branch_to_plot)
    
    save to pdf


# Main method:
if __name__=='__main__':

    import ArgumentParser

    parser = program 'root_plots'

    # Positional arguments:
    path_with_root_file (Where root file is located and its name)
    # tree of the file which is going to be used is "alibava_clusters", but user has to say from which 
    # branch of this tree wants to have the plot.
    branch_to_plot (branch of alibava_clusters)

    # read inputs executing parser:
    args = parser
    path_with_root_file
    
    # read method outputs are the strings with the sensor name and run number:
    output: two strings
    sensor_type, run_number = read_path(path_with_root_file)

    # plot method opens the alibava_cluster tree and plots the required branch from it:
    # output: plot
    plot_branch(path_with_root_file, branch_to_plot, sensor_type, run_number)
