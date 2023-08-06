#!/usr/bin/env python

#    TFCE_mediation TMI multimodality, multisurface multiple regression
#    Copyright (C) 2017  Tristram Lett

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import os
import numpy as np
import math
import argparse as ap
from time import time
import matplotlib.pyplot as plt

from tfce_mediation.cynumstats import resid_covars, tval_int
from tfce_mediation.tfce import CreateAdjSet
from tfce_mediation.tm_io import read_tm_filetype, write_tm_filetype, savemgh_v2, savenifti_v2
from tfce_mediation.pyfunc import save_ply, convert_redtoyellow, convert_bluetolightblue, convert_mpl_colormaps, calc_sobelz, convert_voxel


DESCRIPTION = "Multisurface multiple regression with TFCE and tmi formated neuroimaging files."

def calculate_tfce(merge_y, masking_array, pred_x, calcTFCE, vdensity, position_array, fullmask, perm_number = None, randomise = False, verbose = False, no_intercept = True, set_surf_count = None, print_interation = False):
	X = np.column_stack([np.ones(merge_y.shape[0]),pred_x])
	if randomise:
		np.random.seed(perm_number+int(float(str(time())[-6:])*100))
		X = X[np.random.permutation(range(merge_y.shape[0]))]
	k = len(X.T)
	invXX = np.linalg.inv(np.dot(X.T, X))
	tvals = tval_int(X, invXX, merge_y, merge_y.shape[0], k, merge_y.shape[1])
	if no_intercept:
		tvals = tvals[1:,:]
	tvals = tvals.astype(np.float32, order = "C")
	tfce_tvals = np.zeros_like(tvals).astype(np.float32, order = "C")
	neg_tfce_tvals = np.zeros_like(tvals).astype(np.float32, order = "C")

	for tstat_counter in range(tvals.shape[0]):
		tval_temp = np.zeros_like((fullmask)).astype(np.float32, order = "C")
		if tvals.shape[0] == 1:
			tval_temp[fullmask==1] = tvals[0]
		else:
			tval_temp[fullmask==1] = tvals[tstat_counter]
		tval_temp = tval_temp.astype(np.float32, order = "C")
		tfce_temp = np.zeros_like(tval_temp).astype(np.float32, order = "C")
		neg_tfce_temp = np.zeros_like(tval_temp).astype(np.float32, order = "C")
		calcTFCE.run(tval_temp, tfce_temp)
		calcTFCE.run((tval_temp*-1), neg_tfce_temp)
		tval_temp = tval_temp[fullmask==1]
		tfce_temp = tfce_temp[fullmask==1]
		neg_tfce_temp = neg_tfce_temp[fullmask==1]
#		position = 0
		for surf_count in range(len(masking_array)):
			start = position_array[surf_count]
			end = position_array[surf_count+1]
			if isinstance(vdensity, int): # check vdensity is a scalar
				tfce_tvals[tstat_counter,start:end] = (tfce_temp[start:end] * (tval_temp[start:end].max()/100) * vdensity)
				neg_tfce_tvals[tstat_counter,start:end] = (neg_tfce_temp[start:end] * ((tval_temp*-1)[start:end].max()/100) * vdensity)
			else:
				tfce_tvals[tstat_counter,start:end] = (tfce_temp[start:end] * (tval_temp[start:end].max()/100) * vdensity[start:end])
				neg_tfce_tvals[tstat_counter,start:end] = (neg_tfce_temp[start:end] * ((tval_temp*-1)[start:end].max()/100) * vdensity[start:end])
			if randomise:
				if set_surf_count is not None:
					os.system("echo %f >> perm_maxTFCE_surf%d_tcon%d.csv" % (np.nanmax(tfce_tvals[tstat_counter,start:end]),int(set_surf_count[surf_count]),tstat_counter+1))
					os.system("echo %f >> perm_maxTFCE_surf%d_tcon%d.csv" % (np.nanmax(neg_tfce_tvals[tstat_counter,start:end]),int(set_surf_count[surf_count]),tstat_counter+1))
				else:
					os.system("echo %f >> perm_maxTFCE_surf%d_tcon%d.csv" % (np.nanmax(tfce_tvals[tstat_counter,start:end]),surf_count,tstat_counter+1))
					os.system("echo %f >> perm_maxTFCE_surf%d_tcon%d.csv" % (np.nanmax(neg_tfce_tvals[tstat_counter,start:end]),surf_count,tstat_counter+1))
			else:
				if set_surf_count is not None:
					print "Maximum (untransformed) postive tfce value for surface %s, tcon %d: %f" % (int(set_surf_count[surf_count]),tstat_counter+1,np.nanmax(tfce_tvals[tstat_counter,start:end])) 
					print "Maximum (untransformed) negative tfce value for surface %s, tcon %d: %f" % (int(set_surf_count[surf_count]),tstat_counter+1,np.nanmax(neg_tfce_tvals[tstat_counter,start:end]))
				else:
					print "Maximum (untransformed) postive tfce value for surface %s, tcon %d: %f" % (surf_count,tstat_counter+1,np.nanmax(tfce_tvals[tstat_counter,start:end])) 
					print "Maximum (untransformed) negative tfce value for surface %s, tcon %d: %f" % (surf_count,tstat_counter+1,np.nanmax(neg_tfce_tvals[tstat_counter,start:end]))
		if verbose:
			print "T-contrast: %d" % tstat_counter
			print "Max tfce from all surfaces = %f" % tfce_tvals[tstat_counter].max()
			print "Max negative tfce from all surfaces = %f" % neg_tfce_tvals[tstat_counter].max()
	if randomise:
		if print_interation:
			print "Interation number: %d" % perm_number
