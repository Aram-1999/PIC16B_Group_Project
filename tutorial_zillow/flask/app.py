from flask import Flask, render_template, g, request
import pandas as pd
import plotly
from plotly import express as px
import sqlite3
import os
import json
import numpy as np
from scipy import stats
from flask import Flask, session
import plotly.express.colors
import pickle

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def main():
    return render_template('base.html')  

@app.route('/data_collection', methods=['POST', 'GET'])
def data_collection():
    '''
    Renders template for data collection
    Uses model to predict house price from user input
    '''

    if request.method == 'GET':
        city = request.args.get('city')
        return render_template('data_collection.html', city=city,
                               prediction = False)
    else:
        # if user submits form
        city = request.args.get('city')
        bed=request.form["bed"]
        session['bed_info'] = bed
        bath=request.form["bath"]
        session['bath_info'] = bath
        sqft=request.form["sqft"]
        session['sqft_info'] = sqft
        year_made=request.form["year_made"]
        home_type = request.form['home_type']
        zipcode = str(request.form["zipcode"])
        
        with open('Model/model1.pkl', 'rb') as f:
            model = pickle.load(f)
        
        price = model.predict(pd.DataFrame({
            'address/zipcode': [zipcode],
            'bathrooms': [bed],
            'bedrooms': [bath]
        }))

        return render_template('data_collection.html', city = city,
                               prediction = True,
                               price = int(price[0]),
                               bed=bed, bath=bath, sqft=sqft,
                               year_made=year_made,
                               home_type=home_type,
                               zipcode=zipcode)

def mapbox(name, **kwargs):
    """
    Creates a mapbox of all the data points scraped for the name (city name) parameter
    """

    df = pd.read_csv(f"Datasets/{name}.csv")
    center = {'lat': np.mean(df['latitude']), 'lon': np.mean(df['longitude'][0])}

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
                            center = center, 
                            hover_data = ["address/city","price", 'bathrooms', 'bedrooms',
                                          'homeType'],
                            lat = "latitude",
                            lon = "longitude", 
                            zoom = 8,
                            height = 600,
                            mapbox_style=kwargs.pop("style", "open-street-map"))

    fig.update_layout(margin={"r":30,"t":10,"l":30,"b":0})
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def density_mapbox(name, **kwargs):
    """
    Creates a mapbox of all the data points scraped for the name (city name) parameter
    """

    df = pd.read_csv(f"Datasets/{name}.csv")
    sample_size = df.shape[0]
    center = {'lat': np.mean(df['latitude']), 'lon': np.mean(df['longitude'][0])}


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

    
    if df.shape[0] != 0:
        radius = 5 * int(np.log2((sample_size + df.shape[0]) / df.shape[0]))
        if radius < 1:
            radius = 1
    else:
        radius = 1
    fig = px.density_mapbox(df, 
                            center = center,
                            hover_data = ["address/city","price", 'bathrooms', 'bedrooms'],
                            lat = "latitude",
                            lon = "longitude", 
                            zoom = 8,
                            radius = radius,
                            height = 600,
                            mapbox_style=kwargs.pop("style", "open-street-map"))

    fig.update_layout(margin={"r":30,"t":10,"l":30,"b":0})
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def cleaning(name):
    df = pd.read_csv(f"Datasets/{name}.csv")
    df = df[(np.abs(stats.zscore(df["price"])) <3)]
    df["bathrooms"] = df["bathrooms"].round()
    df = df[df["bathrooms"] < 30]
    df = df[df["bedrooms"] < 30]
    df = df[df["livingArea"] < 25000]
    df["livingArea"] = round(df["livingArea"] / 500.0) *500
    return df

