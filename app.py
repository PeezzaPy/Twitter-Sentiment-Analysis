from flask import Flask, render_template, jsonify
from sentiment_analysis import analyze, load_model
# from tweepy import API
# import tweepy
# import json

# # Load Twitter API credentials from JSON file
# with open('twitter_credentials.json', 'r') as file:
#     twitter_credentials = json.load(file)

# Set up Tweepy
# auth = tweepy.OAuthHandler(
#     twitter_credentials['api_key'], twitter_credentials['api_secret_key'], 
#     twitter_credentials['access_token'], twitter_credentials['access_token_secret']
# )
# api = tweepy.API(auth, wait_on_rate_limit=True)

app = Flask(__name__) 
# app.secret_key = "tweetimentanalysis"


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

# @app.route('/login')
# def login():
#     # Generate the Twitter authentication URL
#     auth_url = auth.get_authorization_url()
#     # Store the request token in the session for later use
#     session['request_token'] = auth.request_token

#     return redirect(auth_url)


# @app.route('/logout')
# def logout():
#     del session['request_token']
#     return redirect(url_for('index'))


# @app.route('/callback')
# def callback():
#     # Retrieve the request token from the session
#     request_token = session['request_token']
#     del session['request_token']
#     # Get access tokens using the verifier
#     verifier = request.args.get('oauth_verifier')

#     auth.request_token = request_token
#     try:
#         auth.get_access_token(verifier)
#         api = API(auth)
#         user = api.verify_credentials()
        
#         # Store the access tokens in the session
#         session['access_token'] = auth.access_token
#         session['access_token_secret'] = auth.access_token_secret

#         print(session['access_token'])
#         print(session['access_token_secret'])

#         # Post a tweet
#         tweet_text = "Hello, Twitter! This is my first tweet using Tweepy. #TweepyTutorial"

#         try:
#             api.update_status(status=tweet_text)
#             print("Tweet posted successfully!")
#         except tweepy.TweepyException as e:
#             print(f"Error posting tweet: {e}")

#         # search_query = "'Elon Musk''fired'-filter:retweets AND -filter:replies AND -filter:links"
#         # no_of_tweets = 20
#         # tweets = api.search_tweets(q=search_query, lang="en", count=no_of_tweets)
#         # attributes_container = [[tweet.user.name, tweet.created_at, tweet.full_text] for tweet in tweets]
#         # columns = ["User", "Date Created", "Tweet"]
#         # tweets_df = pd.DataFrame(attributes_container, columns)
#         # print(tweets_df)

#         return redirect(url_for('runandresult'))

    # except tweepy.TweepyException as e:
    #     print(f"Error: {e}")
    #     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