#		os.system("echo %s >> perm_maxTFCE_allsurf.csv" % ( ','.join(["%0.2f" % i for i in tfce_tvals.max(axis=1)] )) )
#		os.system("echo %s >> perm_maxTFCE_allsurf.csv" % ( ','.join(["%0.2f" % i for i in neg_tfce_tvals.max(axis=1)] )) )
		tvals = None
		tfce_tvals = None
		neg_tfce_tvals = None
	tval_temp = None
	tfce_temp = None
	neg_tfce_temp = None
	del calcTFCE
	if not randomise:
		return (tvals.astype(np.float32, order = "C"), tfce_tvals.astype(np.float32, order = "C"), neg_tfce_tvals.astype(np.float32, order = "C"))

def calculate_mediation_tfce(medtype, merge_y, masking_array, pred_x, depend_y, calcTFCE, vdensity, position_array, fullmask, perm_number = None, randomise = False, verbose = False, no_intercept = True):
	n = len(pred_x)
	if randomise:
		np.random.seed(perm_number+int(float(str(time())[-6:])*100))
		indices_perm = np.random.permutation(range(merge_y.shape[0]))
	if (medtype == 'M') or (medtype == 'I'):
		if randomise:
			pathA_nx = pred_x[indices_perm]
	else:
		if randomise:
			pathA_nx = pred_x[indices_perm]
			pathB_nx = depend_y[indices_perm]
	SobelZ = calc_sobelz(medtype, pred_x, depend_y, merge_y, merge_y.shape[0], merge_y.shape[1])
	SobelZ = SobelZ.astype(np.float32, order = "C")
	tfce_SobelZ = np.zeros_like(SobelZ).astype(np.float32, order = "C")
	zval_temp = np.zeros_like((fullmask)).astype(np.float32, order = "C")
	zval_temp[fullmask==1] = SobelZ
	zval_temp = zval_temp.astype(np.float32, order = "C")
	tfce_temp = np.zeros_like(zval_temp).astype(np.float32, order = "C")
	calcTFCE.run(zval_temp, tfce_temp)
	zval_temp = zval_temp[fullmask==1]
	tfce_temp = tfce_temp[fullmask==1]
	for surf_count in range(len(masking_array)):
		start = position_array[surf_count]
		end = position_array[surf_count+1]
		tfce_SobelZ[:,start:end] = (tfce_temp[start:end] * (zval_temp[start:end].max()/100) * vdensity[start:end])
		if randomise:
			os.system("echo %f >> perm_maxTFCE_surf%d_zstat.csv" % (np.nanmax(tfce_SobelZ[:,start:end]),surf_count))
	if verbose:
		print "Max Zstat tfce from all surfaces = %f" % tfce_SobelZ.max()
	if randomise:
		print "Interation number: %d" % perm_number
		os.system("echo %s >> perm_maxTFCE_allsurf_zstat.csv" % ( ','.join(["%0.2f" % i for i in tfce_SobelZ.max(axis=1)] )) )
		SobelZ = None
		tfce_SobelZ = None
	zval_temp = None
	tfce_temp = None
	del calcTFCE
	if not randomise:
		return (SobelZ.astype(np.float32, order = "C"), tfce_SobelZ.astype(np.float32, order = "C"))

#find nearest permuted TFCE max value that corresponse to family-wise error rate 
def find_nearest(array,value,p_array):
	idx = np.searchsorted(array, value, side="left")
	if idx == len(p_array):
		return p_array[idx-1]
	elif math.fabs(value - array[idx-1]) < math.fabs(value - array[idx]):
		return p_array[idx-1]
	else:
		return p_array[idx]

def paint_surface(lowthresh, highthres, color_scheme, data_array, save_colorbar = True):
	colormaps = np.array(plt.colormaps(),dtype=np.str)
	if (str(color_scheme) == 'r_y') or (str(color_scheme) == 'red-yellow'):
		out_color_array = convert_redtoyellow(np.array((float(lowthresh),float(highthres))), data_array, save_colorbar = save_colorbar)
	elif (str(color_scheme) == 'b_lb') or (str(color_scheme) == 'blue-lightblue'):
		out_color_array = convert_bluetolightblue(np.array((float(lowthresh),float(highthres))), data_array, save_colorbar = save_colorbar)
	elif np.any(colormaps == str(color_scheme)):
		out_color_array = convert_mpl_colormaps(np.array((float(lowthresh),float(highthres))), data_array, str(color_scheme), save_colorbar = save_colorbar)
	else:
		print "Error: colour scheme %s does not exist" % str(color_scheme)
		quit()
	return out_color_array

