from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd

# Initialize variables
dataset = []
tweet_words = []

def load_csv(file):
    dataFrame = pd.read_csv(file, nrows=200000)
    random_row = dataFrame.sample(n=20)
    
    for i in range(len(random_row)):
        id = random_row.iloc[i, 1]
        user = random_row.iloc[i, 4]
        tweet = random_row.iloc[i, 5]
        dataset.append((id, user, tweet))

    return dataset

# Load csv (excel) file
excel_file_path = "dataset/training.1600000.processed.noemoticon.csv"
dataset = load_csv(excel_file_path)

# Load each row
for i in range(len(dataset)):
    tweet = dataset[i]      # load each row
    for word in tweet[2].split(' '):        # load the tweet element (third column)
        if word.startswith('@') and len(word) > 1:
            word = '@user'

        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)

    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"Username: {tweet[1]}  |  Tweet: {tweet[2]} ")
    
    # print("\n")
    # print("Processed: = " + tweet_proc)


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
        s = scores[i]
        print(l, s)


