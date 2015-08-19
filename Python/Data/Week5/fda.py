import numpy as np
import urllib2
import csv
import pandas as pd
from subprocess import call


def makeCSV(city,year):
	csvfile = urllib2.urlopen('http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=5051&Year='+year+'&Month=1&Day=1&timeframe=2&submit=Download+Data')
	csvResponse = csvfile.read()

	target = open("temp.csv", 'w')

	target.write(csvResponse)

	mainRows = []
	with open('temp.csv') as csvfile:
	    csvfile = csv.reader(csvfile)
	    for row_no,row in enumerate(csvfile):
	        if row_no > 24:
	            mainRows.append(row)

	call(["rm","temp.csv"])

	filename = city+year+'.csv'
	with open(filename, 'w') as fp:
	    a = csv.writer(fp, delimiter=',')
	    a.writerows(mainRows)
	        
def getFiveYearsMean(city,year):
	filename = city+year+'.csv'
	data = pd.read_csv(filename)

	meanTempDay = data[data.columns[9]]

	l = []
	for i in xrange(24):
	    l.append( (meanTempDay[15*i:15*i+15].mean() ) )

	return pd.DataFrame(l)/5

	







fifteenDaysMean = None
for curYear in range(1930,1936):
	if fifteenDaysMean is None:
		fifteenDaysMean = getFiveYearsMean("toronto",str(curYear))
	else:
		fifteenDaysMean = fifteenDaysMean + getFiveYearsMean("toronto",str(curYear))
	
print fifteenDaysMean