def strip_basename(basename):
	if basename.endswith('.mgh'):
		basename = basename[:-4]
	elif basename.endswith('.nii.gz'):
		basename = basename[:-7]
	else:
		pass
	if basename.startswith('lh.all'):
		basename = 'lh.%s' % basename[7:]
	if basename.startswith('rh.all'):
		basename = 'rh.%s' % basename[7:]
	return basename

def merge_adjacency_array(adjacent_range, adjacency_array):
	v_count = 0
	if len(adjacent_range) == 1:
		adjacency = np.copy(adjacency_array[0])
		for i in range(len(adjacency)):
			adjacency[i] = np.array(list(adjacency[i])).tolist() # list fixes 'set' 'int' error
	else:
		for e in adjacent_range:
			if v_count == 0:
				adjacency = np.copy(adjacency_array[0])
				for i in range(len(adjacency)):
					adjacency[i] = np.array(list(adjacency[i])).tolist() # list fixes 'set' 'int' error
				v_count += len(adjacency_array[e])
			else:
				temp_adjacency = np.copy(adjacency_array[e])
				for i in range(len(adjacency_array[e])):
					temp_adjacency[i] = np.add(list(temp_adjacency[i]), v_count).tolist() # list fixes 'set' 'int' error
				adjacency = np.hstack((adjacency, temp_adjacency))
				v_count += len(adjacency_array[e])
	return adjacency

def lowest_length(num_contrasts, surface_range, tmifilename):
	lengths = []
	for contrast in range(num_contrasts):
		for surface in surface_range: # the standardization is done within each surface
			lengths.append(np.array(np.genfromtxt('output_%s/perm_maxTFCE_surf%d_tcon%d.csv' % (tmifilename,surface,contrast+1)).shape[0]))
	return np.array(lengths).min()

def saveauto(image_array, index, imagename, affine=None):
	if index.shape[2] > 1:
		savenifti_v2(image_array,index, imagename, affine)
	else:
		savemgh_v2(image_array,index, imagename, affine)

def apply_mfwer(image_array, num_contrasts, surface_range, num_perm, num_surf, tminame, position_array, pos_range, neg_range, method = 'scale', weight = None): # weight = None is essentially Tippet without considering mask size

	maxvalue_array = np.zeros((num_perm,num_contrasts))
	temp_max = np.zeros((num_perm, num_surf))
	positive_data = np.zeros((image_array[0].shape[0],num_contrasts))
	negative_data = np.zeros((image_array[0].shape[0],num_contrasts))

	if weight == 'logmasksize':
		x = []
		for i in range(len(position_array)-1):
			x.append((position_array[i+1] - position_array[i]))
		weights = (np.log(x)/np.log(x).sum())/np.mean(np.log(x)/np.log(x).sum()) # weights between mask size and max values probablity.
		w_temp_max = np.zeros((num_perm, num_surf))

	for contrast in range(num_contrasts):
		for surface in surface_range: # the standardization is done within each surface
			log_perm_results = np.log(np.genfromtxt('output_%s/perm_maxTFCE_surf%d_tcon%d.csv' % (tminame,surface,contrast+1))[:num_perm])
			# set log(0) back to zero (only happens with small masks and very large effect sizes)
			log_perm_results[np.isinf(log_perm_results)] = 0
			start = position_array[surface]
			end = position_array[surface+1]

			# log transform, standarization
			posvmask = np.log(image_array[0][start:end,pos_range[contrast]]) > 0
			temp_lt = np.log(image_array[0][start:end,pos_range[contrast]][posvmask]) # log and z transform the images by the permutation values (the max tfce values are left skewed)
			temp_lt -= log_perm_results.mean()
			temp_lt /= log_perm_results.std()
			temp_lt += 10
			positive_data[start:end,contrast][posvmask] = temp_lt
			del temp_lt, posvmask

			posvmask = np.log(image_array[0][start:end,neg_range[contrast]]) > 0
			temp_lt = np.log(image_array[0][start:end,neg_range[contrast]][posvmask]) # log and z transform the images by the permutation values (the max tfce values are left skewed)
			temp_lt -= log_perm_results.mean()
			temp_lt /= log_perm_results.std()
			temp_lt += 10
			negative_data[start:end,contrast][posvmask] = temp_lt
			del temp_lt, posvmask

			log_perm_results -= log_perm_results.mean() # standardize the max TFCE values 
			log_perm_results /= log_perm_results.std()
			if weight == 'logmasksize':
				w_log_perm_results = log_perm_results * weights[surface]
				w_log_perm_results += 10
				w_temp_max[:,surface] = w_log_perm_results
			log_perm_results += 10
			temp_max[:,surface] = log_perm_results


		if not weight == None:
			w_temp_max[np.isnan(w_temp_max)]=0
			max_index = np.argmax(w_temp_max, axis=1)
			max_value_list = np.zeros((len(max_index)),dtype=np.float32) # this should not be necessary
			for i in range(len(temp_max)):
				max_value_list[i]= temp_max[i,max_index[i]]
			maxvalue_array[:,contrast] = np.sort(max_value_list)
			del max_value_list
		else:
			maxvalue_array[:,contrast] = np.sort(temp_max.max(axis=1))
	del temp_max
	# two for loops just so my brain doesn't explode
	for contrast in range(num_contrasts):
		sorted_perm_tfce_max=maxvalue_array[:,contrast]
		p_array=np.zeros_like(sorted_perm_tfce_max)
		corrp_img = np.zeros((positive_data.shape[0]))
		for j in xrange(num_perm):
			p_array[j] = np.true_divide(j,num_perm)
		cV=0
		for k in positive_data[:,contrast]:
			corrp_img[cV] = find_nearest(sorted_perm_tfce_max,k,p_array)
			cV+=1
		positive_data[:,contrast] = np.copy(corrp_img)
		cV=0
		corrp_img = np.zeros((negative_data.shape[0]))
		for k in negative_data[:,contrast]:
			corrp_img[cV] = find_nearest(sorted_perm_tfce_max,k,p_array)
			cV+=1
		negative_data[:,contrast] = np.copy(corrp_img)

	return positive_data, negative_data

