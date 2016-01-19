import numpy as np
import urllib2
import csv
import pandas as pd
from subprocess import call
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from pylab import *
import os
matplotlib.rcParams['figure.figsize'] = (50, 50)

class fda:
    def __init__(self,initialYear,endYear,city,code):
        self.initialYear = initialYear
        self.endYear = endYear
        self.city = city
        self.code = code
        self.mean = 0.0
        self.std = 0.0
        self.years = endYear - initialYear + 1
        # self.city_curve_map = {}
        # self.size = size

    # initialYear = int(input("Enter initialYear: "))
    # endyear = int(input("Enter endyear: "))

    # city = raw_input("Enter a city: ")
    # code = raw_input("Enter code: ")



    def makeCSV(self,year):
        filename = self.city+str(year)+'.csv'
        if os.path.isfile(filename):
            return
        
        csvfile = urllib2.urlopen('http://www.wunderground.com/history/airport/'+self.code+'/'+str(year)+'/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=2015&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1')
        csvResponse = csvfile.read()
        target = open("temp.csv", 'w')
        target.write(csvResponse)


        mainRows = []
        with open('temp.csv') as csvfile:
            csvfile = csv.reader(csvfile)
            for row_no,row in enumerate(csvfile):
                if row_no > 0:
                    mainRows.append(row)
        
        call(["rm","temp.csv"])

        with open(filename, 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(mainRows)
                
    def getFiveYearsMean(self,year):
        filename = self.city+year+'.csv'
        try:
            data = pd.read_csv(filename)
        except:
            self.years = self.years-1
            return None


        meanTempDay = data[data.columns[2]]
        try:
	        self.mean =self.mean + round(meanTempDay.mean(),2)/self.years
        except:
	    	return None
        #self.std = self.std + round(meanTempDay.std(),2)/self.years
        # maxT = meanTempDay.max()

        l = []
        for i in xrange(24):
            l.append( (meanTempDay[15*i:15*i+15].mean() ) )

        return pd.DataFrame(l)/self.years

    def getBSplineCurve(self,fifteenDaysMean):
        x = np.linspace(0,23,24)
        y = np.array(fifteenDaysMean)
        # plt.plot(x, y,'ro', ms= 5)
        # plt.xlabel('15 days mean')
        # plt.ylabel('temperature')
        # plt.title(self.city+str(self.initialYear)+'-'+str(self.endYear))

        spl = UnivariateSpline(x, y)
        xs = np.linspace(0, 23, 1000)
        spl_xs = spl(xs)
        # plt.plot(xs, spl_xs, 'g', lw=3)
        # plt.ylim([-30,40])
        # plt.text(1,fifteenDaysMean.mean()*1.5,'mu = '+ str(self.mean)+' sigma = '+ str(self.std), horizontalalignment='left',
        #  verticalalignment='center')
        # plt.savefig(self.city+str(self.initialYear)+'.png')
        # plt.show()
        # self.city_curve_map[self.city] = plt
        # plt.close()
        if np.isnan(spl_xs).any():
            return None
        else:
            return spl_xs


    	return self.city_curve_map

    def getCurve(self):
        for curYear in range(self.initialYear,self.endYear+1):
            self.makeCSV(curYear)


        fifteenDaysMean = None
        for curYear in range(self.initialYear,self.endYear+1):
            fiveYearsMean = self.getFiveYearsMean(str(curYear))
            if fiveYearsMean is None:
                continue
            if fifteenDaysMean is None:
                fifteenDaysMean = fiveYearsMean
            else:
                fifteenDaysMean = fifteenDaysMean + fiveYearsMean

        # fifteenDaysMean.loc[23] = fifteenDaysMean.loc[0]
        if fifteenDaysMean is not None:
            curve = self.getBSplineCurve(fifteenDaysMean)
            return curve
        else:
            print "No data found for : " + self.city
            return None

    

    def getDerivative(self,curve):
    	der = []
    	for i in xrange(1,len(curve)-1):
    		der.append(1000*(curve[i] - curve[i-1]))

    	return der



    def getFeatures(self,points):

    	features = []
    	features.append(max(points))
    	features.append(points.index(max(points)))
    	features.append(min(points))
    	features.append(points.index(min(points)))
    	features.append(max(points) - min(points))

    	der = getDerivative(points)

    	features.append(max(der))
    	features.append(min(der))

    	# no of extremum
    	count = 0
    	for i in xrange(1,len(points)-2):
    		if points[i]>points[i-1] and points[i]>points[i+1]:
    			count = count+1

    	features.append(count)
    	return features




# x = np.linspace(0,23,24)
# y = np.linspace(5,28,24)
# data = {'x':x,'y':y}
# import seaborn as sb                           http://stanford.edu/~mwaskom/software/seaborn/tutorial/axis_grids.html
# g = sb.FacetGrid(pd.DataFrame(data))
# g.map(plt.scatter, "x", "y")
# g.add_legend();