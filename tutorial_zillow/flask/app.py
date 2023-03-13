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
        d = getStats(city)
        bed=request.form["bed"]
        if bed:
            d['bed'] = bed
        bath=request.form["bath"]
        if bath:
            d['bath'] = bath
        sqft=request.form["sqft"]
        if sqft:
            d['sqft'] = sqft
        year_made=request.form["year_made"]
        if year_made:
            d['year_made'] = year_made
        home_type=request.form["home_type"]
        if home_type:
            d['home_type'] = home_type
        zipcode=request.form["zipcode"]
        if zipcode:
            d['zipcode'] = zipcode
        return render_template('data_collection.html', **d)
                            #    bed=bed, bath=bath, sqft=sqft,
                            #    year_made=year_made,
                            #    home_type=home_type,
                            #    zipcode=zipcode,
                            #    city=city)

def mapbox(name, **kwargs):
    """
    Creates a mapbox of all the data points scraped for the name (city name) parameter
    """

    df = pd.read_csv(f"Datasets/{name}.csv")

    for key, value in kwargs.items():
        if(key == "feature"):
            feature = value
        if(key == "number"):
            num = value
            if num != '':
                num = int(num)
                df = df[df[feature] == num]
        if(key == "feature_type"):
            feature_type = value
            if feature_type != []:
                df = df[df["homeType"].isin(feature_type)]
        if(key == "feature_min_max"):
            feature_min_max = value
        if(key == "min"):
            minimum = value
            if minimum != '':
                minimum = int(minimum)
                df = df[df[feature_min_max] >= minimum]
        if(key == "max"):
            maximum = value
            print(maximum, feature_min_max)
            if maximum != '':
                maximum = int(maximum)
                df = df[df[feature_min_max] <= maximum]

    fig = px.scatter_mapbox(df, 
                            hover_data = ["address/city","price", 'bathrooms', 'bedrooms',
                                          'homeType'],
                            lat = "latitude",
                            lon = "longitude", 
                            zoom = 8,
                            height = 600,
                            mapbox_style="open-street-map")

    fig.update_layout(margin={"r":30,"t":10,"l":30,"b":0})
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def density_mapbox(name, **kwargs):
    """
    Creates a mapbox of all the data points scraped for the name (city name) parameter
    """

    df = pd.read_csv(f"Datasets/{name}.csv")
    sample_size = df.shape[0]

    for key, value in kwargs.items():
        if(key == "feature"):
            feature = value
        if(key == "number"):
            num = value
            num = int(num)
            df = df[df[feature] == num]

    radius = 6 * sample_size // df.shape[0]

    fig = px.density_mapbox(df, 
                            hover_data = ["address/city","price", 'bathrooms', 'bedrooms'],
                            lat = "latitude",
                            lon = "longitude", 
                            zoom = 8,
                            radius = radius,
                            height = 600,
                            mapbox_style="open-street-map")

    fig.update_layout(margin={"r":30,"t":10,"l":30,"b":0})
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def histogram(name):

    df = pd.read_csv(f"Datasets/{name}.csv")
    fig = px.histogram(df, x="bedrooms")
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'POST':
        min = request.form.get("minimum")
        max = request.form.get('maximum')
        feature_min_max = request.form.get("features_min_max")
        feature_type = []
        if request.form.get("apartment"):
            feature_type.append(request.form.get("apartment"))
        if request.form.get("condo"):
            feature_type.append(request.form.get("condo"))
        if request.form.get("lot"):
            feature_type.append(request.form.get("lot"))
        if request.form.get("multi_family"):
            feature_type.append(request.form.get("multi_family"))
        if request.form.get("townhouse"):
            feature_type.append(request.form.get("townhouse"))
        feature = request.form.get("features")
        number = request.form.get("number")
        city = request.args.get('city')
        graph1 = mapbox(city, feature=feature, number=number,
                        feature_type=feature_type,
                        feature_min_max=feature_min_max,
                        min=min, max=max)
        graph2 = density_mapbox(city)
        return render_template('visualization.html', city=city, graph1 = graph1,
                               graph2=graph2)
    else:
        city = request.args.get('city')
        graph1 = mapbox(city)
        graph2 = density_mapbox(city)
        return render_template('visualization.html', city=city, graph1 = graph1,
                               graph2=graph2)

def clean(df):
    re_str = 'photos/'
    clean_df = df.drop(df.columns[df.columns.str.contains(re_str)], axis=1)
    clean_df = clean_df.drop(df.columns[df.columns.str.contains("address/community")], axis=1)
    return clean_df

@app.route('/view_data', methods=['GET','POST'])
def view_data():
    name = "Los Angeles" # default
    if request.method == 'POST':
        name = request.form["name"]
        data = pd.read_csv(f"Datasets/{name}.csv")
        clean_data = clean(data)
        pd.set_option('display.max_colwidth', 10)
        return render_template('view_data.html', tables=[clean_data.to_html()], titles=[''], city=name)
    else: 
        data = pd.read_csv("Datasets/Los Angeles.csv") # default
        clean_data = clean(data)
        return render_template('view_data.html', tables=[clean_data.to_html()], titles=[''], city=name)
    

def getStats(name):
    df = pd.read_csv(f"Datasets/{name}.csv")

    modes = df[['address/zipcode', 'homeType', 'bathrooms', 'bedrooms', 'yearBuilt']].mode()
    mode_zipcode = modes.iloc[0]['address/zipcode']
    mode_home_type = modes.iloc[0]['homeType']
    mode_bath = modes.iloc[0]['bathrooms']
    mode_bed = modes.iloc[0]['bedrooms']
    mode_year = modes.iloc[0]['yearBuilt']

    return {
        "zipcode": int(mode_zipcode),
        "home_type": mode_home_type,
        "bath": int(mode_bath),
        "bed": int(mode_bed),
        "year_made": int(mode_year),
        "sqft": 20000   # placeholder
    }

