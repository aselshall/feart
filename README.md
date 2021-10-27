# Subset selection 
This repo contains the codes for the manuscript of "prescreening-based subset selection for improving predictions of Earth system models for regional environmental management of red tide." The folder `Subset_selection` contains two codes for processing the data and figures in the manuscript. Check the Jupyter notebook `DataVisualization_zos` for Figs. 1 and 2, and Jupyter notebook `SubsetSelection.ipynb` for Figs. 4-7. Interactive versions of these two notebooks are [c1.ipynb](https://colab.research.google.com/github/aselshall/feart/blob/main/i/c1.ipynb) and [c2.ipynb](https://colab.research.google.com/github/aselshall/feart/blob/main/i/c2.ipynb) respectively, which can be found under folder `i`. Using colab, the interactive notebooks can be executed by anyone, who has a web browser and Google. Thus, these interactive versions make the codes immediately reproducible and thus can be executed with different opitions along with reading the manuscript. 

The folder `Karenia_brevis_data_analysis` contains the codes for processing the Karenia brevis data.

The folder `zos_data_extraction` contains the codes for preprocessing zos data (sea surface height above geoid). These are mainly data crunching tasks such as hyber-slabing, and stacking using the netCDF Operators (NCO, http://nco.sourceforge.net/). This is followed by data extraction along 300 m Bathymetry (B300) in the study area. This is mainly to reduce the size of the Earth system models (ESMs) data and reanalysis data from 80 GB to about 10 MB for the ESMs data `zos_data_B300_ESMs43210.npy` and less than 1 MB for the reanalysis data `zos_data_B300_Reanalysis10_phy001_030_r1.csv`. These two files are used as input files for `SubsetSelection.ipynb` and its interactive version `c2.ipynb`.

