# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import GaussianNB
# from sklearn.naive_bayes import MultinomialNB
# import torch 
from csv import reader
from math import pi
# import pandas as pd 
from math import sqrt
from math import pi
from math import exp
import json
import collections
import os
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup	
def separate_by_class(dataset):
	separated = dict()
	for i in range(len(dataset)):
		vector = dataset[i]
		class_value = vector[-1]
		if (class_value not in separated):
			separated[class_value] = list()
		separated[class_value].append(vector)
	return separated	

def summarize_by_class(dataset):
	separated = separate_by_class(dataset)
	summaries = dict()
	for class_value, rows in separated.items():
		summaries[class_value] = summarize_dataset(rows)
	return summaries

filename='data.csv'
dataset = load_csv(filename)
separated = separate_by_class(dataset)

# sort label & data
keys = list(separated.keys())
keys.sort()

# bring header to top
last_key = keys.pop()
keys.insert(0, last_key)
# print(keys)
# re-assign value
temp = dict()
for key in keys:
    temp[key] = separated[key]
separated = temp
# dont clear temp dict

# check data
# json_object = json.dumps(separated, indent=4)
# Writing to sample.json
# with open("sort.json", "w") as outfile:
#     outfile.write(json_object)

# end sort

for label in separated:
	print(label)
	for row in separated[label]:
		print(row)

# show min, max label & value, ignore header data
min_label = keys[1]
min_label_value = separated[min_label]
print('min_label')
print(min_label)
print('min_label_value')
print(min_label_value)
# max label & value
max_label = keys[-1]
max_label_value = separated[max_label]
print('max_label')
print(max_label)
print('max_label_value')
print(max_label_value)

def mean(numbers):
	return sum(numbers)/float(len(numbers))
def stdev(numbers):
	avg = mean(numbers)
	if float(len(numbers)-1):		
		variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
		return sqrt(variance)

def summarize_dataset(dataset):
	summaries = [(mean(column), stdev(column), len(column)) for column in zip(*dataset)]
	del(summaries[-1])
	return summaries
def calculate_probability(x, mean, stdev):
	a=0
	if x is not None and mean is not None and stdev is not None and x != 0 and mean != 0 and stdev != 0 :
			exponent = exp(-((x-mean)**2.0 / (2.0 * stdev ** 2.0 )))
			a=(1 / (sqrt(2.0 * pi) * stdev)) * exponent
	return a	

def calculate_class_probabilities(summaries, row):
	total_rows = sum([summaries[label][0][2] for label in summaries])
	probabilities = dict()
	for class_value, class_summaries in summaries.items():
		probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
		for i in range(len(class_summaries)):
			mean, stdev, _ = class_summaries[i]
			probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
	return probabilities	
def predict(summaries, row):
	probabilities = calculate_class_probabilities(summaries, row)
	best_label, best_prob = None, -1
	for class_value, probability in probabilities.items():
		if best_label is None or probability > best_prob:
			best_prob = probability
			best_label = class_value
	return best_label	
filename='data.csv'
dataset = load_csv(filename)
separated = separate_by_class(dataset)
for i in range(len(dataset[0])-1):
	str_column_to_int(dataset, i)
# convert class column to integers
str_column_to_int(dataset, len(dataset[0])-1)
# fit model
model = summarize_by_class(dataset)
probabilities = calculate_class_probabilities(model, dataset[0])
print(probabilities)
# predict the label
label = predict(model, dataset[100])
print(label)
 #show min, max label & value, ignore header data
min_label = keys[1]
min_label_value = separated[min_label]
print('min_label')
print(min_label)
print('min_label_value')
print(min_label_value)
# max label & value
max_label = keys[-1]
max_label_value = separated[max_label]
print('max_label')
print(max_label)
print('max_label_value')
print(max_label_value)
# convert class column to integers
