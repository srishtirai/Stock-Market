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
		# df_vwap['year'] = df_vwap.Date.dt.year
		# df_vwap['month'] = df_vwap.Date.dt.month
		# df_vwap['day'] = df_vwap.Date.dt.day
		# df_vwap['day of week'] = df_vwap.Date.dt.dayofweek
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
		return render_template("result.html",msg=open,name=name,turn=turn,open=open,close=close,prev=prev,high=high,low=low,vol=volume,trades=trades,img="static/images/"+name+"1.png")
	else:
		msg="The provided company data is not available"
		return render_template("notavail.html",msg=msg)
