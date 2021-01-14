# Scripts for NDM-1 peptide macrocycle inhibitor design and analysis
This repositiry includes the scripts used for Mulligan VK, Workman S, Sun T, Rettie S, Li X, Worrall LJ, Craven TW, King DT, Hosseinzadeh P, Watkins AM, Renfrew PD, Guffy S, Labonte JW, Moretti R, Bonneau R, Strynadka NCJ, and Baker D. (2020): Computationally-designed peptide macrocycle inhibitors of New Delhi metallo-beta-lactamase 1.  Manuscript under review.

## Contents

### Design RosettaScripts XML Scripts

Modernized design scripts compatible with the latest version of Rosetta are located in the following sub-directories:

* NDM1i-1_design_script/modernized/ -- Design script for NDM1i-1 designs, with syntax updated for the current version of Rosetta.
* NDM1i-3_design_script/modernized/ -- Design script for NDM1i-3, with syntax updated for the current version of Rosetta.
* NDM1i-4_design_script/original/ -- Design script used to produce NDM1i-4A through NDM1i-4G designs, which is already compatible with current versions of Rosetta.

Legacy versions of design scripts are also provided:

* NDM1i-1_design_script/original/ -- Design script used to produce NDM1i-1A through NDM1i-1G designs.  This script is for legacy Rosetta weekly build 2016.46, and will not work properly with current Rosetta versions.  It is intended only for exact reproduction of the protocol used with the version of the software that was used.
* NDM1i-3_design_script/original/ -- Design script used to produce NDM1i-3A through NDM1i-3D designs.  This script is for legacy Rosetta weekly build 2018.19, and will not work properly with current Rosetta versions.  It is intended only for exact reproduction of the protocol used with the version of the software that was used.

### Analysis RosettaScripts XML Scripts and Commandline Inputs

* The NDM1i-3D_biding_mode_comparison_script/ directory contains the protocol for computing the complex energy of the designed and experimentally-observed (inverted) binding modes of the NDM1i-3D peptide.  These scripts are compatible with current versions of Rosetta.
* The peptide_structure_prediction_example/ directory contains example inputs for running the **simple_cycpep_predict** application for a peptide sequence and structure to compute _PNear_.

### Analysis and Plotting Python Scripts

The NDM1i_experimental_data_analysis_Python_script/ directory contains Python scripts used for fitting _IC50_ data to the Hill equation.