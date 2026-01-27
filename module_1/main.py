# Tonya Capillo
# Module 1: Personal Website

# an object of WSGI application
from flask import Flask, render_template

app = Flask(__name__) # Flask constructor

@app.route('/')

def home():
    return render_template('home.html')

@app.route('/contact')

def contact():
    return render_template('contact.html')

@app.route('/projects')

def contact():
    return render_template('projects.html')



if __name__ == '__main__':
    # Run the applicaiton
    app.run(host='0.0.0.0', port=8080)

