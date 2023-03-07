from flask import Flask, render_template, g, request
import pandas as pd
import plotly
from plotly import express as px
import sqlite3
import os
import json

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')  

@app.route('/data_collection', methods=['POST', 'GET'])
def data_collection():
    if request.method == 'GET':
        args = request.args
        print(args)
        return render_template('data_collection.html')
    else:
        bed=request.form["bed"]
        bath=request.form["bath"]
        sqft=request.form["sqft"]
        year_made=request.form["year_made"]
        home_type=request.form["home_type"]
        zipcode=request.form["zipcode"]
        return render_template('data_collection.html', 
                               bed=bed, bath=bath, sqft=sqft,
                               year_made=year_made,
                               home_type=home_type,
                               zipcode=zipcode)

def mapbox(name):
    """
    Creates a mapbox of all the data points scraped for the name (city name) parameter
    """
    df = pd.read_csv(f"Datasets/{name}.csv")
    fig = px.scatter_mapbox(df, 
                            hover_data = ["address/city","price", 'bathrooms', 'bedrooms'],
                            lat = "latitude",
                            lon = "longitude", 
                            zoom = 8,
                            height = 600,
                            mapbox_style="open-street-map")

    fig.update_layout(margin={"r":30,"t":10,"l":30,"b":0})
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'POST':
        name = request.form.get("name")
        graph = mapbox(name)
        return render_template('visualization.html', name=name, graph = graph)
    else:
        return render_template('visualization.html')

@app.route('/view_data', methods=['GET','POST'])
def view_data():
    data = pd.read_csv(f"Datasets/Los Angeles.csv")
    return render_template('view_data.html', tables=[data.to_html()], titles=[''])