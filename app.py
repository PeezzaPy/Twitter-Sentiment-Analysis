from flask import Flask, render_template, jsonify
from sentiment_analysis import analyze, load_model


app = Flask(__name__) 

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
    load_model()
    tweet_structures = analyze()
    return render_template('runandresult.html', tweet_structures=tweet_structures)


@app.route('/get_new_analysis')
def get_new_analysis():
    tweet_structures = analyze()  # Call your analyze function to get new results
    # Convert the results to a format suitable for JSON
    json_results = [
        {
            'username': tweet.username,
            'tweet': tweet.tweet,
            'analysis': {
                'Positive': tweet.analysis['Positive'],
                'Neutral': tweet.analysis['Neutral'],
                'Negative': tweet.analysis['Negative'],
            }
        }
        for tweet in tweet_structures
    ]
    return jsonify(json_results)


# Supporting Info in Webpage
@app.route('/terms-of-service')
def term():
    return render_template('term.html')

@app.route('/donate-gcash')
def donate():
    return render_template('donate.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')



if __name__ == '__main__':
    app.run(debug=True)
