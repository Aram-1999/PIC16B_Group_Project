from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')  

@app.route('/data_collection')
def data_collection():
    args = request.args
    return args
    return render_template('data_collection.html')

@app.route('/visualization')
def visualization():
    return render_template('visualization.html')