def histogram_count(name, feature, user_info, color):
    df = cleaning(name)
    highest_value = 450
    fig = px.histogram(df, x=feature, width = 500, color_discrete_sequence=color)
    fig.add_shape(type="line",x0=user_info, y0=0, x1=user_info, y1=highest_value,line=dict(color="red", width=3, dash="dash"))
    fig.add_annotation(x=user_info, y=highest_value, ax=0, ay=-40,text="Your Data",arrowhead=1, arrowwidth=3, showarrow=True)
    fig.update_traces(marker_line_color="black", marker_line_width=1, opacity=0.7)
    if feature == "livingArea":
        fig.update_layout(title={"text": "Square Footage ", "x": 0.5}, yaxis_title="Count")
    else: 
        fig.update_layout(title={"text": "Number of " + feature, "x": 0.5}, yaxis_title="Count")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



def histogram_price(name, feature, user_info, color):
    df = cleaning(name)
    median_price = df[[feature,"price"]].groupby(feature).median().round(0)
    highest_value = int(median_price.max())
    fig = px.histogram(median_price, width =500, x=median_price.index, y="price", nbins =30, color_discrete_sequence=color)
    fig.add_shape(type="line", x0=user_info, y0=0, x1=user_info, y1=highest_value, line=dict(color="red", width=3, dash="dash"))
    fig.add_annotation(x=user_info, y=highest_value, ax=0, ay=-40,text="Your Data",arrowhead=1, arrowwidth=3, showarrow=True)
    fig.update_traces(marker_line_color="black", marker_line_width=1, opacity=0.7)
    if feature == "livingArea":
        fig.update_layout(title={"text": "Median Price of Homes vs Square Footage" , "x": 0.5}, yaxis_title="Price")
    else:
        fig.update_layout(title={"text": "Median Price of Homes vs " + feature, "x": 0.5}, yaxis_title="Price")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def scatterplot_count(name, feature1, feature2, user_info):
    df = cleaning(name)
    offset = 1
    scatter_1 = df.groupby([feature1, feature2]).size().reset_index().rename(columns={0:'count'})
    fig = px.scatter(scatter_1, x = feature1, y = feature2, color = "count", color_continuous_scale=px.colors.sequential.Plotly3_r, range_color = [1,100], width = 500)
    if feature2 == "livingArea":
        offset = 550
        fig.update_layout(title={"text": "Amount of " + feature1 + " vs Square Footage", "x": 0.5})
        fig.add_shape(type="circle",x0=int(user_info[0])-1, x1=int(user_info[0])+1, y0 = int(user_info[1])-offset, y1 = int(user_info[1])+offset)
    else: 
        fig.add_shape(type="circle",x0=int(user_info[0])-1, x1=int(user_info[0])+1, y0 = int(user_info[1])-offset, y1 = int(user_info[1])+offset)
        fig.update_layout(title={"text": "Amount of " + feature1 + " vs Amount of " + feature2, "x": 0.5})
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/morevisualization')
def morevisualization():
    '''
    renders template for data visualization page
    '''
    # set default values if user didn't submit anything
    city = session.get('city_info')
    default = getStats(city)
    bed = session.get('bed_info') if session.get('bed_info') else default['bed']
    bath = session.get('bath_info') if session.get('bath_info') else default['bath']
    sqft = session.get('sqft_info') if session.get('sqft_info') else default['sqft']
    
    # create histograms
    graph1 = histogram_count(name =session.get('city_info'), feature = "bedrooms", user_info = bed, color = ['indianred'])
    graph2 = histogram_count(name =session.get('city_info'), feature = "bathrooms", user_info =  bath, color = ["#4083f7"])
    graph3 = histogram_count(name =session.get('city_info'), feature = "livingArea", user_info =  sqft, color = ['#42c947'])
    graph4 = histogram_price(name =session.get('city_info'), feature = "bedrooms", user_info =  bed, color = ["indianred"])
    graph5 = histogram_price(name =session.get('city_info'), feature = "bathrooms", user_info =  bath, color = ["#4083f7"])
    graph6 = histogram_price(name =session.get('city_info'), feature = "livingArea", user_info =  sqft, color = ['#42c947'])
    
    # create scatterplots
    graph7 = scatterplot_count(name=session.get('city_info'), feature1 = "bedrooms", feature2 = "bathrooms", user_info = [bed, bath])
    graph8 = scatterplot_count(name=session.get('city_info'), feature1 = "bedrooms", feature2 = "livingArea", user_info = [bed, sqft])
    graph9 = scatterplot_count(name=session.get('city_info'), feature1 = "bathrooms", feature2 = "livingArea", user_info = [bath, sqft])

    return render_template('morevisualization.html', city = session.get('city_info'), graph1 = graph1, graph2 = graph2, graph3 = graph3, graph4=graph4, graph5=graph5, graph6=graph6, graph7=graph7, graph8=graph8, graph9=graph9)

