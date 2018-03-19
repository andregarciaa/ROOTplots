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

    # list all "/eos/.../beam_analysis_cluster.root" file paths in the known folders of the given path:
    all_paths = glob.glob('/eos/user/d/duarte/alibavas_data_root/*/*/*beam_analysis_cluster.root')  

    # if list is empty, raise error:
    if(all_paths == []): raise IOError("\033[1;35mThe given directory does not contain the necessary ROOT file/s\033[1;m")

    # example of path_with_root_file:
    # /eos/user/d/duarte/alibavas_data_root
    # inside it, there will be:
    #   /N1-7_7e15_b2/run000391/
    #   391_2017-05-21_15-26_gerva_MBV3_N1-7_-200V_-31d2uA_-25C_lat132_beam_analysis_cluster.root

    # for each root file path, the sensor type  will be saved in a variable overwriten in each 
    # iteration, but the run number will be saved in an array, overwritten when changing the 
    # type of sensor:
    run_numbers = []

    # check each root file path and write the new information in the variables:
    for file in all_paths:
        # If during the path reading we change to the following type of sensor, this means all the 
        # runs of a sensor have been read, so they can be saved inside the key "sensor_type" inside 
        # the dictionary "path_sensor_run_dic":
        if(sensor_type != file.split("/")[6] && sensor_type != ""):
            # Initialise again "run_numbers" list:
            run_numbers = []
           
            # The value of the path_sensor_run_dic dictionary for each sensor_type is all the runs
            saved until this moment for that sensor_type:
            path_sensor_run_dic = dict(sensor_type:run_path_dic[run_number])

        # substring of path_with_root_file containing the sensor type (spliting with "/": 7th place)
        sensor_type = file.split("/")[6]

        # substring of path_with_root_file after sensor type, removing "run000" from the begining:
        run_numbers = append(file.split("/")[7].replace("run000",""))

        # The following lines will add values to two dictionaries (one inside the other):
        # The first one relates run number with the path where it is located:
        run_path_dic = dict(run_number:file)

    return path_sensor_run_dic

#----------------------------------------------------------------------------

# 2nd method looks for the branch name given by user, checking "alibava_clusters" tree 
# inside all the ROOT files. Creates a pdf with all the canvas, doing a Landau-Gauss
# fit and computing the fit variables. MPVs are stored in a dictionary:

def process(all_paths, branch_to_plot, sensor_types, run_numbers):

    for element in all_paths, run_numbers, sensor_types:
        # open ROOT loading the ROOT file:
        root -l element
        .ls
        # check there is a tree called alibava_clusters:
        if yes: continue
        if not: Print("ERROR: root file of ", element," is not right")

	# open charge vs time and find time window
        min_time
	max_time

        # Plot the branch (like: cluster_calibrate_charge) applying the time window, 
        # with required limits, colors, titles, etc:
        alibava_clusters.Draw(branch_to_plot, "min_time<event_time && event_time<max_time",\
				nentries, firstentry = 101)
        Landau-Gauss fit
        Obtain fit values and add to legend
        add to pdf

    return mpv_values

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
    # output: one dictionary
    path_sensor_run_dic = read_path(path_with_root_file)

    # plot method saves a pdf with all the canvas of the calibrated charge distributions and a 
    # dictionary containing sensor name, run number and MPV obtained. In order to do it, it opens 
    # the alibava_cluster tree and looks for the required branch from it.
    # outputs: 
    #    dictionary with the MPV fit values of each run and sensor
    #    pdf with the plots
    mpv_values = process(branch_to_plot, paths_sensor_run_dic)
