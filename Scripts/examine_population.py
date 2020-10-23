import math
import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import random

class idData:
	def __init__(self, id, app_data, chest, left, right):
		self.id = id
		self.app_data = app_data
		self.chest = chest
		self.left = left
		self.right = right

# return timing intervals as indicated in appData.json
# labeled in unix timestamps
def get_timings(app_data):
	stamps = app_data['activityTimestamps']
	timings = []
	for s in stamps:
		t1 = s['enter']
		t2 = s['leave']
		timings.append(t1)
		timings.append(t2)
	return timings

# return timing intervals as indicated in appData.json
# labeled in minutes
def get_timings_min(app_data):
	stamps = app_data['activityTimestamps']
	timings = []
	for s in stamps:
		t1 = ((s['enter']/1000)/60) % 60
		t2 = ((s['leave']/1000)/60) % 60
		timings.append(t1)
		timings.append(t2)
	return timings

def draw_timings(plt, timings):
	plt.axvspan(timings[4], timings[5], alpha=0.2, color='green', label='VAS')						# First sliders
	plt.axvspan(timings[6], timings[7], alpha=0.3, color='blue', label='Rust')						# First relax
	plt.axvspan(timings[8], timings[9], alpha=0.2, color='pink', label='Spraak voor stress')		# First record
	plt.axvspan(timings[10], timings[11], alpha=0.2, color='green')									# Second sliders
	plt.axvspan(timings[12], timings[13], alpha=0.2, color='red', label='MIST')						# MIST
	plt.axvspan(timings[14], timings[15], alpha=0.3, color='purple', label = 'Spraak na stress')	# Second record
	plt.axvspan(timings[16], timings[17], alpha=0.4, color='pink', label='Feedback')				# Feedback
	plt.axvspan(timings[18], timings[19], alpha=0.2, color='green') 								# Third sliders
	plt.axvspan(timings[20], timings[21], alpha=0.3, color='blue')									# Second relax
	plt.axvspan(timings[22], timings[23], alpha=0.2, color='green') 								# Fourth sliders
	plt.axvspan(timings[24], timings[25], alpha=0.25, color='green', label='RRS/DASS')				# PANAS
	plt.axvspan(timings[26], timings[27], alpha=0.25, color='green')								# DASS

# plot the ECG
def plot_ECG(data, feature):
	print('Plotting ECG of id '+data.id)
	minutes = ((data.chest['time']/1000)/60) % 60
	hours = (((data.chest['time']/1000)/60)/60) % 24
	plt.figure(figsize=(15,8))
	plt.title('ECG van ID '+str(data.id),fontsize=22)
	plt.plot(data.chest['time'], data.chest[feature],linewidth=2.0,color='black')
	xt = []
	xl = []
	c = 0
	for m in minutes:
		if m % 5 == 0:
			xt.append((data.chest['time'])[c])
			if m < 10:
				xl.append(str(int(hours[c]))+':0'+str(int(m))) # hh:mm label
			else:
				xl.append(str(int(hours[c]))+':'+str(int(m))) # hh:mm label
		c += 1
	plt.xticks(xt, xl)
	timings = get_timings(data.app_data)
	draw_timings(plt, timings)
	questions = (data.app_data['actualQuestions'])[0]
	plt.axvline(questions['start'], linestyle='--', color='black', label='Real MIST')
	plt.grid(True)
	plt.xlabel('Tijdstip (uren)', fontsize=18)
	plt.ylabel(feature, fontsize=18)
	plt.legend(fontsize=14)
	plt.show()

