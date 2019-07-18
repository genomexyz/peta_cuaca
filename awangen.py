#!/usr/bin/python

import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from PIL import Image
import matplotlib.patches as mpatches
from imread import imread, imsave

#setting
IR1file = 'nc/H08_B13_Indonesia_201702150000.nc'
IR2file = 'nc/H08_B15_Indonesia_201702150000.nc'
IR3file = 'nc/H08_B08_Indonesia_201702150000.nc'


# Algoritma

def findcbvar1(ir1, ir2):
	if np.shape(ir1) != np.shape(ir2):
		return None
	cbvar1 = np.zeros(np.shape(ir1))
	for i in range(len(cbvar1)):
		for j in range(len(cbvar1[0])):
			if ir1[i,j] - ir2[i,j] <= 1.:
				cbvar1[i,j] = 1.
	return cbvar1


f = Dataset(IR1file)
latitude = f.variables['latitude'][:]
longitude = f.variables['longitude'][:]
IR1 = f.variables['IR'][0,:,:]-273.15
f.close()

f = Dataset(IR2file)
IR2 = f.variables['I2'][0,:,:]-273.15
f.close()

cbmat = findcbvar1(IR1, IR2)

fotocbvar1 = np.zeros((len(IR1), len(IR1[0]), 4), dtype=np.uint8)
for i in range(len(cbmat)):
	for j in range(len(cbmat[0])):
		if cbmat[i,j] > 0:
			fotocbvar1[i,j,0] = 255
			fotocbvar1[i,j,1] = 0
			fotocbvar1[i,j,2] = 0
			fotocbvar1[i,j,3] = 255

imsave('foto/awan_cb_var1.png', fotocbvar1)
