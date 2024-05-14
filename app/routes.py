from app import app
from flask import Flask, render_template

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
    