@app.route('/visualization', methods=['GET', 'POST'])
def visualization():
    city = request.args.get('city')
    session['city_info'] = city
    if request.method == 'POST':
        min = request.form.get("minimum")
        max = request.form.get('maximum')
        feature_min_max = request.form.get("features_min_max")
        style = request.form.get("style")
        print(style)
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
                        min=min, max=max, style=style)
        graph2 = density_mapbox(city, feature=feature, number=number,
                        feature_type=feature_type,
                        feature_min_max=feature_min_max,
                        min=min, max=max, style=style)
        return render_template('visualization.html', city=city, graph1 = graph1,
                               graph2=graph2)
    else:
        city = request.args.get('city')
        graph1 = mapbox(city)
        graph2 = density_mapbox(city)
        return render_template('visualization.html', city=city, graph1 = graph1,
                               graph2=graph2)

def clean(df):
    '''
    This function will clean each city's dataset
    Args:
    df: the dataset of a city
    Return:
    cleaned dataset that no longer contains columns that are not needed (such as photos)
    '''
    re_str = 'photos/' # use this string to drop all 'photos' columns
    clean_df = df.drop(df.columns[df.columns.str.contains(re_str)], axis=1)
    clean_df = clean_df.drop(df.columns[df.columns.str.contains("address/community")], axis=1) # drop empty column
    return clean_df

@app.route('/view_data', methods=['GET','POST'])
def view_data():
    '''
    This function will display the dataset of a selected city
    Return:
    an html-rendered table that contains all data of a particular city
    '''
    city = session.get('city_info')
    if request.method == 'POST':
        city = request.form["name"]
        data = pd.read_csv(f"Datasets/{city}.csv")
        clean_data = clean(data)
        pd.set_option('display.max_colwidth', 10)
        return render_template('view_data.html', tables=[clean_data.to_html()], titles=[''], city=city)
    else: 
        data = pd.read_csv(f"Datasets/{city}.csv") # default
        clean_data = clean(data)
        return render_template('view_data.html', tables=[clean_data.to_html()], titles=[''], city=city)
    
def getStats(name):
    '''
    Returns dictionary of statistics for a city to use as default values
    '''

    # get data frame for given city
    df = pd.read_csv(f"Datasets/{name}.csv")

    # get mode values
    modes = df[['address/zipcode', 'homeType', 'bathrooms', 'bedrooms', 'yearBuilt', 'livingArea']].mode()
    mode_zipcode = modes.iloc[0]['address/zipcode']
    mode_home_type = modes.iloc[0]['homeType']
    mode_bath = modes.iloc[0]['bathrooms']
    mode_bed = modes.iloc[0]['bedrooms']
    mode_year = modes.iloc[0]['yearBuilt']
    mode_area = modes.iloc[0]['livingArea']

    # return dictionary
    return {
        "zipcode": int(mode_zipcode),
        "home_type": mode_home_type,
        "bath": int(mode_bath),
        "bed": int(mode_bed),
        "year_made": int(mode_year),
        "sqft": int(mode_area)  
    }
