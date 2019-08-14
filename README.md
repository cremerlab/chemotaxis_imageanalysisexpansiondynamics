# ct_imageanalysisexpansiondynamics
To analyze expansion and growth dynamics of fluorescently labeld cells expanding in soft-agar. Code implements 
file handling specifically for the Leica Microsystems Leica Application Suite and its data export option as raw tif.

We used this code to analyze images acquired with a Leica Microsystems SP8 confocal microscope. Method details and the biological context are provided in our  manuscript:
- J.Cremer, T.Honda, Y.Tang, J.Wong-Ng, M.Vergassola, T.Hwa. Chemotaxis as a navigation strategy to thrive in nutrient-replete environments

August 2019, Jonas Cremer and all coauthors.

## Required modules
Required modules include Numpy, SciPy, and PIL. This code was tested and run with Python 2.7.

## Collect data
Images were collected scanning samples in low-magnification, tile-scanning along one axes (x) and through the agar (z). Ensure scans across the entire agar thickness, adjust intensity and detection settings such that full dynamical range is used but saturation at high bacterial densities (later in time) is prevented. See our manuscript for detailed informations.

## Run the script
Run "imageanalysis_populationdynamics.py" to do image analysis. Before running script the first time, adjust path settings (name of input data and output folders etc), see comments provided in the file. 

