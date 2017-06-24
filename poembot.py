import markovbot_2
from random import choice
import itertools
import tweepy


# Get API credentials from apps.twitter.com and enter them here.
consumer_key = '00000'
consumer_secret = '00000'
access_token = '00000'
access_token_secret = '00000'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Works from markovbot_2.py to generate four lines, turn them into a list,
# then convert that list into a string with line breaks (i.e. the poem). 
def poem_markovize():
    markovizer = markovbot_2.Markovizer("Dickinson_Poems.txt", encoding="utf-8")
    poem = []
    for num_lines in itertools.repeat(None, 4):
        line_start = choice(["I", "You", "And", "Then", "If", "Oh", "We",
                             "But", "Our", "He", "How", "Who", "When"])
        line = markovizer.create_utterance(line_start, char_limit=40)
        poem.append(line[:-1])
    poem = '\n'.join(poem)
    print(poem)
    api.update_status(poem)


poem_markovize()

