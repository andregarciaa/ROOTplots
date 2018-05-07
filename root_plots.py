#!/usr/bin/env python
# writen in Python, so look for command interpreter in this path

import os
import glob
import os.path
import alibavaSkifftools.analysis_functions as an
import ROOT
from ROOT import *
from sifca_utils.plotting import set_sifca_style
sifca_style=set_sifca_style(stat_off=False)
sifca_style.cd()  # esto quizas no es necesario, pero no hace danyo

"""
Script which creates a PDF file with the canvas of the calibrated charge 
distributions obtained from a path with several ROOT files. 
Two particular cases of charge distribution of 3D sensors can be selected 
through hardcoding: the six 3D sensors measured at May 2017 SPS Test Beam 
or only M1-5 and N1-3 from TB and RS of 2016 and 2017 (in order to compare 
them to study excessive collected charge by M1-5).

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
    - Input: nothing
    - Output: sensor_run_path_dic: dictionary relating sensor_name--run_number--full_path
    """

    # FOR ALL THE 3D SENSORS OF TB 2017:---------------------------------------------------------------
    #selection = 1
    # - list all "/eos/.../beam_analysis_cluster.root" file paths in the known folders of the given path:
    # all_paths = glob.glob('/eos/user/d/duarte/alibavas_data_root/*/*/*beam_analysis_cluster.root')  
    # - Due to last line is hardcoded, if list is empty, raise the following error (FOR /EOS/...):
    # if(all_paths == []): raise IOError("\033[1;35mYou are not in lxplus, so you cannot access the \
    # /eos/user/d/duarte/alibavas_data_root/ path, where the root files are looked for.\033[1;m")
    # - example of path_with_root_file:
    # /eos/user/d/duarte/alibavas_data_root
    # - inside it, there will be:
    #   /N1-7_7e15_b2/run000391/
    #   391_2017-05-21_15-26_gerva_MBV3_N1-7_-200V_-31d2uA_-25C_lat132_beam_analysis_cluster.root
    # ------------------------------------------------------------------------------------------------


    # FOR M1-5 AND N1-3 OF TB AND RS 2016 AND 2017-----------------------------------------------------
    selection = 2
    all_paths = glob.glob('/afs/cern.ch/user/a/agarciaa/workspace/private/TB-RS_problem_M1-5/*/*/*beam_analysis_cluster.root')
    # - Check with ONE file:
    #all_paths = ['/afs/cern.ch/user/a/agarciaa/workspace/private/TB-RS_problem_M1-5/resultsTB2017cern/M1-5/379_2017-05-21_00-20_gerva_MB2_M1-5_-30V_-92d8uA_-25C_lat132_beam_analysis_cluster.root']
    # - example of path_with_root_file:
    # /afs/cern.ch/user/a/agarciaa/workspace/private/TB-RS_problem_M1-5/resultsTB2017cern/M1-5/
    # 378_2017-05-20_23-25_gerva_MB2_M1-5_-30V_-91d3uA_-25C_lat132_beam_analysis_cluster.root
    # ------------------------------------------------------------------------------------------------

    # FOR M1-5 AND N1-3 OF TB 2017. ROOT files by Jordi-----------------------------------------------
    #selection = 3
    #all_paths1 = glob.glob('/eos/user/d/duarte/alibavas_data_root/M1-5_0_b2/*/*beam_analysis_cluster.root')
    #all_paths2 = glob.glob('/eos/user/d/duarte/alibavas_data_root/N1-3_0_b1/*/*beam_analysis_cluster.root')
    #all_paths = all_paths1 + all_paths2
    # - example of path_with_root_file:
    # /eos/user/d/duarte/alibavas_data_root/M1-5_0_b2/run000378/
    # 378_2017-05-20_23-25_gerva_MB2_M1-5_-30V_-91d3uA_-25C_lat132_beam_analysis_cluster.root
    #if(all_paths == []): raise IOError("\033[1;35mYou are not in lxplus, so you cannot access the \
    #/eos/user/d/duarte/alibavas_data_root/ path, where the root files are looked for.\033[1;m")
    # ------------------------------------------------------------------------------------------------

    # Instantiate the big dictionary:
    sensor_run_path_dic = {}

    # Check each root file path and write the new information in the variables:
    for rootfile in all_paths:

        # obtain the name of the sensor for each rootfile in the directory:

        if selection == 1:
            # FOR ALL THE 3D SENSORS OF TB 2017:--------------------------------------------
            sensor_name = rootfile.split("/")[6]
            # In the directory there are also data from iLGAD, LGAD and REF, ignore:
            if(sensor_name == "LGAD7859W1H6_0_b1" or sensor_name == \
"iLGAD8533W1K05T_0_b2" or sensor_name == "REF_0_b1"):
                continue
        elif selection == 2:
            # FOR M1-5 AND N1-3 OF TB AND RS 2016 AND 2017:---------------------------------
            sensor_name = rootfile.split("/")[10]
            # In the directory there are also folders which are not of M1-5 and N1-3, ignore:
            if sensor_name != "N1-3" and sensor_name != "M1-5":
                continue
        elif selection ==3:
            # FOR M1-5 AND N1-3 OF TB 2017 root files of Jordi-----------------------------
            sensor_name = rootfile.split("/")[6]

        # If the information of the current kind of sensor hasn't been collected yet, create 
        # its own dictionary inside a new key of the big one:
        if not sensor_run_path_dic.has_key(sensor_name):
            # Instantiate a dictionary for each sensor:
            sensor_run_path_dic[sensor_name] = {}

        # get the run number from the path of each root file:
        # FOR ALL THE 3D SENSORS OF TB 2017 and FOR M1-5 AND N1-3 OF TB 2017 root files of Jordi:
        if selection==1 or selection==3: run_number = rootfile.split("/")[7].replace("run000","")
        # FOR M1-5 AND N1-3 OF TB AND RS 2016 AND 2017:------------------------------------------
        if selection==2 : run_number = rootfile.split("/")[11].split("_")[0]

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
    - Input: sensor_run_path_dic: dictionary
    - Outputs: pdf file. All the fitted calibrated charge distribution plots
               mpv_values: dictionary. MPVs of the Landau-Gauss fits
    """

    correction = 1

    # Do you want to correct the calibration or gain factor by 1.075?? (uncomment:)
    # correction = 1.075

    ROOT.gROOT.SetBatch()
    mpv_values = {}

    # Create canvas to later save the histograms in pdf document:
    canvas = TCanvas("canvas")

    # Create PDF file which will contain all the plots:
    name_pdf = "Cluster_calibr_charge_distributions.pdf"
    canvas.Print(name_pdf+"(")

    for sensor,sensor_dict in sensor_run_path_dic.iteritems():
        for run,filename in sensor_dict.iteritems():
            # Open ROOT file:
            root_file = ROOT.TFile(filename)
            # Get the "alibava_clusters" tree from the ROOT file:
            root_tree = root_file.Get("alibava_clusters")
            root_tree.Show(0)

            # Check if the required branches exist and there is data:
            if not hasattr(root_tree, "eventTime"): 
                print "There is no eventTime branch in the alibava_clusters\
tree of sensor {0} at run {1}".format(sensor, run)
                print "File: {0}".format(filename)
                continue
            if not hasattr(root_tree, "cluster_calibrated_charge"):
                print "There is no cluster_calibrated_charge branch in \
the alibava_clusters tree of sensor {0} at run {1}".format(sensor, run)
                print "File: {0}".format(filename)
                continue                
            if root_tree.GetEntries()<2000:
                print "{0} has less than 2000 events!!".format(root_file)
                continue

            # Obtain the time window and save in a list of 2 elements:
            time_window = an.get_time_window(root_tree,"eventMasked == 0 && abs(common_mode) < 20")
            mint = float(time_window[0])
            maxt = float(time_window[1])
            cut = "{0} < eventTime && {1} > eventTime".format(mint,maxt)

            # Choose width and height of the stats box:
            gStyle.SetStatW(0.25)
            gStyle.SetStatH(0.20)
            gStyle.SetStatY(0.93)

            # Do not take into account clusters with a high common mode value:
            cut += " && abs(common_mode) < 20" 

            # Plot the calibrated charge distribution (branch), applying the time cuts:
            # CHANGE HERE THE VALUE OF THE CORRECTION (DIVISION) OR PUT 1 WHEN NO CORRECTION:
            root_tree.Draw("cluster_calibrated_charge/1>>Landau-Gauss(100,-0.5, 60000.5)",cut)

            # Landau-Gauss fit
            histo = ROOT.gDirectory.Get("Landau-Gauss")

            # Set axis titles and their sizes and positions:
            histo.GetXaxis().SetTitle("Q / electrons")
            histo.GetYaxis().SetTitle("entries")
            histo.GetXaxis().SetTitleSize(0.035)
            histo.GetYaxis().SetTitleSize(0.035)
            histo.GetXaxis().SetTitleOffset(1.6)
            histo.GetYaxis().SetTitleOffset(1.6)

            # Construct a ROOT function from the python function for the fit:
            fun = ROOT.TF1("Landau-Gauss",an.landau_gaus,5000,60000.5,4)

            # Give an initial value to the parameters of the fit function:
            # MPV (Landau peak), width, area (entry number), Gauss sigma(noise)

            fun.SetParNames("MPV","Landau width","Total area","Gauss sigma")
            fun.SetParameter(0, histo.GetBinCenter(histo.GetMaximumBin()))
            fun.SetParameter(1, 30)
            fun.SetParameter(2, 13000)
            fun.SetParameter(3, 28)
            gStyle.SetOptFit(1111)

            # depending on the root files, we can take from the name the measure (TB or RS and year) or 
            # put it in the case of Jordi's processed root files, they are ONLY TB2017 at the moment:
            if sensor_run_path_dic[sensor][run].split("/")[8]=="TB-RS_problem_M1-5": 
                measure = sensor_run_path_dic[sensor][run].split("/")[9].replace("results","")
            if sensor_run_path_dic[sensor][run].split("/")[4]=="duarte" and sensor_run_path_dic[sensor][run].split("/")[5]=="alibavas_data_root":
                measure = "TB2017"
            
            histo.SetTitle("{0} Sensor {1} run {2} Calibrated charge. {3} < \
time window < {4}".format(measure,sensor,run,mint,maxt))

            # Plot and fit the range with automatic range:
            if correction!=1:
                fit_range_min = histo.GetMaximumBin()-20000
                fit_range_max = histo.GetMaximumBin()+40000
                histo.Fit(fun,"","",fit_range_min,fit_range_max)
                histo.Draw()
            else:
                histo.Fit(fun,"","",7000,60000)
                histo.Draw()

            # Decide if the fit range by hand is good or not:
            if fun.GetChisquare()/fun.GetNDF()>2:
                histo.Fit(fun,"","",5000,60000)
                histo.Draw()

            # Add MPV value (peak)
            pt = TPaveText(.6, 0.4, 0.78, 0.48, "NDC")
            if correction==1:  
                pt = TPaveText(.6, 0.4, 0.78, 0.48, "NDC")
                pt.AddText("Peak: {0} ke".format("{0:.1f}".format(fun.GetParameter(0)/1000.0)))
            else:
                pt = TPaveText(.6, 0.4, 0.9, 0.48, "NDC")
                pt.AddText("Peak: {0} ke. Correction: {1}".format("{0:.1f}".format(fun.GetParameter(0)/1000.0),correction))
            pt.Draw()

            # Save one PDF document for all the generated plots:
            canvas.Print(name_pdf,"Title: {0} run {1} Calib charge.".format(sensor,run))

            # Add MPV to mpv_values dictionary:
            if not mpv_values.has_key(sensor):
                # Instantiate a dictionary for each sensor:
                mpv_values[sensor] = {}
            # Save the MPV value for each sensor and run number:
            mpv_values[sensor][run] = fun.GetParName(0)

    # When all the data has been checked, close the pdf file:
    canvas.Print(name_pdf+")")
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
