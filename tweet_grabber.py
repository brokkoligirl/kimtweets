import GetOldTweets3 as Got3
import csv
import datetime


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


if __name__ == '__main__':

    beginning = datetime.datetime.now()
    print(beginning)
    grab_all_tweets('kimkardashian', 0, 'allkim_copy_for_use.csv', "a", "2019-07-22")
    ending = datetime.datetime.now()
    print(ending)
