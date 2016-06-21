import tweepy
import os
import random

consumer_key =  ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

path = "path_to_directory"
im = (path + "/" + random.choice(os.listdir(path)))
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
api.update_with_media(im, 'Your daily dose of Dilbert #dilbert')
