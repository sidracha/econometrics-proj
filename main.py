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
	f = open(PRESIDENTS_JSON_PATH)
	president_data = json.load(f)

	
	date_format = "%Y-%m-%d"

	slopes = []
	percentages = []

	#print("Year   Party        Slope($/year)     Slope ($/day)      % change           Intercept         R-Squared")

	data = {
		"Party": [],
		"Slope ($/year)": [],
		"Slope ($/day)": [],
		"% change (4 yrs)": [],
		"Intercept": [],
		"R Squared": []
	}

	for k, v in obj.items():

		dates = obj[k][0]

		dates_arr = []
		values_arr = obj[k][1]

		values_sum = 0
		values_count = 0

		for i, date in enumerate(dates):
			a = datetime.datetime.strptime(dates[0], date_format)
			b = datetime.datetime.strptime(date, date_format)
			delta = b-a
			dates_arr.append(delta.days)
			values_sum += values_arr[i]
			values_count += 1 

		data_time = np.asarray(dates_arr)
		data_values = np.asarray(values_arr)

		df = pd.DataFrame({"time": data_time, "count": data_values})

		regr = linear_model.LinearRegression()
		regr.fit(df.time.values.reshape(-1, 1), df["count"])

		slope = regr.coef_[0] * 365
		slope_day = slope / 365
		slopes_obj = {k: slope}
		slopes.append(slopes_obj)

		percentage = slope / values_arr[0] * 100
		percentage_obj = {k: percentage}
		percentages.append(percentage_obj)

		intercept = regr.intercept_

		SSR = 0
		SST = 0
		average = values_sum / values_count
		for i, v in enumerate(dates_arr):
			predicted = (dates_arr[i] * slope_day) + intercept
			actual = values_arr[i]
			residual = actual - predicted
			SSR += (residual ** 2)
		
			distance= actual - average
			SST += (distance ** 2)

		r_squared = 1 - (SSR / SST)

		
		#print(k, president_data[k], slope, slope_day, percentage, intercept, r_squared)
		data["Party"].append(president_data[k])
		data["Slope ($/year)"].append(slope)
		data["Slope ($/day)"].append(slope_day)
		data["% change (4 yrs)"].append(percentage)
		data["Intercept"].append(intercept)
		data["R Squared"].append(r_squared)

	#print("-------------------------")
	#print("change in price per year on average: ", get_average_values(slopes))
	#print("percent change per year on average: ", get_average_values(percentages))

	df_index = []
	for k, v in president_data.items():
		df_index.append(k)
	

	df = pd.DataFrame(data, index=df_index)

	print(df)

	return slopes, percentages


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




def example_regression_plot_values(year: int):


	data = {

		"2017": [4.78, 21353.73],
		"2013": [2.71, 14850.10],
		"1977": [0.006, 857.77]

	}


	x_values_old, y_values_old = get_data()

	x_values = []
	y_values = []

	for i, val in enumerate(x_values_old):
		if int(val[6:]) < year or int(val[6:]) > year + 3:
			continue
		

		x_values.append(val)
		y_values.append(y_values_old[i])
	
	dates = mdates.num2date(mdates.datestr2num(x_values))


	
	date_format = "%m/%d/%Y"

	line_y_values = []


	for i, v in enumerate(x_values):
		
		a = datetime.datetime.strptime(x_values[0], date_format)
		b = datetime.datetime.strptime(v, date_format)
		delta = b - a
		days = delta.days
		val = days * data[str(year)][0] + data[str(year)][1]

		line_y_values.append(val)


	

	return dates, y_values, line_y_values

def example_regression_plot(year: int):
	f = open(PRESIDENTS_JSON_PATH)
	president_data = json.load(f)

	dates, y_values, line_y_values = example_regression_plot_values(year)

	fig, ax = plt.subplots(1, 1)
	ax.plot(dates, y_values)
	plt.plot(dates, y_values, "-")
	plt.plot(dates, line_y_values)
	plt.xlabel("Date")
	plt.ylabel("DOW Jones Price ($)")
	
	party_control = president_data[str(year)]
	plt.title(party_control + " Control")
	
	plt.show()


def example_residual_plot(year: int):
	f = open(PRESIDENTS_JSON_PATH)
	president_data = json.load(f)
	

	dates, y_values, line_y_values = example_regression_plot_values(year)
	residual_zero = []
	residuals = []


	for val in dates:
		residual_zero.append(0)


	for i, v in enumerate(line_y_values):
		residual = y_values[i] - v
		residuals.append(residual)

	
	plt.plot(dates, residual_zero)
	plt.scatter(dates, residuals)
	plt.xlabel("Date")
	plt.ylabel("Residual")
	plt.title(president_data[str(year)]+ " Control")

	plt.show()
	


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
	plt.ylabel("DOW Jones Price ($)")

	plt.show()



print("1. Graph real data")
print("2. Print slopes and percentages")
print("3. Graph example regressions")

user_input = input("> ")
user_input = user_input.strip()
if user_input == "1":
	graph_real()

if user_input == "2":
	obj = get_obj()
	slopes, percentages = linear_regressions(obj)


if user_input == "3":
	print("year?")
	user_input = input("> ")

	user_input = int(user_input)

	example_regression_plot(user_input)
	#example_residual_plot(user_input)
