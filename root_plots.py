#!/usr/bin/env python
# writen in Python, so look for command interpreter in this path

import os
import glob
import os.path
import alibavaSkifftools.analysis_functions as an
import ROOT
from ROOT import *

"""
Script which creates ROOT plots from a ROOT file. Modified for particular case of
charge distribution of 3D sensors from May 2017 SPS TB.

__author__ = "Andrea Garcia Alonso"
__copyright__ = "Copyright 2018"
__version__ = "1.0"
__email__ = "andrea.garcia.alonso@cern.ch"

"""

#----------------------------------------------------------------------------

def read_path():

    """
    Method read_path() checks the path where the root files are stored and saves them all
    (including their full paths) in a list. Then, it goes down this list saving in a
    dictionary the sensors names related with all the runs of each one and the full path.
    Input: nothing
    Returns: dictionary relating sensor_name--run_number--full_path
    """

    # list all "/eos/.../beam_analysis_cluster.root" file paths in the known folders of the given path:
    all_paths = glob.glob('/eos/user/d/duarte/alibavas_data_root/*/*/*beam_analysis_cluster.root')  

    # Due to last line is hardcoded, if list is empty, raise the following error:
    if(all_paths == []): raise IOError("\033[1;35mYou are not in lxplus, so you cannot access to the \
    /eos/user/d/duarte/alibavas_data_root/ path, where the root files are looked for.\033[1;m")

    # example of path_with_root_file:
    # /eos/user/d/duarte/alibavas_data_root
    # inside it, there will be:
    #   /N1-7_7e15_b2/run000391/
    #   391_2017-05-21_15-26_gerva_MBV3_N1-7_-200V_-31d2uA_-25C_lat132_beam_analysis_cluster.root

    # Instantiate the big dictionary:
    sensor_run_path_dic = {}

    # Check each root file path and write the new information in the variables:
    for rootfile in all_paths:

        # obtain the name of the sensor for each rootfile in the directory:
        sensor_name = rootfile.split("/")[6]
        
        # In the directory there are also data from iLGAD, LGAD and REF, ignore:
        if(sensor_name == "LGAD7859W1H6_0_b1" or sensor_name == \
        "iLGAD8533W1K05T_0_b2" or sensor_name == "REF_0_b1"): 
            continue

        # If the information of the current kind of sensor hasn't been collected yet, create 
        # its own dictionary inside a new key of the big one:
        if not sensor_run_path_dic.has_key(sensor_name):
            # Instantiate a dictionary for each sensor:
            sensor_run_path_dic[sensor_name] = {}

        # get the run number from the path of each root file:
        run_number = rootfile.split("/")[7].replace("run000","")

        # Save the path of the root file for each sensor and run number:
        sensor_run_path_dic[sensor_name][run_number] = rootfile

    return sensor_run_path_dic

#----------------------------------------------------------------------------


def process(sensor_run_path_dic):
    """
    This method looks for the branch inside the "alibava_clusters" tree for all
    the ROOT files which have been stored in sensor_run_path_dic dictionary.
    Creates a pdf with all the canvas, doing a Landau-Gauss
    fit and computing the fit variables. MPVs are stored in a dictionary:
    input: sensor_run_path_dic dictionary.
    output: pdf with all the calibrated charge distribution plots and a dictionary
    with all the MPV of the Landau-Gauss fits for those distributions.

    """
    mpv_values = {}

    # Create canvas to later save the histograms in pdf document:
    canvas = TCanvas("canvas")

    for sensor in sensor_run_path_dic:
        for run in sensor_run_path_dic[sensor]:
            # Open ROOT file:
            root_file = ROOT.TFile(sensor_run_path_dic[sensor][run])
            # Get the "alibava_clusters" tree from the ROOT file:
            root_tree = root_file.Get("alibava_clusters")
            # Check if the required branck exists:
            if(hasattr(root_tree, "eventTime")=="False"): 
                raise RunTimeError("\033[1;mThere is no eventTime branch in the tree of \
                sensor {0} at run {1}.format(sensor, run)\033[1;m")
                
            # Obtain the time window and save in a list of 2 elements:
            time_window = an.get_time_window(root_tree,"eventTime")
            mint = float(time_window[0])
            maxt = float(time_window[1])
            cut = "{0} < eventTime && {1} > eventTime".format(mint,maxt)

            # Plot the calibrated charge distribution (branch), applying the time cuts:
            root_tree.Draw("cluster_calibrated_charge>>histo(200,-0.5, 80000.5)",cut)

            # Landau-Gauss fit
            histo = ROOT.gDirectory.Get("histo")
            # Construct a ROOT function from the python function for the fit:
            fun = ROOT.TF1("Landau-Gauss",an.landau_gaus,-0.5, 200.5,4)
            # Give an initial value to the parameters of the fit function:
            # MPV (Landau peak), width, area (entry number), Gauss sigma(noise)
            fun.SetParNames("MPV","Landau width","Total area","Gauss sigma")
            fun.SetParameter(0, histo.GetBinCenter(histo.GetMaximumBin()))
            fun.SetParameter(1, 30)
            fun.SetParameter(2, 13000)
            fun.SetParameter(3, 28)
            gStyle.SetOptFit(1111)
            # Plot and fit the range from 1000 to 60000:
            histo.Fit(fun,"","",1000,60000)

            # Save in ONE PDF document all the plots:
            canvas.SaveAs("Cluster_calibr_charge_distributions.pdf)",\
            ("Calibrated charge distribution for {0}").format(sensor_run_path_dic[sensor][run]))

            # Add MPV to mpv_values dictionary:
            if not mpv_values.has_key(sensor):
                # Instantiate a dictionary for each sensor:
                mpv_values[sensor] = {}
            # Save the MPV value for each sensor and run number:
            mpv_values[sensor][run] = fun.GetParName(0)

    return mpv_values


#----------------------------------------------------------------------------

# Main method:
if __name__=='__main__':

    # read method obtains sensor name and run number strings and root file paths list:
    # output: one dictionary
    sensor_run_path_dic = read_path()

    # plot method saves a pdf with all the canvas of the calibrated charge distributions and a 
    # dictionary containing sensor name, run number and MPV obtained. In order to do it, it opens 
    # the alibava_cluster tree and looks for the required branch from it.
    # outputs: 
    #    dictionary with the MPV fit values of each run and sensor
    #    pdf with the plots
    mpv_values = process(sensor_run_path_dic)