# plot the EDA/GSR
# data is an idData instance
# scaling 'none', 'rest_normalized', 'normalized'
# no scaling plots GSR as is, 'normalized' scaled all data from 0 to 1
# and 'rest_normalized' sets the end of the first rest period to 1 with
# 0 at the lowest point before rest
# col selects what data to plot from the csv file (eg.: 'GSR_SCL')
# left and right are booleans to indicate data presence
def plot_GSR(data, col, left, right):
	print('Plotting GSR of id '+data.id)
	if left:
		minutes = ((data.left['time']/1000)/60) % 60
		hours = (((data.left['time']/1000)/60)/60) % 24
	elif right:
		minutes = ((data.right['time']/1000)/60) % 60
		hours = (((data.right['time']/1000)/60)/60) % 24
	plt.figure(figsize=(15,8))
	if data.app_data['rightHanded']:
		handedness = ' (Rechtshandig)'
	else:
		handedness = ' (Linkshandig)'
	plt.title('EDA van ID '+str(data.id)+handedness,fontsize=22)
	if left:
		plt.plot(data.left['time'], data.left[col],linewidth=2.0,color='black', label='Linkerhand')
	if right:
		plt.plot(data.right['time'], data.right[col],linewidth=2.0,color='blue', label='Rechterhand')
	xt = []
	xl = []
	c = 0
	for m in minutes:
		if m % 5 == 0:
			if left:
				xt.append((data.left['time'])[c])
			else:
				xt.append((data.right['time'])[c])
			if m < 10:
				xl.append(str(int(hours[c]))+':0'+str(int(m))) # hh:mm label
			else:				
				xl.append(str(int(hours[c]))+':'+str(int(m))) # hh:mm label
		c += 1
	plt.xticks(xt, xl)
	timings = get_timings(data.app_data)
	draw_timings(plt, timings)
	questions = (data.app_data['actualQuestions'])[0]
	plt.axvline(questions['start'], linestyle='--', color='black', label='Echte MIST')
	plt.grid(True)
	plt.xlabel('Tijdstip (uren)', fontsize=18)
	plt.ylabel(col, fontsize=18)
	plt.legend(fontsize=14)
	plt.show()

# plot a statistical population plot of GSR
# id_datas and ids to be considered
def plot_pop_GSR(id_datas, ids):
	all_data = pd.DataFrame()
	lengths = []
	longest_min = []
	for id in ids:
		gsr = id_datas[id].left

		# Cut GSR from beginning of first rest to end of PANAS
		minutes = ((gsr['time']/1000)/60) % 60
		timings = get_timings_min(id_datas[id].app_data)
		c = 0
		for m in minutes:
			if abs(timings[6]-m) <= 0.015: # Less than a second time difference
				start = c
			if abs(timings[25]-m) <= 0.015:
				end = c
			c += 1
		gsr = gsr[start:end]
		if len(minutes) > len(longest_min):
			longest_min = minutes-minutes[0] # Use a relative timescale, as long as the longest timeseries
		i = gsr['time'].index.values[0]
		gsr['time'] = gsr['time'] - (gsr['time'])[i]
		all_data = all_data.append(gsr)
		lengths.append(len(gsr))

	# Examine difference in GSR data length
	plt.hist(lengths)
	plt.title('Lengtes van afgesneden EDA data')
	plt.show()

	# Line plot with confidence interval
	all_data.set_index('time')
	ax = sns.lineplot(x='time', y='GSR_SCL', data=all_data)
	xl = [0, 5, 10, 15, 20, 25, 30]
	xt = np.multiply(xl, 60*1000)
	plt.xticks(xt, xl)
	plt.xlabel('Verlopen tijd sinds de start van de eerste rust (minuten)', fontsize=18)
	plt.ylabel('GSR_SCL', fontsize=18)
	plt.grid(True)
	plt.show()

