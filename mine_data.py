import csv
import re

import redis
import tweepy
from keybert import KeyBERT

from redis_functions import save_tag

file = open("read_tweet_ids.csv", "r")
read_tweet_ids = list(csv.reader(file, delimiter=","))
file.close()
if read_tweet_ids:
    read_tweet_ids = read_tweet_ids[0]

client_id = "dzFTUnVsQzE2S2VoNHowNVZDd0M6MTpjaQ"
client_secret = "XJVwI8uejJD7QzMpL7z8OyOlOAuxuLj0Zjoob9QrA4gUfS4Ah-"
redirect_uri = "https://docs.tweepy.org/en/stable/index.html"

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri=redirect_uri,
    scope=["tweet.read", "tweet.write", "users.read"],
    client_secret=client_secret,
)

ignore_tags = [
    "Events [Entity Service]",
    "Entities [Entity Service]",
    "Unified Twitter Taxonomy",
    "Unified Twitter",
]
ignore_words = ["Vertical", "Taxonomy", "Category"]

print("Go to the following url and authenticate: \n")

print(oauth2_user_handler.get_authorization_url())

authorization_response = input("\nPaste the url you get after being redirected here: ")

access_token = oauth2_user_handler.fetch_token(authorization_response)

client = tweepy.Client(access_token["access_token"])

kw_model = KeyBERT()

r = redis.StrictRedis(
    host="localhost", port=6379, charset="utf-8", decode_responses=True
)

for tweet in tweepy.Paginator(
    client.get_home_timeline,
    max_results=100,
    user_auth=False,
    tweet_fields=["context_annotations"],
).flatten(limit=200):
    if str(tweet.id) in read_tweet_ids:
        continue
    text = re.sub(r"https?://\S+", "", tweet.text)
    keywords = [i[0] for i in kw_model.extract_keywords(text)]
    temp_list = []
    for t in tweet.context_annotations:
        tag = t["domain"]["name"]
        for w in ignore_words:
            if tag.find(w) != -1:
                tag = tag.replace(w, "")
                tag = tag.strip()
        if tag not in temp_list and tag not in ignore_tags:
            save_tag(r, tag, keywords)
            temp_list.append(tag)
    read_tweet_ids.append(tweet.id)

with open("read_tweet_ids.csv", "w") as file:
    wr = csv.writer(file)
    wr.writerow(read_tweet_ids)
