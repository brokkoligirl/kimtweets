import GetOldTweets3 as Got3
import csv
import datetime
import pandas as pd
import tweepy
import configparser


def grab_all_tweets(usr_name, n, filename, mode='w', date_since=None):

    """
    returns a csv file with the n most recent tweets of a twitter user

    :param usr_name: twitter user name whose tweets are to be downloaded
    :param n: maximum number of tweets to download. will grab all avilable tweets if set to 0
    :param filename: name of the csv file to which the tweets will be saved
    :param date_since: (str. "yyyy-mm-dd"): lower bound date (UTC) to restrict search. default is None.
    :param mode: a or w

    depending on the amount of tweets in the account, this can take 20+ minutes
    """

    if date_since is None:

        tweet_criteria = Got3.manager.TweetCriteria().setUsername(usr_name) \
                                                     .setMaxTweets(n)

    else:

        tweet_criteria = Got3.manager.TweetCriteria().setUsername(usr_name) \
                                                     .setMaxTweets(n) \
                                                     .setSince(date_since)

    tweets = Got3.manager.TweetManager.getTweets(tweet_criteria)

    column_names = ["username", "date", "retweets", "favorites", "text", "geo",
                    "mentions", "hashtags", "id", "permalink"]

    counter = 0

    with open(filename, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)
        if mode == 'w':
            writer.writerow(column_names)

        for tweet in tweets:
            tweet_id = tweet.id
            permalink = tweet.permalink
            username = tweet.username
            text = tweet.text
            date = tweet.date
            retweets = tweet.retweets
            favorites = tweet.favorites
            mentions = tweet.mentions
            hashtags = tweet.hashtags
            geo = tweet.geo

            tweetrow = [username, date, retweets, favorites, text, geo,
                        mentions, hashtags, tweet_id, permalink]

            writer.writerow(tweetrow)
            counter += 1

    print('finished saving tweets. total number of tweets downloaded: ', counter)


def get_last_tweet_date(filename):
    """
    returns the date of the most recent tweet in the csv file as a string "YYYY-MM-DD"
    :param filename:
    """

    df = pd.read_csv(filename, sep=',', usecols=['date'])
    most_recent_tweet_date = df['date'].sort_values(ascending=False).reset_index(drop=True)[0]
    return most_recent_tweet_date.split()[0]


def drop_duplicates_and_sort(filename):
    """
    drops duplicate tweets and sorts the csv file by date in a descending order
    :param filename:
    :return:
    """

    df = pd.read_csv(filename)
    df.drop_duplicates(subset="id", inplace=True)
    df.sort_values(by=['date'], ascending=False, inplace=True)
    df.to_csv(filename, index=False)


def get_twitter_tokens(filename='config.ini'):
    """
    fetches twitter API tokens from config file
    :return: c_key, c_secret, a_token, a_token_secret
    """

    config = configparser.ConfigParser()
    config.read(filename)
    c_key = config['TWITTER']['consumer_key']
    c_secret = config['TWITTER']['consumer_secret']
    a_token = config['TWITTER']['access_token']
    a_token_secret = config['TWITTER']['access_token_secret']

    return c_key, c_secret, a_token, a_token_secret


def twitter_auth(c_key, c_secret, a_token, a_token_secret):
    """
    function for twitter authentication.
    :return: tweepy.API object
    """

    auth = tweepy.OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token, a_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def update_stats_for_recent_tweets(filename, api, num):

    df = pd.read_csv(filename)
    df.sort_values(by=['date'], ascending=False, inplace=True)
    df.reset_index(drop=True)
    for i in range(num):
        tweet_id = df.iloc[i]['id']
        status = api.statuses_lookup([tweet_id])
        df.at[i, "favorites"] = status[0].favorite_count
        df.at[i, "retweets"] = status[0].retweet_count

    df.to_csv(filename, index=False)


if __name__ == '__main__':

    filename = 'allkim.csv'

    c_key, c_secret, a_token, a_token_secret = get_twitter_tokens()
    api = twitter_auth(c_key, c_secret, a_token, a_token_secret)

    update_stats_for_recent_tweets(filename, api, 40)

    begin_date = get_last_tweet_date(filename)

    grab_all_tweets(usr_name='kimkardashian', n=0, filename=filename,
                    mode="a", date_since=begin_date)

    drop_duplicates_and_sort(filename)