# Plot accelerometer data
def plot_acceleration(data, left, right, chest):
	print('Plotting acceleration of id '+data.id)
	if left:
		minutes = ((data.left['time']/1000)/60) % 60
		hours = (((data.left['time']/1000)/60)/60) % 24
	elif right:
		minutes = ((data.right['time']/1000)/60) % 60
		hours = (((data.right['time']/1000)/60)/60) % 24
	elif chest:
		minutes = ((data.right['time']/1000)/60) % 60
		hours = (((data.right['time']/1000)/60)/60) % 24
	plt.figure(figsize=(15,8))
	if data.app_data['rightHanded']:
		handedness = ' (Rechtshandig)'
	else:
		handedness = ' (Linkshandig)'
	plt.title('accelerometerdata van ID '+str(data.id)+handedness,fontsize=22)
	xt = []
	xl = []
	c = 0
	for m in minutes:
		if m % 5 == 0:
			xt.append((data.left['time'])[c])
			if m < 10:
				xl.append(str(int(hours[c]))+':0'+str(int(m))) # hh:mm label
			else:				
				xl.append(str(int(hours[c]))+':'+str(int(m))) # hh:mm label
		c += 1
	plt.xticks(xt, xl)
	timings = get_timings(data.app_data)
	draw_timings(plt, timings)
	questions = (data.app_data['actualQuestions'])[0]
	plt.axvline(questions['start'], linestyle='--', color='black', label='Echte MIST')
	plt.grid(True)
	if left:
		mean_left = abs(data.left['mean_x'])+abs(data.left['mean_y'])+abs(data.left['mean_z'])
		std_left = abs(data.left['std_x'])+abs(data.left['std_y'])+abs(data.left['std_z'])
		plt.plot(data.left['time'], mean_left,linewidth=2.0,color='black', label='Linkerhand')
		plt.fill_between(data.left['time'], mean_left+std_left,mean_left-std_left, color='lightgray', alpha=0.8)
	if right:
		mean_right = abs(data.right['mean_x'])+abs(data.right['mean_y'])+abs(data.right['mean_z'])
		std_right = abs(data.right['std_x'])+abs(data.right['std_y'])+abs(data.right['std_z'])
		plt.plot(data.right['time'], mean_right,linewidth=2.0,color='blue', label='Rechterhand')
		plt.fill_between(data.right['time'], mean_right+std_right,mean_right-std_right , color='lightblue',alpha=0.8)
	if chest:
		mean_chest = abs(data.chest['mean_x'])+abs(data.chest['mean_y'])+abs(data.chest['mean_z'])
		std_chest = abs(data.chest['std_x'])+abs(data.chest['std_y'])+abs(data.chest['std_z'])
		plt.plot(data.chest['time'], mean_chest,linewidth=2.0,color='red', label='Borst')
		plt.fill_between(data.chest['time'], mean_chest+std_chest,mean_chest-std_chest, color='lightcoral',alpha=0.8)

	plt.xlabel('Tijdstip (uren)', fontsize=18)
	plt.ylabel('acc', fontsize=18)
	plt.legend(fontsize=14)
	plt.show()

