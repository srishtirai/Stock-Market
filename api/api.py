from flask import Flask,render_template,request
import numpy as np 
import pandas as pd 
import os

# print(os.listdir("C:/Users/RAI/Desktop/Final Project/Dataset"))
app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route("/result",methods=["POST"])
def result():
	name=request.form.get("name")

	return render_template("result.html",name=name) 
