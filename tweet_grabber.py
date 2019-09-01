import GetOldTweets3 as got
import csv
import datetime


def tweet_grabber(usr_name, n, filename):

    """
    returns a csv file with the last n tweets of a twitter user

    :param usr_name: twitter user name whose tweets we want to download
    :param n: maximum number of tweets to download. will grab all tweets if set to 0
    :param filename: name of the csv file to which the tweets will be saved

    depending on the amount of tweets in the account, this can take 20+ minutes
    """

    tweet_criteria = got.manager.TweetCriteria().setUsername(usr_name) \
                                                .setMaxTweets(n)

    tweets = got.manager.TweetManager.getTweets(tweet_criteria)

    column_names = ["username", "date", "retweets", "favorites", "text", "geo",
                    "mentions", "to", "hashtags", "id", "permalink"]

    counter = 0

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)

        for tweet in tweets:
            tweet_id = tweet.id
            permalink = tweet.permalink
            username = tweet.username
            to = tweet.to
            text = tweet.text
            date = tweet.date
            retweets = tweet.retweets
            favorites = tweet.favorites
            mentions = tweet.mentions
            hashtags = tweet.hashtags
            geo = tweet.geo

            tweetrow = [username, date, retweets, favorites, text, geo,
                        mentions, to, hashtags, tweet_id, permalink]

            writer.writerow(tweetrow)
            counter +=1

    print('finished saving tweets. total number of tweets downloaded: ', counter)


beginning = datetime.datetime.now()
print(beginning)
tweet_grabber('kimkardashian', 0, 'kim.csv')
ending = datetime.datetime.now()
print(ending)
