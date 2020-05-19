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
import warnings                   # To ignore the warnings 
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
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
		data = df[['Date','Open','High','Low','Close','Volume','VWAP']]
		df_vwap = df[['Date','VWAP']]
		df_vwap['Date'] = df_vwap['Date'].apply(pd.to_datetime)
		name=df['Symbol'][1]
		plt.figure(figsize=(16,8)) 
		plt.plot(df_vwap['VWAP'], label='VWAP') 
		plt.title('VWAP visualization for the company : '+name) 
		plt.xlabel("Time(year)") 
		plt.ylabel("Volume Weighted Average Price") 
		plt.legend(loc='best')
		return render_template("result.html",name=plt.plot(df_vwap['VWAP'], label='VWAP'),msg=msg ) 
	else:
		msg="The provided company data is not available"
		return render_template("notavail.html",msg=msg)