def create_position_array(masking_array):
	pointer = 0
	position_array = [0]
	for i in range(len(masking_array)):
		pointer += len(masking_array[i][masking_array[i]==True])
		position_array.append(pointer)
	return position_array

def create_full_mask(masking_array):
	# make mega mask
	fullmask = []
	for i in range(len(masking_array)):
		if masking_array[i].shape[2] == 1: # check if vertex or voxel image
			fullmask = np.hstack((fullmask, masking_array[i][:,0,0]))
		else:
			fullmask = np.hstack((fullmask, masking_array[i][masking_array[i]==True]))
	return fullmask

def calc_mixed_tfce(assigntfcesettings, merge_y, masking_array, position_array, vdensity, pred_x, calcTFCE, perm_number = None, randomise = False, medtype = None, depend_y = None):
	for i in np.unique(assigntfcesettings):
		data_mask = np.zeros(merge_y.shape[1], dtype=bool)
		extract_range = np.argwhere(assigntfcesettings==i)
		for surface in extract_range:
			start = position_array[int(surface)]
			end = position_array[int(surface)+1]
			data_mask[start:end] = True
		subset_merge_y = merge_y[:,data_mask]
		try:
			temp_vdensity = vdensity[data_mask]
		except:
			temp_vdensity = 1

		if randomise:
			
			if i == 0:
				display_iter = True
			else:
				display_iter = False

			calculate_tfce(subset_merge_y, 
				np.array(masking_array)[assigntfcesettings==i], 
				pred_x, 
				calcTFCE[i], 
				temp_vdensity, 
				create_position_array(np.array(masking_array)[assigntfcesettings==i]),
				create_full_mask(np.array(masking_array)[assigntfcesettings==i]),
				set_surf_count = extract_range,
				perm_number=perm_number, 
				randomise = True,
				print_interation = display_iter)
		else:
			temp_tvals, temp_tfce_tvals, temp_neg_tfce_tvals = calculate_tfce(subset_merge_y, 
				np.array(masking_array)[assigntfcesettings==i], 
				pred_x, 
				calcTFCE[i], 
				temp_vdensity, 
				create_position_array(np.array(masking_array)[assigntfcesettings==i]),
				create_full_mask(np.array(masking_array)[assigntfcesettings==i]),
				set_surf_count = extract_range)

			if i == 0: # at first instance
				tvals = tfce_tvals = neg_tfce_tvals = np.zeros((temp_tvals.shape[0],merge_y.shape[1]))
			tvals[:,data_mask] = temp_tvals
			tfce_tvals[:,data_mask] = temp_tfce_tvals
			neg_tfce_tvals[:,data_mask] = temp_neg_tfce_tvals
			temp_tvals = None
			temp_tfce_tvals = None
			temp_neg_tfce_tvals = None
	if not randomise:
		return tvals, tfce_tvals, neg_tfce_tvals


