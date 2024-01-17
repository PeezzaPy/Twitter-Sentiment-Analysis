class TwitterUser:
    def __init__(self, username, tweet):
        self.username = username
        self.tweet = tweet
        self.analysis = {}

    def get_analysis(self, label, confidence):
        self.analysis[label] = confidence