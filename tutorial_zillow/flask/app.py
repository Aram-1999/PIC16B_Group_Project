from flask import Flask, render_template, g, request
import sqlite3

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

@app.route('/visualization')
def visualization():
    return render_template('visualization.html')