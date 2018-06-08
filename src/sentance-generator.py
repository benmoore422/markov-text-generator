import sys 
import re
import random
import tweepy
from keys import *

# open file and remove double lines
def read_file(filename):
    with open(filename, "r") as file:
        contents = file.read().replace('\n\n', ' ').replace('\n', ' ')
    return contents

def make_chain(txt, chain = {}):
    words = txt.split(' ')
    i = 1

    for word in words[i:]:
        key = words[i - 1]
        if key in chain:
            chain[key].append(word)
        else:
            chain[key] = [word]
        i += 1

    print(chain)
    return chain


def generate_message(chain, count = 100):
    word1 = random.choice(list(chain.keys()))
    message = word1.capitalize()

    while len(message.split(' ')) < count:
        word2 = random.choice(chain[word1])
        word1 = word2
        message += ' ' + word2

    return message


def write_file(filename, message):
    with open(filename, "w") as file:
        file.write(message)

def twitter_authenticate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)

def clean_tweet(tweet):
    return re.sub(r"(?:\@|https?\://)\S+", "", tweet)


def get_users_tweets(username):
    usr_tweets = []
    api = twitter_authenticate()

    tweets = api.user_timeline(screen_name = username, count = 100, include_rts = False)

    for status in tweets:
        usr_tweets.append(clean_tweet(status.text))

    return " ".join(usr_tweets)



def main():
    tweets = get_users_tweets(sys.argv[1]) + get_users_tweets(sys.argv[2])
    chain = make_chain(tweets)
    message = generate_message(chain)
    write_file("output.txt", message)


if __name__ == '__main__':
    main()
