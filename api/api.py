from flask import Flask,render_template,request
import numpy as np 
import pandas as pd 
import os            # For mathematical calculations 
import matplotlib.pyplot as plt  # For plotting graphs 
import datetime as dt
from datetime import datetime    # To access datetime 
from pandas import Series        # To work on series 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from matplotlib.pyplot import figure
import warnings                   # To ignore the warnings 
import math
from sklearn import preprocessing,svm
from datetime import datetime as dt
import datetime 
import calendar
warnings.filterwarnings("ignore")
plt.style.use('dark_background')
plt.show()

app = Flask(__name__)

@app.route('/')
def index(): 
	files=os.listdir("C:/Users/RAI/Desktop/Final Project/Dataset")
	data=[]
	l=len(files)
	for i in range(0,l):
		file=files[i][:-4]
		data.append (pd.read_csv("C:/Users/RAI/Desktop/Final Project/Dataset/"+file+".csv").tail(1))
	return render_template("index.html",len=len(files),files=files,data=data)

def day(last_date):
	born = datetime.datetime.strptime(last_date, '%Y-%m-%d').weekday() 
	day=calendar.day_name[born] 
	j=0
	if day=='Monday':
		j=2
	elif day=='Tuesday':
		j=3
	elif day=='Wednesday':
		j=4
	elif day=='Thursday':
		j=5
	elif day=='Friday':
		j=6
	elif day=='Saturday':
		j=7
	elif day=='Sunday':
		j=1
	return j


def ValuePredictor(name):
	df1 = pd.read_csv("C:/Users/RAI/Desktop/Final Project/Dataset/"+name+".csv")
	forecast_col = 'Close'
	df1.fillna(value=-99999, inplace=True)
	forecast_out = 60
	df1['forecast'] = df1[forecast_col]
	small= df1[['Open','High','Low','Close','Volume']]
	X=np.array(small)
	X = preprocessing.scale(X)
	X_lately = X[-forecast_out:]
	X = X[:]
	df1.dropna(inplace=True)
	y = np.array(df1['forecast'])
	y = y.reshape((y.shape[0], 1))
	X_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.2)
	clf = RandomForestRegressor(n_jobs=-1)
	clf.fit(X_train, y_train)
	forecast_set = clf.predict(X_lately)
	df1['Forecast'] = np.nan
	last_date = df1.iloc[-1].Date
	j=day(last_date)
	last_date=dt.strptime(last_date, '%Y-%m-%d').timestamp()
	last_unix = last_date
	one_day = 86400
	next_unix = last_unix + one_day
	l=len(df1)
	dict={}
	for i in forecast_set:
		next_date = dt.fromtimestamp(next_unix)
		next_unix += 86400
		if(j<=5):
			df1.loc[l,'Forecast'] = i
			df1.loc[l,'Date']=next_date.date()
			d=next_date.date().strftime("%Y-%m-%d")
			dict[d]=round(i,4)
			l=l+1
		j=j+1
		if(j==8):
			j=1
	fig5, ax = plt.subplots(figsize=(20,8))
	df1.set_index('Date', inplace=True, drop=False)
	df1.index = pd.to_datetime(df1.index)
	df1['Close'].plot(color="blue")
	df1['Forecast'].plot(color="red")
	fig5.savefig('static/images/'+name+'5.png')
	return dict

@app.route("/result",methods=["POST"])
def result():
	name=request.form.get("name")
	name=name.upper()
	companys=os.listdir("C:/Users/RAI/Desktop/Final Project/Dataset")
	if(name+".csv" in companys):
		df = pd.read_csv("C:/Users/RAI/Desktop/Final Project/Dataset/"+name+".csv")
		msg=name
		df_vwap = df[['Date','VWAP']]
		df_vwap['Date'] = df_vwap['Date'].apply(pd.to_datetime)
		df_vwap.set_index('Date', inplace=True)
		l=len(df)
		l=l-1
		cname=df['Symbol'][l]
		open=df['Open'][l]
		close=df['Close'][l]
		prev=df['Prev Close'][l]
		high=df['High'][l]
		low=df['Low'][l]
		volume=df['Volume'][l]/1000000
		trades=df['Trades'][l]
		turn=df['Turnover'][l]/1000000000
		date=df['Date'][l]
		fig1, ax = plt.subplots(figsize=(20,8))
		ax.plot(df_vwap.loc['2020-01-20':'2020-01-25', 'VWAP'], linestyle='-')
		plt.yticks([])
		plt.xticks(fontsize=16)
		plt.legend(loc='best')
		fig1.savefig('static/images/'+name+'1.png')
		fig2, ax = plt.subplots(figsize=(20,8))
		ax.plot(df_vwap.loc['2020-3':'2020-4', 'VWAP'], linestyle='-')
		fig2.savefig('static/images/'+name+'2.png')
		fig3, ax = plt.subplots(figsize=(20,8))
		ax.plot(df_vwap.loc['2020', 'VWAP'], linestyle='-')
		fig3.savefig('static/images/'+name+'3.png')
		fig4, ax = plt.subplots(figsize=(20,8))
		ax.plot(df_vwap['VWAP'], linestyle='-')
		fig4.savefig('static/images/'+name+'4.png')
		dict=ValuePredictor(name) 
		return render_template("result.html",msg=open,name=name,turn=turn,open=open,close=close,prev=prev,high=high,low=low,vol=volume,dict=dict,trades=trades,img="static/images/"+name+"1.png")
	else:
		msg="The provided company data is not available"
		return render_template("notavail.html",msg=msg)