# Low- or highpass filter
# fc = cutoff frequency as a fraction of the sampling rate
# low is a boolean to indicate low or high-pass filtering
# trans = size of transition band as a fraction of the sampling rate
# Fs = sample freq in Hz (default 1 Hz)
def filter(signal, Fc, low, trans=0.05, Fs=1):
	N = int(np.ceil(4/trans)) # 
	if not N % 2: N += 1
	n = np.arange(N)

	# Compute LP filter
	h = np.sinc(2*Fc*(n - (N-1)/2))
	w = np.blackman(N)	# Window function
	h = h * w
	h = h / np.sum(h) 	# Windowed filter

	# Compute HP filter via spectral inversion
	if not low:
		h = -h
		h[(N-1) // 2] += 1

	return np.convolve(signal, h)

# Checks data validity
# Returns a string stating a possible issue or 'valid'
def is_valid_GSR(data):
	# Check energy
	if (data['GSR_SCL'].values**2).sum(axis=0) < 7: # Magic number heuristically chosen
		return 'low_energy'

	# High pass to check for noise/discontinuities
	s = filter(data['GSR_SCL'].values, 0.06, False)
	cut = (len(s) - len(data['GSR_SCL'].values))//2 + 10
	s = s[cut:len(s)-cut]
	s = np.divide(s, np.max(s)) # Normalize
	HF_e = (s**2).sum(axis=0)
	if HF_e > 30: # Determined with histogram
		return 'high_frequency'

	# Check amount of zeroes
	unique, counts = np.unique(data['GSR_SCL'].values, return_counts=True)
	#uc = dict(zip(unique,counts))
	if 0 in unique:
		return 'zeros'
	return 'valid'

# Find possibly invalid GSR data
def find_outliers_GSR(id_datas, lefts, rights):
	low_energies = []
	high_frequencies = []
	zeros = []

	for id in lefts:
		data = id_datas[str(id)].left
		v = is_valid_GSR(data)
		if v is 'low_energy':
			low_energies.append(id)
		if v is 'high_frequency':
			high_frequencies.append(id)
		if v is 'zeros':
			zeros.append(id)

	for id in rights:
		data = id_datas[str(id)].right
		v = is_valid_GSR(data)
		if v is 'low_energy':
			if id not in low_energies:
				low_energies.append(id)
		if v is 'high_frequency':
			if id not in high_frequencies:
				high_frequencies.append(id)
		if v is 'zeros':
			if id not in zeros:
				zeros.append(id)

	print("Low energy: "+str(low_energies))
	print("Unsmooth: "+str(high_frequencies))
	print("Zeros: "+str(zeros))

# Calculate GSR variations
# Start and stop are 12 and 13 for the MIST
def calculate_GSR_var(data, left, start, stop):
	timings = get_timings(data.app_data)
	t1 = int(timings[start]/1000)*1000 # Remove milliseconds
	t2 = int(timings[stop]/1000)*1000
	try:
		if left:
			pre_MIST = data.left.set_index('time').loc[t1, 'GSR_SCL']
			post_MIST = data.left.set_index('time').loc[t2, 'GSR_SCL']
			max_MIST = data.left['GSR_SCL'].max()
		else:
			pre_MIST = data.right.set_index('time').loc[t1, 'GSR_SCL']
			post_MIST = data.right.set_index('time').loc[t2, 'GSR_SCL']
			max_MIST = data.right['GSR_SCL'].max()
		var = (post_MIST - pre_MIST)/max_MIST
		return var
	except:
		print("ID "+data.id+' appears to have incomplete GSR data')
		return None

# Calculate the average GSR over a span of time and compare with the peak GSR
def avg_GSR_over_peak(data, left, start, stop):
	timings = get_timings(data.app_data)
	t1 = int(timings[start]/1000)*1000 # Remove milliseconds
	t2 = int(timings[stop]/1000)*1000
	try:
		if left:
			avg_over_peak = data.left.set_index('time').loc[t1:t2, 'GSR_SCL'].mean() / data.left.max()
		else:
			avg_over_peak = data.right.set_index('time').loc[t1:t2, 'GSR_SCL'].mean() / data.right.max()
		return avg_over_peak
	except:
		print('ID '+data.id+' appears to have incomplete GSR data')
		return None

# Calculate LFHF variations
def calculate_LFHF_var(data):
	timings = get_timings(data.app_data)
	t1 = int(timings[12]/1000)*1000 # Remove milliseconds, index 12 and 13 mark the beginning and end of the MIST
	t2 = int(timings[13]/1000)*1000
	pre_MIST = data.chest.set_index('time').loc[t1, 'ECG_LFHF']
	post_MIST = data.chest.set_index('time').loc[t2, 'ECG_LFHF']
	max_MIST = data.chest['ECG_LFHF'].max()
	var = (post_MIST - pre_MIST)/max_MIST
	return var

# Scatter plot GSR variations against VAS
def plot_GSR_VAS(id_datas, ids):
	vas = pd.read_csv('VASscores.csv').set_index('ID')
	gsr = pd.DataFrame(columns=['ID', 'var']).set_index('ID') # Hold GSR variations per ID
	for id in ids:
		data = id_datas[id]
		if data.left is not None:
			gsr = gsr.append(pd.DataFrame({'ID':[data.id], 'var':[calculate_GSR_var(data, True, 12, 13)]}).set_index('ID'))
		elif data.right is not None:
			gsr = gsr.append(pd.DataFrame({'ID':[data.id], 'var':[calculate_GSR_var(data, False, 12, 13)]}).set_index('ID'))
		else:
			print('ID '+data.id+' did not contain any GSR data')
	gsr_vas = pd.DataFrame(columns=['ID','gsr_var','vas_delta'])
	for id in vas.index.tolist():
		if str(id) in gsr.index.tolist():
			gsr_vas = gsr_vas.append(pd.DataFrame({'ID':str(id),'gsr_var':[float((gsr['var'])[str(id)])], 'vas_delta':[float((vas['VAS Delta'])[id])]}))
	gsr_vas.plot.scatter(x='gsr_var', y='vas_delta')
	greens = gsr_vas[(gsr_vas['gsr_var'] > 0) & (gsr_vas['vas_delta'] < 0)]['ID']
	plt.fill([0,0,1,1],[0,-250,-250,0], 'g', alpha=0.3)
	plt.fill([0,0,-1,-1],[0,-250,-250,0], 'r', alpha=0.3)
	plt.fill([0,0,-1,-1],[0,100,100,0], 'r', alpha=0.5)
	plt.fill([0,0,1,1],[0,100,100,0], 'r', alpha=0.3)
	plt.xlim([-0.75,1])
	plt.ylim([-250,75])
	plt.xlabel('EDA variatie', fontsize=18)
	plt.ylabel('VAS variatie', fontsize=18)
	plt.grid(True)
	plt.show()

# Scatter plot GSR variations against predicted labels
def plot_GSR_labels(id_datas, ids):
	def draw_regions():
		# plt.fill([0,0,1,1],[0,-1,-1,0], 'g', alpha=0.3)
		# plt.fill([0,0,-1,-1],[0,-1,-1,0], 'r', alpha=0.3)
		# plt.fill([0,0,-1,-1],[0,1,1,0], 'r', alpha=0.5)
		# plt.fill([0,0,1,1],[0,1,1,0], 'r', alpha=0.3)
		plt.xlim([-1,1])
		plt.ylim([0,1])
		plt.xlabel('EDA variatie', fontsize=18)
		plt.ylabel('Stressprobabiliteit', fontsize=18)
		plt.grid(True)
		plt.show()
	prob = pd.read_csv('ivector_predicted_probabilities.csv').set_index('id')
	gsr = pd.DataFrame(columns=['ID', 'var']).set_index('ID') # Hold GSR variations per ID
	for id in ids:
		data = id_datas[id]
		if data.left is not None:
			gsr = gsr.append(pd.DataFrame({'ID':[data.id], 'var_before':[avg_GSR_over_peak(data, True, 8, 9)], 'var_after':[avg_GSR_over_peak(data, True, 14, 15)]}).set_index('ID'))
		elif data.right is not None:
			gsr = gsr.append(pd.DataFrame({'ID':[data.id], 'var_before':[avg_GSR_over_peak(data, False, 8, 9)], 'var_after':[avg_GSR_over_peak(data, False, 14, 15)]}).set_index('ID'))
		else:
			print('ID '+data.id+' did not contain any GSR data')
	gsr_prob = pd.DataFrame(columns=['ID','var_before', 'var_after','before','after'])
	for id in prob.index.tolist():
		if str(id) in gsr.index.tolist():
			gsr_prob = gsr_prob.append(pd.DataFrame({'ID':str(id), 'var_before':[float((gsr['var_before'])[str(id)])], 'var_after':[float((gsr['var_after'])[str(id)])], 'before':[float((prob['before'])[id])], 'after':[float((prob['after'])[id])]}))
	gsr_prob.plot.scatter(x='var_before', y='before')
	draw_regions()
	gsr_prob.plot.scatter(x='var_after', y='after')
	draw_regions()

# Scatter plot GSR variations against VAS
def plot_LFHF_VAS(id_datas, ids):
	vas = pd.read_csv('VASscores.csv').set_index('ID')
	lfhf = pd.DataFrame(columns=['ID', 'var']).set_index('ID') # Hold GSR variations per ID
	for id in ids:
		data = id_datas[id]
		if data.chest is not None:
			lfhf = lfhf.append(pd.DataFrame({'ID':[data.id], 'var':[calculate_LFHF_var(data,)]}).set_index('ID'))
		else:
			print('ID '+data.id+' did not contain any ECG data')
	lfhf_vas = pd.DataFrame(columns=['lfhf_var','vas_delta'])
	for id in vas.index.tolist():
		if str(id) in lfhf.index.tolist():
			lfhf_vas = lfhf_vas.append(pd.DataFrame({'lfhf_var':[float((lfhf['var'])[str(id)])], 'vas_delta':[float((vas['VAS Delta'])[id])]}))
	lfhf_vas.plot.scatter(x='lfhf_var', y='vas_delta')
	plt.fill([0,0,1,1],[0,-250,-250,0], 'g', alpha=0.3)
	plt.fill([0,0,-1,-1],[0,-250,-250,0], 'r', alpha=0.3)
	plt.fill([0,0,-1,-1],[0,100,100,0], 'r', alpha=0.5)
	plt.fill([0,0,1,1],[0,100,100,0], 'r', alpha=0.3)
	plt.xlim([-0.75,1])
	plt.ylim([-250,75])
	plt.xlabel('LFHF variation', fontsize=18)
	plt.ylabel('VAS variation', fontsize=18)
	plt.grid(True)
	plt.show()

#Scatter plot RRS scores against VAS
def plot_RRS_VAS_MIST(id_datas):
	vas = pd.read_csv('Vasscores.csv').set_index('ID')
	vas = vas.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
	vas.plot.scatter(x='TT RRS',y='VAS Delta')
	plt.xlim([0,70])
	plt.ylim([-250,75])
	plt.xlabel('RRS Treynor Totaal', fontsize=18)
	plt.ylabel('VAS', fontsize=18)
	plt.grid(True)
	plt.show()
	
#Scatter plot gem DASS scores against VAS
def plot_DASS_VAS(id_datas):
	vas = pd.read_csv('Vasscores.csv').set_index('ID')
	vas.plot.scatter(x='gem DASS',y='VAS Delta')
	plt.xlim([0,20])
	plt.ylim([-250,75])
	plt.xlabel('gemiddelde DASS', fontsize=18)
	plt.ylabel('VAS', fontsize=18)
	plt.grid(True)
	plt.show()

#Scatter plot stress DASS scores against VAS
def plot_DASS_STRESS_VAS(id_datas):
	vas = pd.read_csv('Vasscores.csv').set_index('ID')
	vas.plot.scatter(x='stress DASS',y='VAS Delta')
	plt.xlim([0,20])
	plt.ylim([-250,75])
	plt.xlabel('DASS STRESS', fontsize=18)
	plt.ylabel('VAS', fontsize=18)
	plt.grid(True)
	plt.show()
	
#Scatter plot anxiety DASS scores against VAS
def plot_DASS_ANXIETY_VAS(id_datas):
	vas = pd.read_csv('Vasscores.csv').set_index('ID')
	vas.plot.scatter(x='anxiety DASS',y='VAS Delta')
	plt.xlim([0,20])
	plt.ylim([-250,75])
	plt.xlabel('DASS ANXIETY', fontsize=18)
	plt.ylabel('VAS', fontsize=18)
	plt.grid(True)
	plt.show()
	
#Scatter plot depressie DASS scores against VAS
def plot_DASS_DEPRESSION_VAS(id_datas):
	vas = pd.read_csv('Vasscores.csv').set_index('ID')
	vas.plot.scatter(x='depressie DASS',y='VAS Delta')
	plt.xlim([0,20])
	plt.ylim([-250,75])
	plt.xlabel('DASS DEPRESSION', fontsize=18)
	plt.ylabel('VAS', fontsize=18)
	plt.grid(True)
	plt.show()
	
#Scatter plot RRS brooding against VAS 2e rust	
def plot_RRS_VAS(id_datas):
	vas = pd.read_csv('Vasscores.csv').set_index('ID')
	vas.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
	vas.plot.scatter(x='TT RRS',y='VAS Delta 2e rust')
	plt.fill([0,0,70,70],[-100,0,0,-100],'r',alpha=0.3)
	plt.fill([0,0,70,70],[200,0,0,200],'g',alpha=0.3)
	plt.xlim([0,70])
	plt.ylim([-100,200])
	plt.xlabel('RRS Treynor Totaal', fontsize=18)
	plt.ylabel('VAS variatie 2e rust', fontsize=18)
	plt.grid(True)
	plt.show()
	
#Scatter plot RRS brooding against GSR 2e rust
def plot_RRS_GSR(id_datas, ids):
	vas = pd.read_csv('VASscores.csv').set_index('ID')
	gsr = pd.DataFrame(columns=['ID', 'var']).set_index('ID') # Hold GSR variations per ID
	for id in ids:
		data = id_datas[id]
		if data.left is not None:
			gsr = gsr.append(pd.DataFrame({'ID':[data.id], 'var':[calculate_GSR_var(data, True, 20, 21)]}).set_index('ID'))
			if calculate_GSR_var(data, True, 20, 21) is not None:
				if calculate_GSR_var(data, True, 20, 21) > 0.25:
					print(data.id)
		elif data.right is not None:
			gsr = gsr.append(pd.DataFrame({'ID':[data.id], 'var':[calculate_GSR_var(data, False, 20, 21)]}).set_index('ID'))
			if 	calculate_GSR_var(data, False, 20, 21) is not None:
				if calculate_GSR_var(data, False, 20, 21) > 0.25:
					print(data.id)
		else:
			print('ID '+data.id+' did not contain any GSR data')
	gsr_vas = pd.DataFrame(columns=['ID','gsr_var','TT_RRS'])
	for id in vas.index.tolist():
		if str(id) in gsr.index.tolist():
			gsr_vas = gsr_vas.append(pd.DataFrame({'ID':str(id),'gsr_var':[float((gsr['var'])[str(id)])], 'TT_RRS':[float((vas['TT RRS'])[id])]}))
	gsr_vas.plot.scatter(x='TT_RRS', y='gsr_var')
	plt.fill([0,0,70,70],[-1,0,0,-1],'g',alpha=0.3)
	plt.fill([0,0,70,70],[1,0,0,1],'r',alpha=0.3)
	plt.xlim([0,70])
	plt.ylim([-1,1])
	plt.xlabel('RRS Treynor Totaal', fontsize=18)
	plt.ylabel('EDA variatie 2e rust', fontsize=18)
	plt.grid(True)
	plt.show()
	
# Generate stress labels as CSV
def generate_labels(id_datas, lefts, rights, completes):
	vas = pd.read_csv('VASscores.csv').set_index('ID')
	labels = pd.DataFrame(columns=['ID','before_MIST','after_MIST','feedback']).set_index('ID')
	

	# Check data validity, prefer valid left GSR > right GSR (no real reasons, more valid lefts coincidentally)
	for id in id_datas.keys():
		left = False
		right = False
		before_MIST = False
		after_MIST = False
		feedback = False
		discard = False
		if id_datas[id].id in lefts:
			if is_valid_GSR(id_datas[id].left):
				left = True
		if id_datas[id].id in rights:
			if is_valid_GSR(id_datas[id].right):
				right = True
		if left or right:
			if calculate_GSR_var(id_datas[id], left, 6, 7) > 0.1: # Increase in GSR during rest?
				# TODO: Check with after
				before_MIST = True
			if (calculate_GSR_var(id_datas[id], left, 12, 13) > 0) and (vas['VAS Delta'][int(id)] < 0):
				after_MIST = True
			if calculate_GSR_var(id_datas[id], left, 13, 17) > -0.1:
				feedback = after_MIST
		elif vas['VAS Delta'][int(id)] < -50:
			after_MIST = True
			before_MIST = False # TODO: Checl
			feedback = True
		else:
			print('ID '+id+" wasn't used")
			discard = True
		if not discard:
			b = 0
			a = 0
			f = 0
			if before_MIST:
				b = 1
			if after_MIST:
				a = 1
			if feedback:
				f = 1
			labels = labels.append(pd.DataFrame({'ID':[int(id)], 'before_MIST':[b], 'after_MIST':[a], 'feedback':[f]}).set_index('ID'))
		else:
			labels = labels.append(pd.DataFrame({'ID':[int(id)], 'before_MIST':[-1], 'after_MIST':[-1], 'feedback':[-1]}).set_index('ID'))
	labels.sort_index(inplace=True)
	labels.to_csv('labels.csv', sep=',')
	return labels

# Load all data

id_datas = {}	# Contains data objects of all valid IDs (own an appData file)
chests = []		# IDs who own chest.csv
lefts = []		# IDs who own left.csv
rights = [] 	# IDs who own right.csv
completes = []	# IDs who own all of the above

dir_names = next(os.walk('.'))[1]
print('Found '+str(len(dir_names))+' IDs.')

# Loop folders
for id in dir_names:
	if os.path.isfile(os.path.join(id, 'appData.json')):
		with open(os.path.join(id,'appData.json')) as app_file:
			app_data_string = app_file.read()
			app_data = json.loads(app_data_string)
			data = idData(id, app_data, 'none', 'none', 'none')
		id_datas[id] = data

		# Check for and load CSV files
		complete = True
		if os.path.isfile(os.path.join(id, 'chest.csv')):
			chest = pd.read_csv(os.path.join(id, 'chest.csv'), sep=',')
			data.chest = chest
			if chest.empty:
				print(id + ' contains empty chest data')
			else:	
				chests.append(id)
		else:
			complete = False
		if os.path.isfile(os.path.join(id, 'left.csv')):
			left = pd.read_csv(os.path.join(id, 'left.csv'), sep=',')
			data.left = left
			if left.empty:
				print(id + ' contains empty left data')
			else:
				lefts.append(id)
		else:
			complete = False
		if os.path.isfile(os.path.join(id, 'right.csv')):
			right = pd.read_csv(os.path.join(id, 'right.csv'), sep=',')
			data.right = right
			if right.empty:
				print(id + ' contains empty right data')
			else:
				rights.append(id)
		else:
			complete = False
		if complete:
			completes.append(id)
		
print(str(len(id_datas))+' IDs contained appData.json')
print(str(len(completes))+' IDs contained all chest and bands data')

print('')
print("Commands: plot (GSR|ECG|ACC) (ID|'all') ('none'|'rest_normalized'|'normalized') (column)")
print("\t  find outliers (GSR)")
print("\t  scatter (GSR_VAS|RRS_VAS_MIST|DASS_VAS|DASS_STRESS_VAS|DASS_ANXIETY_VAS|DASS_DEPRESSION_VAS|RRS_VAS|RRS_GSR)")
print("\t  generate labels\n")

# Command loop for CLI
while True:
	x = input()
	cmd = x.split()
	
	if cmd[0].lower() == 'plot':
		if len(cmd) < 3:
			print('Not enough arguments')
			continue

		if cmd[1].lower() == "gsr":
			if cmd[2].lower() == 'all':
				# Plot population GSR
				plot_pop_GSR(id_datas, lefts)
			else:
				if len(cmd) < 4:
					cmd.append('GSR_SCL')
				id = cmd[2]
				# Plot GSR
				if (id in lefts) or (id in rights):
					plot_GSR(id_datas[id], cmd[3], (id in lefts), (id in rights))
		elif cmd[1].lower() == 'ecg':
			if cmd[2].lower() == 'all':
				# Plot population ECG
				plot_pop_ECG(id_datas, lefts)
			else:
				if len(cmd) < 4:
					cmd.append('ECG_mean_heart_rate')
				id = cmd[2]
				# Plot ECG
				if id in chests:
					plot_ECG(id_datas[id], cmd[3])
		elif cmd[1].lower() == 'acc':
			id = cmd[2]
			if (id in lefts) or (id in rights) or (id in chests):
				plot_acceleration(id_datas[id], (id in lefts), (id in rights), (id in chests))
			continue
		else:
			print("I don't know what you want me to plot")
			continue
	elif cmd[0].lower() == 'find':
		if len(cmd) == 1:
			print('Not enough arguments')
			continue
		elif cmd[1].lower() == 'outliers':
			if len(cmd) < 3:
				find_outliers(id_datas, chests, lefts, rights, completes)
			else:
				if cmd[2].lower() == 'gsr':
					find_outliers_GSR(id_datas, lefts, rights)
				else:
					print("I don't know what you want me to find")
					continue
		else:
			print('Try: find outliers')
			continue
	elif cmd[0].lower() == 'scatter':
		if len(cmd) == 1:
			print('Not enough arguments')
			continue
		elif cmd[1].lower() == 'gsr_vas':
			plot_GSR_VAS(id_datas, list(set().union(lefts,rights)))
		elif cmd[1].lower() == 'lfhf_vas':
			plot_LFHF_VAS(id_datas, chests)
		elif cmd[1].lower() == 'gsr_prob':
			plot_GSR_labels(id_datas, list(set().union(lefts,rights)))
		elif cmd[1].lower() == 'rrs_vas_mist':
			plot_RRS_VAS_MIST(id_datas)
		elif cmd[1].lower() == 'dass_vas':
			plot_DASS_VAS(id_datas)
		elif cmd[1].lower() == 'dass_stress_vas':
			plot_DASS_STRESS_VAS(id_datas)
		elif cmd[1].lower() == 'dass_anxiety_vas':
			plot_DASS_ANXIETY_VAS(id_datas)
		elif cmd[1].lower() == 'dass_depression_vas':
			plot_DASS_DEPRESSION_VAS(id_datas)
		elif cmd[1].lower() == 'rrs_vas':
			plot_RRS_VAS(id_datas)
		elif cmd[1].lower() == 'rrs_gsr':
			plot_RRS_GSR(id_datas, list(set().union(lefts,rights)))
		else:
			print('Try: scatter GSR_VAS')
	elif cmd[0].lower() == 'generate':
		if cmd[1].lower() == 'labels':
			generate_labels(id_datas, lefts, rights, completes)
		else:
			print('Try: generate labels')