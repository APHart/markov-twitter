"""Generate Markov text from text files.

    format for function call: python markov.py text_file n is_song 
    where: 
    n = number of links in markov chain, 
    is_song = True if song, otherwise defaulted to False"""

from random import choice
import twitter
import os
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as text:

        text = text.read()

    return text


def make_chains(text_string, n=2):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = text_string.split()

    #Adding None at the end of the list for stop flag in make_text funct.
    words.append(None)

    index = 0

    while index < (len(words) - n):

        #creates tuple of slice of words list, determined by n.
        key = tuple(words[index:index + n])

        if key in chains:

            #adding another value to the key
            chains[key].append(words[index + n])

        else:

            #adds key and value to chains dictionary
            chains[key] = [words[index + n]]

        index += 1

    return chains


def make_text(chains, n=2):
    """Return text from chains."""

    #Selects a random key from chains dictionary

    while True:
        key = choice(chains.keys())

    #only using key if it starts with a capital letter.
        if key[0].istitle():
            break

    words = []

    #Unpacks words from key tuple and adds them to words list
    for word in key:
        words.append(word)

    while True:

        #Selects random value for specified key
        rand_value = choice(chains[key])

        if rand_value is None:
            break

        else:

            #Adds word to words list
            words.append(rand_value)

            #Reassigns key to slice of original key, starting at index 1
            #(through to the end), concatenated with tuple of rand_value
            key = key[1:] + (rand_value,)

    return " ".join(words)


def make_twitter_ready(chains, n=2, is_song=False):
    """Takes in text, limits to 140 chars, ends with punctuation, returns text """

    #list of punctuation that is acceptable to end the tweet with
    punctuation = ['.', '?', '!']

    #Producting text
    text = make_text(chains, n)
    #Limit the text to 140 chars:
    text = text[:140]

    #Ensures tweet ends with punctuation:
    if is_song is False:

        while text[-1] not in punctuation:
            #if there is no punctuation in the entire 140 chars, make new text.
            if len(text) == 1:
                text = make_text(chains, n)
                text = text[:140]

            #removing the last character if not end of sentence punctuation.
            else:
                text = text[:-1]

    else:

        while text[-1] != ' ':
            #if string does not end with a space, removes last character
            text = text[:-1]

    return text


def send_tweet(file_path):
    """Takes a file, creates Markov chain and posts as tweet."""

    #Twitter app authentication
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # print api.VerifyCredentials()

    #Generating text string from file
    input_text = open_and_read_file(input_path)
    #Creates Markov chain dictionary
    chains = make_chains(input_text, n)

    print "This is the last tweet you posted:"
    last_text = api.GetUserTimeline(user_id=918221167332270080,count=1)
    print last_text(Text)

    while True:

        #Formatting chain string for Twitter
        our_tweet = make_twitter_ready(chains, n, is_song)
        print our_tweet
        print
        to_tweet = raw_input("Would you like to post this tweet?(y/n) ")

        if to_tweet.lower() == 'y':
            break

    status = api.PostUpdate(our_tweet)
    # print status.text


input_path = sys.argv[1]

n = int(sys.argv[2])

#check to see if the user types in something for is_song in command line
try:
    is_song = sys.argv[3]

#If the user doesn't type in anything, is_song automatically defaulted to False
except(IndexError):
    is_song = False


#calls send_tweet function in while loop to continue tweeting if desired.
while True:

    send_tweet(input_path)

    tweet_again = raw_input("Would you like to tweet again?(y/n) ")

    if tweet_again.lower() != 'y':
        break