def getArgumentParser(ap = ap.ArgumentParser(description = DESCRIPTION)):

	ap.add_argument("-i_tmi", "--tmifile",
		help="Input the *.tmi file for analysis.", 
		nargs=1,
		metavar=('*.tmi'),
		required=True)

	group = ap.add_mutually_exclusive_group(required=True)
	group.add_argument("-i", "--input", 
		nargs=2, 
		help="[Predictor(s)] [Covariate(s)]", 
		metavar=('*.csv', '*.csv'))
	group.add_argument("-r", "--regressors", 
		nargs=1, help="Single step regression", 
		metavar=('*.csv'))
	group.add_argument("-mfwe","--multisurfacefwecorrection", 
		help="Input the stats tmi using -i_tmi *.tmi. The corrected files will be appended to the stats tmi. Note, the intercepts will be ignored.",
		action='store_true')
	ap.add_argument("-m", "--mediation",
		nargs=2, help="Perform a mediation analysis. The type of mediation {I,M,Y} and dependent variable must be inputted.", 
		metavar=('{I,M,Y}','*.csv'))
	ap.add_argument("-p", "--randomise", 
		help="Specify the range of permutations. e.g, -p 1 200", 
		nargs=2,
		type=int,
		metavar=['INT'])
	ap.add_argument("-i_name", "--analysisname",
		help="Input the *.tmi file for analysis.", 
		nargs=1)
	ap.add_argument("--tfce", 
		help="TFCE settings. H (i.e., height raised to power H), E (i.e., extent raised to power E). Default: %(default)s). H=2, E=2/3 is the point at which the cummulative density function is approximately Gaussian distributed.", 
		nargs='+', 
		default=[2.0,0.67],
		type=float,
		metavar=('H', 'E'))
	ap.add_argument("-sa", "--setadjacencyobjs",
		help="Specify the adjaceny object to use for each mask. The number of inputs must match the number of masks in the tmi file. Note, the objects start at zero. e.g., -sa 0 1 0 1",
		nargs='+',
		type=int,
		metavar=('INT'))
	ap.add_argument("-st", "--assigntfcesettings",
		help="Specify the tfce H and E settings for each mask. -st is useful for combined analysis do voxel and vertex data. More than one set of values must inputted with --tfce. The number of inputs must match the number of masks in the tmi file. The input corresponds to each pair of --tfce setting starting at zero. e.g., -st 0 0 0 0 1 1",
		nargs='+',
		type=int,
		metavar=('INT'))
	ap.add_argument("--noweight", 
		help="Do not weight each vertex for density of vertices within the specified geodesic distance (not recommended).", 
		action="store_true")
	ap.add_argument("--outtype", 
		help="Specify the output file type", 
		nargs='+', 
		default=['tmi'], 
		choices=('tmi', 'mgh', 'nii.gz', 'auto'))
	ap.add_argument("-c","--concatestats", 
		help="Concantenate FWE corrected p statistic images to the stats file. Must be used with -mfwe option", 
		action="store_true")
	ap.add_argument("-l","--neglog", 
		help="Output negative log(10) pFWE corrected images (useful for visualizing effect sizes).", 
		action="store_true")
	ap.add_argument("-op", "--outputply",
		help="Projects pFWE corrected for negative and positive TFCE transformed t-statistics onto a ply mesh for visualization of results using a 3D viewer. Must be used with -mfwe option. The sigificance threshold (low and high), and either: red-yellow (r_y), blue-lightblue (b_lb) or any matplotlib colorschemes (https://matplotlib.org/examples/color/colormaps_reference.html). Note, thresholds must be postive. e.g., -op 0.95 1 r_y b_lb", 
		nargs=4, 
		metavar=('float','float', 'colormap', 'colormap'))
	correctionoptions = ap.add_mutually_exclusive_group(required=False)
	correctionoptions.add_argument("-ss","--setsurface", 
		help="Must be used with -mfwe option. Input the set of surfaces to create pFWE corrected images using a range. Family-wise error rate correction will only applied to the specified surfaces. e.g., -ss 0 1 5 6", 
		nargs='+',
		type=int,
		metavar=('INT'))
	correctionoptions.add_argument("-ssr","--setsurfacerange", 
		help="Must be used with -mfwe option. Input a range to set the surfaces to create pFWE corrected images using a range. Family-wise error rate correction will only applied to the specified surfaces. e.g., -ssr 0 3", 
		nargs=2,
		type=int,
		metavar=('INT'))

	return ap

def run(opts):
	currentTime=int(time())

