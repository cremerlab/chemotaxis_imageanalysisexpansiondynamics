# ct_imageanalysisexpansiondynamics
To analyze expansion and growth dynamics of fluorescently labeld cells expanding in soft-agar. File handling for Leica SP8 data export.

## Collect data
Collect timelapse data with a confocal microscope, taking z- and x-y scans. Ensure scans across the entire agar thickness, adjust intensity and detection settings such that full dynamical range is used but saturation at high bacterial densities (later in time) is prevented. Details of culturing and image aquisition are described our paper:

This script works with the raw data image export of the Leica SP8 software (Leica Application Suite X). Store output as tif, option raw-data.

## Run the script
Run imageanalysis_populationdynamics.py to do image analysis. Before running script the first time, adjust path settings (name of input data and output folders etc), see comments provided in the file. 
