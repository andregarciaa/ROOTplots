#!/usr/bin/env python
# writen in Python, so look for command interpreter in this path

import os, glob, os.path

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

def read_path(path_with_root_file):

    # list all "/eos/.../beam_analysis_cluster.root" file paths inside any folder of the given path:
    all_files = glob.glob(path_with_root_file+'/**/*beam_analysis_cluster.root', recursive=True)
  
    # if list is empty, raise error:
    if(all_files == []): raise IOError("\033[1;35mThe given directory does not contain the necessary ROOT file/s\033[1;m")

    # example of path_with_root_file:
    # /eos/user/d/duarte/alibavas_data_root
    # inside it, there will be:
    #   /N1-7_7e15_b2/run000391/
    #   391_2017-05-21_15-26_gerva_MBV3_N1-7_-200V_-31d2uA_-25C_lat132_beam_analysis_cluster.root

    # for each root file path, the sensor type and run number will be saved inside the following lists:
    sensor_type[], run_number[]

    # check each root file path and add the information to the two lists:
    for file in all_files:
        # substring of path_with_root_file containing the sensor type (spliting with "/": 7th place)
        sensor_types.append(file.split("/")[6])

        # substring of path_with_root_file after sensor type, removing "run000" from the begining:
        run_numbers.append(file.split("/")[7].replace("run000",""))

    return sensor_types, run_numbers

#----------------------------------------------------------------------------

# 2nd method look for the branch name given by user, checking "alibava_clusters" tree 
# inside all the ROOT files:

def check_branch(all_files, branch_to_plot):
    for element in all_files:
        # open ROOT loading the ROOT file:
        root -l element
        .ls
        # check there is a tree called alibava_clusters:
        if yes: continue
        if not: raise error: root file of element is not right

#----------------------------------------------------------------------------

# 3rd method creates a pdf with all the canvas:

def plot(all_files, sensor_types, run_numbers):
    for element in all_files, run_numbers, sensor_types:
        # Plot the branch (like: cluster_calibrate_charge) with the nicest limits, colors, titles, etc:
        alibava_clusters.Draw(branch_to_plot)
        Landau-Gauss fit
        Obtain fit values and add to legend
        add to pdf

#----------------------------------------------------------------------------

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
    
    # read method obtains sensor name and run number strings and root file paths list:
    # output: two strings and one list
    sensor_types, run_numbers, all_files = read_path(path_with_root_file)

    # check_branch method opens the alibava_cluster tree and looks for the required branch from it:
    # output: nothing if everything is correct
    check_branch(all_files, branch_to_plot)

    # plot method saves a pdf with all the canvas of the calibrated charge distribution:
    # output: plot
    plot(all_files, sensor_types, run_numbers)
