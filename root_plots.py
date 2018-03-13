#!/usr/bin/env python
# writen in Python, so look for command interpreter in this path

import os, glob

"""
Script which creates ROOT plots from a ROOT file. Modified for particular case of
charge distribution of 3D sensors from May 2017 SPS TB.

__author__ = "Andrea Garcia Alonso"
__copyright__ = "Copyright 2018"
__version__ = "1.0"
__email__ = "andrea.garcia.alonso@cern.ch"

"""

#----------------------------------------------------------------------------

# 1st method (quite simple) from path, check there is a root file in the directory and 
# saves 2 strings with the sensor type and the run number (useful for plot titles, legends):

read_path():

    # list all the "beam_analysis_cluster.root" files inside any folder of the given path:
    files = glob.glob('/eos/user/d/duarte/alibavas_data_root/**/*beam_analysis_cluster.root', recursive=True)
  
    # if list is empty, raise error:
    if(files == []): raise IOError("\033[1;35mThe given directory does not contain the necessary ROOT file/s\033[1;m")

    read path_with_root_file
    # example of path_with_root_file: 
    # /eos/user/d/duarte/alibavas_data_root/N1-7_7e15_b2/run000391/
    #   391_2017-05-21_15-26_gerva_MBV3_N1-7_-200V_-31d2uA_-25C_lat132_beam_analysis_cluster.root

    # substring of path_with_root_file containing the sensor type (spliting with "/": 7th place)
    sensor_type = path_with_root_file.split("/")[6]

    # substring of path_with_root_file after sensor type, removing "run000" from the begining:
    run_number = path_with_root_file.split("/")[7].replace("run000","")

    return sensor_type, run_number

#----------------------------------------------------------------------------

# 2nd method look for the branch name given by user, checking "alibava_clusters" tree inside ROOT file:

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
