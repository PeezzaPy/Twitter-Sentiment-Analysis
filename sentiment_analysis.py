from transformers import AutoTokenizer, AutoModelForSequenceClassification
from TwitterUser import TwitterUser
from scipy.special import softmax
import concurrent.futures
import asyncio
import pandas as pd

# Initialize variables for model
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = None
tokenizer = None

# Initialize variables
analyzed_tweet = []
dataset = []


def load_model():
    global roberta, model, tokenizer
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)


def load_csv(file):
    dataFrame = pd.read_csv(file, nrows=200000)
    random_row = dataFrame.sample(n=100)              # change depends on how many do you want to retrieve

    dataset = [(row[1], row[4], row[5]) for row in random_row.itertuples(index=False)]

    return dataset


def analyze():
    excel_file_path = "dataset/training.1600000.processed.noemoticon.csv"
    dataset = load_csv(excel_file_path)
    num_thread = 6

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_thread) as executor:
        chunk_size = len(dataset) // num_thread
        sub_datasets = [dataset[i:i + chunk_size] for i in range(0, len(dataset), chunk_size)]
        
        futures = [executor.submit(analyze_thread, sub_dataset) for sub_dataset in sub_datasets]

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

    return analyzed_tweet


def analyze_thread(tweets):
    for i in range(len(tweets)):
        tweet = tweets[i]

        twitter_user = TwitterUser(tweet[1], tweet[2])
        tweet_words = []

        for word in twitter_user.tweet.split(' '):        # load the tweet attribute
            if word.startswith('@') and len(word) > 1:
                word = '@user'

            elif word.startswith('http'):
                word = "http"
            tweet_words.append(word)

        tweet_proc = " ".join(tweet_words)

        # Load the model
        labels = ['Negative', 'Neutral', 'Positive']

        # sentiment analysis
        encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')

        output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])

        scores = output[0][0].detach().numpy()          # get the logits (raw scores) on first indexes
        scores = softmax(scores)                        # to get the confidence and probabilities

        for i in range(len(scores)):
            l = labels[i]
            s = round((float(scores[i]) * 100), 2)      # percentage with 2 decimal places
            twitter_user.get_analysis(l, s)
        
        # Append the temp_list 
        analyzed_tweet.append((twitter_user))
