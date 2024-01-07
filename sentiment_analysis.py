from transformers import AutoTokenizer, AutoModelForSequenceClassification
from TwitterUser import TwitterUser
from scipy.special import softmax
import pandas as pd

# Initialize variables
analyzed_tweet = []
dataset = []
tweet_words = []


def load_csv(file):
    dataFrame = pd.read_csv(file, nrows=200000)
    random_row = dataFrame.sample(n=3)              # change depends on how many do you want to retrieve

    for i in range(len(random_row)):
        id = random_row.iloc[i, 1]
        user = random_row.iloc[i, 4]
        tweet = random_row.iloc[i, 5]
        dataset.append((id, user, tweet))

    return dataset


def analyze():
    # Load csv (excel) file
    excel_file_path = "dataset/training.1600000.processed.noemoticon.csv"
    dataset = load_csv(excel_file_path)

    # Load each row
    for i in range(len(dataset)):
        tweet = dataset[i]      # load each row
        twitter_user = TwitterUser(tweet[1], tweet[2])
        for word in twitter_user.tweet.split(' '):        # load the tweet element (third column)
            if word.startswith('@') and len(word) > 1:
                word = '@user'

            elif word.startswith('http'):
                word = "http"
            tweet_words.append(word)

        tweet_proc = " ".join(tweet_words)


        # Load the model
        roberta = "cardiffnlp/twitter-roberta-base-sentiment"
        model = AutoModelForSequenceClassification.from_pretrained(roberta)
        tokenizer = AutoTokenizer.from_pretrained(roberta)

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

    # return analyzed_tweet
    return analyzed_tweet