#############################
###### FWER CORRECTION ######
#############################
	if opts.multisurfacefwecorrection:
		_, image_array, masking_array, maskname, affine_array, vertex_array, face_array, surfname, adjacency_array, tmi_history, subjectids = read_tm_filetype('%s' % opts.tmifile[0], verbose=False)

		# check file dimensions
		if not image_array[0].shape[1] % 3 == 0:
			print 'Print file format is not understood. Please make sure %s is statistics file.' % opts.tmifile[0]
			quit()
		else:
			num_contrasts = int(image_array[0].shape[1] / 3)

		# get surface coordinates in data array
		position_array = create_position_array(masking_array)

		if num_contrasts == 1:
			# get lists for positive and negative contrasts
			pos_range = [1]
			neg_range = [2]
		else:
			# get lists for positive and negative contrasts
			pos_range = range(num_contrasts, num_contrasts+num_contrasts)
			neg_range = range(num_contrasts*2, num_contrasts*2+num_contrasts)

		# check that randomisation has been run
		if not os.path.exists("%s/output_%s/perm_maxTFCE_surf0_tcon1.csv" % (os.getcwd(),opts.tmifile[0])): # make this safer
			print 'Permutation folder not found. Please run --randomise first.'
			quit()

		#check permutation file lengths
		num_surf = len(masking_array)
		surface_range = range(num_surf)
		num_perm = lowest_length(num_contrasts, surface_range, opts.tmifile[0])

		if opts.setsurfacerange:
			surface_range = range(opts.setsurfacerange[0], opts.setsurfacerange[1]+1)
		elif opts.setsurface:
			surface_range = opts.setsurface
		if np.array(surface_range).max() > len(masking_array):
			print "Error: range does note fit the surfaces contained in the tmi file. %s contains the following surfaces" % opts.tmifile[0]
			for i in range(len(surfname)):
				print ("Surface %d : %s, %s" % (i,surfname[i], maskname[i]))
			quit()
		print "Reading %d contrast(s) from %d of %d surface(s)" % ((num_contrasts),len(surface_range), num_surf)
		print "Reading %s permutations with an accuracy of p=0.05+/-%.4f" % (num_perm,(2*(np.sqrt(0.05*0.95/num_perm))))

		# calculate the P(FWER) images from all surfaces
		positive_data, negative_data = apply_mfwer(image_array, num_contrasts, surface_range, num_perm, num_surf, opts.tmifile[0], position_array, pos_range, neg_range, weight='logmasksize')

		# write out files
		if opts.concatestats: 
			write_tm_filetype(opts.tmifile[0],
				image_array = positive_data,
				masking_array = masking_array,
				maskname = maskname,
				affine_array = affine_array,
				vertex_array = vertex_array,
				face_array = face_array,
				surfname = surfname,
				adjacency_array = adjacency_array,
				checkname = False,
				tmi_history = tmi_history)
			_, image_array, masking_array, maskname, affine_array, vertex_array, face_array, surfname, adjacency_array, tmi_history, subjectids = read_tm_filetype(opts.tmifile[0], verbose=False)
			write_tm_filetype(opts.tmifile[0],
				image_array = np.column_stack((image_array[0],negative_data)),
				masking_array = masking_array,
				maskname = maskname,
				affine_array = affine_array,
				vertex_array = vertex_array,
				face_array = face_array,
				surfname = surfname,
				adjacency_array = adjacency_array,
				checkname = False,
				tmi_history = tmi_history)
		else:
			for i in range(len(opts.outtype)):
				if opts.outtype[i] == 'tmi':
					write_tm_filetype("tstats_pFWER_%s" % opts.tmifile[0],
						image_array = positive_data,
						masking_array = masking_array,
						maskname = maskname,
						affine_array = affine_array,
						vertex_array = vertex_array,
						face_array = face_array,
						surfname = surfname,
						checkname = False,
						tmi_history = tmi_history)
					write_tm_filetype("negtstats_pFWER_%s" % opts.tmifile[0],
						image_array = negative_data,
						masking_array = masking_array,
						maskname = maskname,
						affine_array = affine_array,
						vertex_array = vertex_array,
						face_array = face_array,
						surfname = surfname,
						checkname = False,
						tmi_history = tmi_history)
					if opts.neglog:
						write_tm_filetype("tstats_negLog_pFWER_%s" % opts.tmifile[0],
							image_array = -np.log10(1-positive_data),
							masking_array = masking_array,
							maskname = maskname,
							affine_array = affine_array,
							vertex_array = vertex_array,
							face_array = face_array,
							surfname = surfname,
							checkname = False,
							tmi_history = tmi_history)
						write_tm_filetype("negtstats_negLog_pFWER_%s" % opts.tmifile[0],
							image_array = -np.log10(1-negative_data),
							masking_array=masking_array,
							maskname=maskname,
							affine_array=affine_array,
							vertex_array=vertex_array,
							face_array=face_array,
							surfname=surfname,
							checkname=False,
							tmi_history=tmi_history)
				else:
					if opts.outtype[i] == 'mgh':
						savefunc = savemgh_v2
					if opts.outtype[i] == 'nii.gz':
						savefunc = savenifti_v2
					if opts.outtype[i] == 'auto':
						savefunc = saveauto
					for surf_count in surface_range:
						start = position_array[surf_count]
						end = position_array[surf_count+1]
						basename = strip_basename(maskname[surf_count])
						if not os.path.exists("output_stats"):
							os.mkdir("output_stats")
						out_image = positive_data[start:end]
						temp_image = negative_data[start:end]
						for contrast in range(num_contrasts):
							out_image[temp_image[:, contrast] != 0,contrast] = temp_image[temp_image[:, contrast] != 0,contrast] * -1
						if affine_array == []:
							savefunc(out_image,masking_array[surf_count], "output_stats/%d_%s_pFWER" % (surf_count, basename))
						else:
							savefunc(out_image,masking_array[surf_count], "output_stats/%d_%s_pFWER" % (surf_count, basename), affine_array[surf_count])
						if opts.neglog:
							out_image = -np.log10(1-positive_data[start:end,contrast])
							temp_image = np.log10(1-negative_data[start:end,contrast])
							for contrast in range(num_contrasts):
								out_image[temp_image[:, contrast] != 0,contrast] = temp_image[temp_image[:, contrast] != 0,contrast]
							if affine_array == []:
								savefunc(out_image,masking_array[surf_count], "output_stats/%d_%s_negLog_pFWER" % (surf_count, basename))
							else:
								savefunc(out_image,masking_array[surf_count], "output_stats/%d_%s_negLog_pFWER" % (surf_count, basename), affine_array[surf_count])
		if opts.outputply:
			colorbar = True
			if not os.path.exists("output_ply"):
				os.mkdir("output_ply")
			for contrast in range(num_contrasts):
				for surf_count in surface_range:
					start = position_array[surf_count]
					end = position_array[surf_count+1]
					basename = strip_basename(maskname[surf_count])
					if masking_array[surf_count].shape[2] > 1:
						img_data = np.zeros((masking_array[surf_count].shape))
						combined_data = positive_data[start:end,contrast]
						combined_data[combined_data<=0] = negative_data[start:end,contrast][combined_data<=0] * -1
						combined_data[np.abs(combined_data)<float(opts.outputply[0])] = 0
						img_data[masking_array[surf_count]] = combined_data
						v, f, values = convert_voxel(img_data, affine = affine_array[surf_count], absthreshold = float(opts.outputply[0]))
						if not v == []:
							out_color_array = paint_surface(opts.outputply[0], opts.outputply[1], opts.outputply[2], values, save_colorbar=colorbar)
							negvalues = values * -1
							index = negvalues > float(opts.outputply[0])
							out_color_array2 = paint_surface(opts.outputply[0], opts.outputply[1], opts.outputply[3], negvalues, save_colorbar=colorbar)
							out_color_array[index,:] = out_color_array2[index,:]
							save_ply(v,f, "output_ply/%d_%s_pFWE_tcon%d.ply" % (surf_count, basename, contrast+1), out_color_array)
							colorbar = False
						else:
							print "No output for %d %s T-contrast %d" % (surf_count, basename, contrast+1)
					else:
						img_data = np.zeros((masking_array[surf_count].shape[0]))
						img_data[masking_array[surf_count][:,0,0]==True] = positive_data[start:end,contrast]
						out_color_array = paint_surface(opts.outputply[0], opts.outputply[1], opts.outputply[2], img_data, save_colorbar=colorbar)
						img_data[masking_array[surf_count][:,0,0]==True] = negative_data[start:end,contrast]
						index = img_data > float(opts.outputply[0])
						out_color_array2 = paint_surface(opts.outputply[0], opts.outputply[1], opts.outputply[3], img_data, save_colorbar=colorbar)
						out_color_array[index,:] = out_color_array2[index,:]
						save_ply(vertex_array[surf_count],face_array[surf_count], "output_ply/%d_%s_pFWE_tcon%d.ply" % (surf_count, basename, contrast+1), out_color_array)
						colorbar = False
	else:

