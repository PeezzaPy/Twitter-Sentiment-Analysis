from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

tweet = "I love shopping at @smsupermalls, It is easy to locate stores and make transactions 💖. more on https://smstore.com"

# pre-process tweet
tweet_words = []

for word in tweet.split(' '):
    if word.startswith('@') and len(word) > 1:
        word = '@user'

    elif word.startswith('http'):
        word = "http"
    tweet_words.append(word)

tweet_proc = " ".join(tweet_words)

print("Tweet: " + tweet)
print("\n")
print("Processed: = " + tweet_proc)

# load the model
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# sentiment analysis
encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')

output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])

scores = output[0][0].detach().numpy()
scores = softmax(scores)

print("\n")
for i in range(len(scores)):
    l = labels[i]
    s = scores[i]
    print(l, s)
