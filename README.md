# Thesis
This repository serves as the central hub for my thesis project focusing on implementing various operations using a Picar (Raspberry Pi-controlled car) integrated with Lidar and Camera functionalities. The project aims to explore the fusion of Lidar and Camera data for enhancing autonomous navigation and perception capabilities.

# Setup

## Conda

The command below will setup a conda environment with required packages.


```
git clone git@github.com:AnupamKshetri/Thesis.git
cd PiCarProject/PiCar
conda env create -f environment.yml
conda activate Lidar_cam
```

# Data collection
To collect the data from both the LiDAR and Camera, `collect_data.py` script is used.

```
python collect_data.py 
```
Once this script is run, by pressing the key "L" on the keyboard, it will capture the image from camera and point cloud data from LiDAR.


# Finding parameters
A script is written in the Jupyter notebook to estimate the precise parameters' value. There are two files:
1. find_param.ipynb: Used to find the precise value of parameters automatically using Bayesian estimation.
2. calibrate_param.ipynb: Used to evaluate the accuracy of the parameters' values determined by plotting the LiDAR data onto the image plane. 

# Testing live
The script `test_live.py` is used to check the calibration in real time.

```
python test_live.py
```