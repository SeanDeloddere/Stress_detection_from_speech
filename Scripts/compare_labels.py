import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

predicted = pd.read_csv('ivector_predicted_probabilities.csv', sep=',').set_index('id')
generated = pd.read_csv('labels.csv', sep=',').set_index('ID')

before_acc = 0
after_acc = 0
valids = 0
invalids = 0
for id in predicted.index.tolist():
	# Check if label was generated
	if generated.loc[id, 'before_MIST'] == -1:
		invalids += 1
		continue # Can't compare to invalid
	if generated.loc[id, 'after_MIST'] == -1:
		invalids += 1
		continue
	valids += 1
	# Compare generated to predicted label
	if predicted.loc[id, 'before'] < 0.5:
		b = 0
	else:
		b = 1
	if predicted.loc[id, 'after'] < 0.5:
		a = 0
	else:
		a = 1
	if generated.loc[id, 'before_MIST'] == b:
		before_acc += 1
	if generated.loc[id, 'after_MIST'] == a:
		after_acc += 1

before_acc = before_acc / valids
after_acc = after_acc / valids

print('Prediction accuracy before MIST: '+str(before_acc))
print('Prediction accuracy after MIST: '+str(after_acc))