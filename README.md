### Keeping up with Kim's Twitter account:

This is a Jupyter notebook compiling information on Kim Kardashian's 
twitter activities. It's very much an ongoing project.

<b>`tweet_grabber.py`</b> contains some useful functions to 
regularly harvest Kim's Twitter activities. The functions use 
<a href="https://tweepy.readthedocs.io/en/latest/">Tweepy</a>, 
the sort-of-official Python library for interacting with Twitter API, 
and, since the Twitter API only allows for the scraping of the last 
~3500 or so tweets, 
Python's <a href="https://github.com/Mottl/GetOldTweets3">Get Old 
Tweets</a> module came in handy.

<hr>

#### Creating a new csv file with all available tweets:</b>

```python
grab_all_tweets(usr_name='KimKardashian', n=0, 
                filename='allkim.csv', mode='w')
```
`n` specifies the number of (most recent) tweets to be grabbed, 
will grab all available tweets if set to zero. 
Note that this can take 20+ minutes when 
used on an account with lots of tweets like Kim's.

<hr>

#### Updating stats on the most recent tweets:

Since the most recent tweets could have been very fresh
when their data was downloaded, it might be useful to
go back over them and update their favorite and retweet counts
before going in and adding the newest tweets to the file.
For this, we're using the official Twitter API, so we need
to fill in our credentials:

```python
c_key, c_secret, a_token, a_token_secret = get_twitter_tokens()
api = twitter_auth(c_key, c_secret, a_token, a_token_secret)

update_stats_for_recent_tweets(filename, api, num)
```
<hr>

#### Appending new tweets to the file:

First, extract the most recent tweet date from the file:

```python
begin_date = get_last_tweet_date(filename='allkim.csv')
```
Then, run `grab_all_tweets` again, with `mode` 
set to `'a'` and `date_since` set to `begin_date`:

```python
grab_all_tweets(usr_name='KimKardashian', n=0, 
                filename='allkim.csv', mode='a', 
                date_since=begin_date)
```

And finally, finish off by dropping duplicates 
and sorting the file by date (in a descending fashion) with 
```python
drop_duplicates_and_sort(filename='allkim.csv')
```
<hr>

This literal gold mine now gives us access to ALL 
of Kim's tweets since the inception of her Twitter 
account on March 21st, 2009 when she tweeted:


<img src="screenshots/Kim_first_tweet.png" width="450" 
alt="Kim's first tweet" title="Kim's first tweet" align="center"/>

A true legend. 