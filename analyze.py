import csv
import matplotlib
import numpy as np

FILE_PATH = "prices.csv"
FILE_PATH2 = "party_control.csv"



def partyValues():
	print("-------------\n")
	with open(FILE_PATH2, "r") as csvfile:
		reader = csv.reader(csvfile)
		for i, row in enumerate(reader):
			print(row)
			#Assign numerical values for party control in the House
			if reader[1, i].equals("Democrat") or "Democrat" in reader[1,i]:
				reader[1,i] == -0.05
			if reader[1, i].equals("Republican") or "Republican" in reader[1,i]:
				reader[i, i] == 0.05
			#Assign numerical values for party control in the Senate
			if reader[2, i].equals("Democrat") or "Democrat" in reader[2,i]:
				reader[2,i] == -0.05
			if reader[2, i].equals("Republican") or "Republican" in reader[2,i]:
				reader[2,i] == 0.05
			#Assign numerical values for party control for the Presidency
			if reader[3, i].equals("Democrat") or "Democrat" in reader[3,i]:
				reader[3,i] == -0.05
			if reader[3, i].equals("Republican") or "Republican" in reader[3,i]:
				reader[3,i] == 0.05
			



def main():
	weights = {
			"Democrat": -0.05,
			"Republican": 0.05,
			"Senate": 1.2,
			"House": 1,
			"President": 1.5
			}

	with open(FILE_PATH2, "r") as csvfile:
		reader = csv.reader(csvfile)

		categories = reader[0]

		PartyValuesArray = []
		for i, row in enumerate(reader):
			PartyValuesArray[i] = reader[1, i] * weights["House"] + reader[2, i] * weights["Senate"] + reader[3, i] * weights["President"]
			continue
				

		for i in PartyValuesArray:
			if (	)		

			#print(row[:4] + " House: {}" + "Senate: {}, President: {}".format(house + " " + , ))
