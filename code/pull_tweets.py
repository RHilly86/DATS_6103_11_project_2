# NOTE: Data was pulled on 11/4/2020 at 10:06 PM
import tweepy
import pandas as pd
import sys

# Specify the path to our config file, which contains our Twitter API and secret keys
sys.path.append("project_2/code")
import config

# Authenticate ourselves using tweepy so we can scrape the feed of CARES Bot
auth = tweepy.OAuthHandler(config.api_key, config.secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

cares_bot_tweets = []

# Iteratively scrape the tweets from CARES Bot
for tweet in tweepy.Cursor(api.user_timeline, screen_name="ExtendCaresUI").items():
  cares_bot_tweets.append(tweet)
  
cares_bot = pd.Series()

# Since we only want the URL of the image, we'll normalize the JSON data and extract the media_url key, which
# has the image link as a URL
for tweet in cares_bot_tweets:
  try:
    cares_bot = cares_bot.append(pd.json_normalize(tweet._json, ["entities", "media"])["media_url"], 
                                 ignore_index=True)
    # It looks like some tweets don't have a media_url (perhaps when Data For Progress launched this bot, they had tweets with no image). Given
    # this, let's skip over these tweets
  except KeyError:
    continue

# Write out the image URLs to a CSV file so we have a static representation of the data that was pulled and so
# the scraper doesn't have to be rerun
cares_bot.to_csv("C:/Users/Rober/DATS_6103/project_2/data/cares_bot_image_urls.csv")

  
