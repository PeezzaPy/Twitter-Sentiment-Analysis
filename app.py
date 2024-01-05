from flask import Flask, redirect, url_for, render_template, request, session
from tweepy import API
import tweepy
import json

# Load Twitter API credentials from JSON file
with open('twitter_credentials.json', 'r') as file:
    twitter_credentials = json.load(file)

app = Flask(__name__) 
app.secret_key = "tweetimentanalysis"

# Set up Tweepy
auth = tweepy.OAuthHandler(twitter_credentials['api_key'], twitter_credentials['api_secret_key'], twitter_credentials['callback_url'])
api = tweepy.API(auth)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/acknowledgement')
def acknowledgement():
    return render_template('acknowledgement.html')

@app.route('/login')
def login():
    # Generate the Twitter authentication URL
    auth_url = auth.get_authorization_url()
    # Store the request token in the session for later use
    session['request_token'] = auth.request_token

    return redirect(auth_url)


@app.route('/logout')
def logout():
    del session['request_token']
    return redirect(url_for('index'))


@app.route('/callback')
def callback():
    # Retrieve the request token from the session
    request_token = session['request_token']
    del session['request_token']
    # Get access tokens using the verifier
    verifier = request.args.get('oauth_verifier')

    auth.request_token = request_token
    try:
        auth.get_access_token(verifier)
        api = API(auth)
        user = api.verify_credentials()
        
        # Store the access tokens in the session
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret

        return render_template('welcome.html', username=user.screen_name)

    except tweepy.TweepyException as e:
        print(f"Error: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
