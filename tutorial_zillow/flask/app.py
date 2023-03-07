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
        city = request.args.get('city')
        return render_template('data_collection.html', city=city)
    else:
        city = request.args.get('city')
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
        city = request.args.get('city')
        graph = mapbox(city)
        return render_template('visualization.html', city=city, graph = graph)
    else:
        city = request.args.get('city')
        graph = mapbox(city)
        return render_template('visualization.html', city=city, graph = graph)