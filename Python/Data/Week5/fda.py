import numpy as np
import urllib2
import csv
import pandas as pd
from subprocess import call
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt


mean = 0.0
std = 0.0

initialYear = int(input("Enter initialYear: "))
endyear = int(input("Enter endyear: "))
years = endyear - initialYear
city = raw_input("Enter a city: ")
code = raw_input("Enter code: ")
# maxT = 0.0


def makeCSV(year):
    csvfile = urllib2.urlopen('http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID='+code+'&Year='+str(year)+'&Month=1&Day=1&timeframe=2&submit=Download+Data')
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

    filename = city+str(year)+'.csv'
    with open(filename, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(mainRows)
            
def getFiveYearsMean(year):
    filename = city+year+'.csv'
    data = pd.read_csv(filename)
    global mean
    global std

    meanTempDay = data[data.columns[9]]
    mean =mean + round(meanTempDay.mean(),2)/years
    std = std + round(meanTempDay.std(),2)/years
    # maxT = meanTempDay.max()

    l = []
    for i in xrange(24):
        l.append( (meanTempDay[15*i:15*i+15].mean() ) )

    return pd.DataFrame(l)/years


def getBSplineCurve(fifteenDaysMean):
    x = np.linspace(0,23,24)
    y = np.array(fifteenDaysMean)
    plt.plot(x, y,'ro', ms= 5)
    plt.xlabel('15 days mean')
    plt.ylabel('temperature')
    plt.title(city+str(initialYear)+'-'+str(endyear))

    spl = UnivariateSpline(x, y)
    xs = np.linspace(0, 23, 1000)
    plt.plot(xs, spl(xs), 'g', lw=3)

    plt.text(1,20,'mu = '+ str(mean)+' sigma = '+ str(std), horizontalalignment='left',
     verticalalignment='center')
    plt.savefig(city+str(initialYear)+'.png')
    plt.show()
    

for curYear in range(initialYear,endyear+1):
    makeCSV(curYear)


fifteenDaysMean = None
for curYear in range(initialYear,endyear+1):
    if fifteenDaysMean is None:
        fifteenDaysMean = getFiveYearsMean(str(curYear))
    else:
        fifteenDaysMean = fifteenDaysMean + getFiveYearsMean(str(curYear))

fifteenDaysMean.loc[23] = fifteenDaysMean.loc[0]
getBSplineCurve(fifteenDaysMean)
