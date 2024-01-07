from flask import Flask, redirect, url_for, render_template, request 
from sentiment_analysis import analyze

app = Flask(__name__) 
app.secret_key = "tweetimentanalysis"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/acknowledgement')
def acknowledgement():
    return render_template('acknowledgement.html')

@app.route('/main')
def runandresult():
    tweet_structures = analyze()
    return render_template('runandresult.html', tweet_structures=tweet_structures)

if __name__ == '__main__':
    app.run(debug=True)