##################################
###### STATISTICAL ANALYSIS ######
##################################
		# read tmi file
		if opts.randomise:
			_, image_array, masking_array, _, _, _, _, _, adjacency_array, _, _  = read_tm_filetype(opts.tmifile[0])
			_ = None
		else: 
			element, image_array, masking_array, maskname, affine_array, vertex_array, face_array, surfname, adjacency_array, tmi_history, _  = read_tm_filetype(opts.tmifile[0])
		# get surface coordinates in data array
		position_array = create_position_array(masking_array)

		if opts.setadjacencyobjs:
			if len(opts.setadjacencyobjs) == len(masking_array):
				adjacent_range = np.array(opts.setadjacencyobjs, dtype = np.int)
			else:
				print "Error: # of masking arrays (%d) must and list of matching adjacency (%d) must be equal." % (len(masking_array), len(opts.setadjacencyobjs))
				quit()
		else: 
			adjacent_range = range(len(adjacency_array))
		calcTFCE = []
		if opts.assigntfcesettings:
			if not len(opts.assigntfcesettings) == len(masking_array):
				print "Error: # of masking arrays (%d) must and list of matching tfce setting (%d) must be equal." % (len(masking_array), len(opts.assigntfcesettings))
				quit()
			if not len(opts.tfce) % 2 == 0:
				print "Error. The must be an even number of input for --tfce"
				quit()
			tfce_settings_mask = []
			for i in np.unique(opts.assigntfcesettings):
				tfce_settings_mask.append((np.array(opts.assigntfcesettings) == int(i)))
				pointer = int(i*2)
				adjacency = merge_adjacency_array(np.array(adjacent_range)[tfce_settings_mask[int(i)]], np.array(adjacency_array)[tfce_settings_mask[int(i)]])
				calcTFCE.append((CreateAdjSet(float(opts.tfce[pointer]), float(opts.tfce[pointer+1]), adjacency)))
				del adjacency
		else:
			adjacency = merge_adjacency_array(adjacent_range, adjacency_array)
			calcTFCE.append((CreateAdjSet(float(opts.tfce[0]), float(opts.tfce[1]), adjacency)))

		# make mega mask
		fullmask = create_full_mask(masking_array)

		if not opts.noweight:
			# correction for vertex density
			vdensity = []
			#np.ones_like(masking_array)
			for i in range(len(masking_array)):
				temp_vdensity = np.zeros((adjacency_array[adjacent_range[i]].shape[0]))
				for j in xrange(adjacency_array[adjacent_range[i]].shape[0]):
					temp_vdensity[j] = len(adjacency_array[adjacent_range[i]][j])
				if masking_array[i].shape[2] == 1:
					temp_vdensity = temp_vdensity[masking_array[i][:,0,0]==True]
				vdensity = np.hstack((vdensity, np.array((1 - (temp_vdensity/temp_vdensity.max())+(temp_vdensity.mean()/temp_vdensity.max())), dtype=np.float32)))
			del temp_vdensity
		else:
			vdensity = 1

		#load regressors
		if opts.input: 
			arg_predictor = opts.input[0]
			arg_covars = opts.input[1]
			pred_x = np.genfromtxt(arg_predictor, delimiter=',')
			covars = np.genfromtxt(arg_covars, delimiter=',')
			x_covars = np.column_stack([np.ones(len(covars)),covars])
			merge_y = resid_covars(x_covars,image_array[0])
		if opts.regressors:
			arg_predictor = opts.regressors[0]
			pred_x = np.genfromtxt(arg_predictor, delimiter=',')
			merge_y=image_array[0].T

		# cleanup 
		image_array = None
		adjacency_array = None
		adjacency = None

		if opts.analysisname:
			outname = opts.analysisname[0]
		else:
			outname = opts.tmifile[0][:-4]

		# make output folder
		if not os.path.exists("output_%s" % (outname)):
			os.mkdir("output_%s" % (outname))
		os.chdir("output_%s" % (outname))
		if opts.randomise:
			randTime=int(time())
			mapped_y = merge_y.astype(np.float32, order = "C") # removed memory mapping
			merge_y = None
			if not outname.endswith('tmi'):
				outname += '.tmi'
			outname = 'stats_' + outname
			if not os.path.exists("output_%s" % (outname)):
				os.mkdir("output_%s" % (outname))
			os.chdir("output_%s" % (outname))
			for i in range(opts.randomise[0],(opts.randomise[1]+1)):
				if opts.assigntfcesettings:
					calc_mixed_tfce(opts.assigntfcesettings, 
						mapped_y,
						masking_array,
						position_array,
						vdensity,
						pred_x,
						calcTFCE,
						perm_number=i,
						randomise = True)
				else:
					calculate_tfce(mapped_y, 
						masking_array,
						pred_x, calcTFCE[0],
						vdensity,
						position_array,
						fullmask,
						perm_number=i,
						randomise = True)
			print("Total time took %.1f seconds" % (time() - currentTime))
			print("Randomization took %.1f seconds" % (time() - randTime))
		else:
			# Run TFCE
			if opts.assigntfcesettings:
				tvals, tfce_tvals, neg_tfce_tvals = calc_mixed_tfce(opts.assigntfcesettings, merge_y, masking_array, position_array, vdensity, pred_x, calcTFCE)
			else:
				tvals, tfce_tvals, neg_tfce_tvals = calculate_tfce(merge_y, masking_array, pred_x, calcTFCE[0], vdensity, position_array, fullmask)
			if opts.outtype[0] == 'tmi':
				if not outname.endswith('tmi'):
					outname += '.tmi'
				outname = 'stats_' + outname
				# write tstat
				write_tm_filetype(outname, image_array = tvals.T, masking_array=masking_array, maskname=maskname, affine_array=affine_array, vertex_array=vertex_array, face_array=face_array, surfname=surfname, checkname=False, tmi_history=[])
				# read the tmi back in.
				_, image_array, masking_array, maskname, affine_array, vertex_array, face_array, surfname, _, tmi_history, subjectids = read_tm_filetype(outname, verbose=False)
				write_tm_filetype(outname, image_array = np.column_stack((image_array[0],tfce_tvals.T)), masking_array=masking_array, maskname=maskname, affine_array=affine_array, vertex_array=vertex_array, face_array=face_array, surfname=surfname, checkname=False, tmi_history=tmi_history)
				_, image_array, masking_array, maskname, affine_array, vertex_array, face_array, surfname, adjacency_array, tmi_history, subjectids = read_tm_filetype(outname, verbose=False)
				write_tm_filetype(outname, image_array = np.column_stack((image_array[0],neg_tfce_tvals.T)), masking_array=masking_array, maskname=maskname, affine_array=affine_array, vertex_array=vertex_array, face_array=face_array, surfname=surfname, checkname=False, tmi_history=tmi_history)
			else:
				print "not implemented yet"

if __name__ == "__main__":
	parser = getArgumentParser()
	opts = parser.parse_args()
	run(opts)
