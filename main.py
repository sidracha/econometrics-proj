import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
from collections import deque
import matplotlib.dates
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json

import pandas as pd

from sklearn import linear_model

STOCK_CSV_PATH = "prices.csv"
PRESIDENTS_CSV_PATH = "presidents.csv"
PRESIDENTS_JSON_PATH = "presidents.json"

STARTING_DOW_VALUE = 830.57
STARTING_YEAR = 1971

def get_data():
	x_values = deque([])
	y_values = deque([])
	with open(STOCK_CSV_PATH, "r") as csvfile:
		reader = csv.reader(csvfile)
		for i, row in enumerate(reader):
			if i == 0:
				continue
		

			if row[0][6] == "0" or row[0][6] == "1" or row [0][6] == "2":
				date = row[0][:6] + "20" + row[0][6:]
			else:
				date = row[0][:6] + "19" + row[0][6:]
			
			#time = np.datetime64(date)
			#time = datetime.datetime(date)

	
			x_values.appendleft(date)

			prc = row[4][1:]
			y_values.appendleft(float(prc))

			#print(row)

		return x_values, y_values


def get_obj():

	x_values, y_values = get_data()
	dates = mdates.num2date(mdates.datestr2num(x_values))


	next = 1977
	current = 1973

	obj = {"1973": [[], []]}


	for i, d in enumerate(dates):
		date = str(d)[:10]

		if int(date[:4]) < 1973:
			continue

		if int(date[:4]) == next:
			current = next
			next += 4
			obj[str(current)] = [[], []]
		
		obj[str(current)][0].append(date)
		obj[str(current)][1].append(y_values[i])
	

	return obj


def print_president_data():

	with open(PRESIDENTS_CSV_PATH, "r") as csvfile:
		reader = csv.reader(csvfile)

		for i, row in enumerate(reader):
		
			print(row)




#obj = {
# 	
#	"1973": [[dates], [prices]],
#	"1977": [[dates], [prices]]
# 
# }

def linear_regressions(obj):
	
	date_format = "%Y-%m-%d"

	slopes = []
	percentages = []

	for k, v in obj.items():

		dates = obj[k][0]
		values = obj[k][1]

		#dates = obj["1973"][0]
		#values = obj["1973"][1]

		dates_arr = []
		values_arr = []

		for i, date in enumerate(dates):
			a = datetime.datetime.strptime(dates[0], date_format)
			b = datetime.datetime.strptime(date, date_format)
			delta = b-a
			dates_arr.append(delta.days)
			values_arr.append(values[i])


			#print(delta.days, values[i], date)
			

		data_time = np.asarray(dates_arr)
		data_values = np.asarray(values_arr)

		df = pd.DataFrame({"time": data_time, "count": data_values})

		regr = linear_model.LinearRegression()
		regr.fit(df.time.values.reshape(-1, 1), df["count"])

		slope = regr.coef_[0] * 365
		slopes_obj = {k: slope}
		slopes.append(slopes_obj)

		percentage = slope / values[0] * 100
		percentage_obj = {k: percentage}
		percentages.append(percentage_obj)

		print(percentage, slope)

	return slopes, percentages


	
	"""
	#data_time = np.asarray(obj["2017"][0])
	#data_count = np.asarray(obj["2017"][1])

	data_time = np.asarray([1, 2, 3, 4, 5, 6])
	data_count = np.asarray([2, 4, 6, 8, 10, 12])

	df = pd.DataFrame({"time": data_time, "count": data_count})

	#df.time = pd.to_datetime(df.time)

	regr = linear_model.LinearRegression()
	regr.fit(df.time.values.reshape(-1, 1), df["count"])

	print(regr.coef_)

	"""

#slopes = [
# 	{
# 		"1973": some slope
# },
#
# 
# ]

#same with percentages

def get_average_values(array_of_objs):
	f = open(PRESIDENTS_JSON_PATH)
	president_data = json.load(f)

	dems_agg = 0
	repubs_agg = 0

	dems_count = 0
	repubs_count = 0


	for obj in array_of_objs:
		year = list(obj.keys())[0]
		party = president_data[year]
		quantity = obj[year]

		if president_data[year] == "Democrat":
			dems_agg += quantity
			dems_count += 1
		
		if president_data[year] == "Republican":
			repubs_agg += quantity
			repubs_count += 1
		

	return_obj = {
		"Democrats": dems_agg/dems_count,
		"Republicans": repubs_agg/repubs_count
	}


	return return_obj	
def analyze_with_party(slopes, percentages):


	"""

	f = open(PRESIDENTS_JSON_PATH)
	president_data = json.load(f)

	dems_agg = 0
	repubs_agg = 0

	dems_count = 0
	repubs_count = 0

	for percentage_obj in percentages:
		year = list(percentage_obj.keys())[0]
		party = president_data[year]
		percent_change = percentage_obj[year]
		#print(f"year: {year}, party: {party}, percent change: {percent_change}")

		if president_data[year] == "Democrat":
			dems_agg += percent_change
			dems_count +=1 
		
		if president_data[year] == "Republican": 
			repubs_agg += percent_change
			repubs_count += 1
	
	print(f"Democrat average percent change: {dems_agg/dems_count}")
	print(f"Republican average percent change: {repubs_agg/repubs_count}")

	"""

	print("slopes", get_average_values(slopes))

	print("--------")

	print("percentages", get_average_values(percentages))	


def graph_real():

	x_values, y_values = get_data()
	tick_spacing = 1600
	dates = mdates.num2date(mdates.datestr2num(x_values))
	fig, ax = plt.subplots(1, 1)
	ax.plot(dates, y_values)
	ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
	ax.minorticks_on()

	next1 = 1977
	
	for i, d in enumerate(dates):


		date = str(d)[:10]
		if date == "1973-01-04":
			ax.axvline(d)
		
		if int(date[:4]) == next1:
			

			ax.axvline(d)
			next1 += 4

	
	plt.plot(dates, y_values, "-")
	
	plt.xlabel("Date")
	plt.ylabel("DOW Jones Index Price ($)")

	plt.show()



print("1. Print real data")
print("2. Print slopes and percentages")

user_input = input("> ")
user_input = user_input.strip()
if user_input == "1":
	graph_real()

if user_input == "2":
	obj = get_obj()
	slopes, percentages = linear_regressions(obj)
	analyze_with_party(slopes, percentages)


