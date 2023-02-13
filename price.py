import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
from collections import deque
import matplotlib.dates
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

FILE_PATH = "prices.csv"

def get_data():
	x_values = deque([])
	y_values = deque([])
	with open(FILE_PATH, "r") as csvfile:
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


def graph_real():

	x_values, y_values = get_data()




	dates = mdates.num2date(mdates.datestr2num(x_values))

	fig, ax = plt.subplots(1, 1)
	ax.plot(dates, y_values)


	tick_spacing = 1

	ax.minorticks_on()

	for i, date in enumerate(dates):
		date2 = str(date)[:10]
		date_arr = date2.split("-")
		
		if date2 == "1975-01-03" or date2 == "1981-01-05" or date2 == "1987-01-05" or date2 == "1997-01-03" or date2 == "2003-01-03" or date2 == "2009-01-05" or date2 == "2015-01-05":
			ax.axvline(date)

		
		if int(date_arr[0]) % 2 == 0:
			continue
		
		if int(date_arr[1]) == 1 and int(date_arr[2]) == 4:
			print(date)
			ax.axvline(date)
		




	plt.plot(dates, y_values, "-")


	plt.show()


def graph_theoretical():
	start_value = 830.57

	

