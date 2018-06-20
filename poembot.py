import markovbot_2
from random import choice
import itertools
import tweepy
from collections import Counter
import yaml

# Get API credentials from apps.twitter.com and enter them here.
'''
consumer_key = '00000'
consumer_secret = '00000'
access_token = '00000'
access_token_secret = '00000'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

'''

# This is using yaml to store your config details. 
config = yaml.safe_load('~/.config/markovbot_2/emilymarkovson.yaml')
auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret']
auth.set_access_token(config['access_token'], config['access_token_secret'])
api = tweepy.API(auth)


def line_starter(text):
    '''
    Returns a random word that starts a line based on all of the words that
    start lines in Dickinson's poems more than once. It might be better to
    decrease the number of possible choices.
    '''
    line_list = text.split('\n')
    start_counts = []
    for line in line_list:
        line = line.strip().split()
        try:
            start_counts.append(line[0])
        except IndexError:
            pass
    start_counts = Counter(start_counts)
    words_greater_one = [x for x, y in start_counts.items() if y > 1]
    return choice(words_greater_one)



# Works from markovbot_2.py to generate four lines, turn them into a list,
# then convert that list into a string with line breaks (i.e. the poem). 
def poem_markovize():
    text = open("Dickinson_Poems.txt").read()
    markovizer = markovbot_2.Markovizer("Dickinson_Poems.txt", encoding="utf-8")
    poem = []
    for num_lines in itertools.repeat(None, 4):
        #line_start = choice(["I", "You", "And", "Then", "If", "Oh", "We",
        #                     "But", "Our", "He", "How", "Who", "When"])
        line_start = line_starter(text)
        line = markovizer.create_utterance(line_start, char_limit=40)
        poem.append(line[:-1])
    poem = '\n'.join(poem)
    print(poem)
    api.update_status(poem)


poem_markovize()

