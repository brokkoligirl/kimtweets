### Previously on Keeping up with the Kardashians:

This is a Jupyter notebook compiling information on Kim Kardashian's twitter activities. It's very much an ongoing project.

<b>Downloading Kim's entire twitter history using `tweet_grabber.py`:</b>

All the functions for downloading tweets into csv format are contained within `tweet_grabber.py`. 

Since the Twitter API only allows for the scraping of the last ~3500 or so tweets, Python's <a href="https://github.com/Mottl/GetOldTweets3">Get Old Tweets</a> module came in handy.

<hr>

#### Creating a new csv file with all available tweets:</b>

```python
grab_all_tweets(usr_name='KimKardashian', n=0, 
                filename='allkim.csv', mode='w')
```
`n` specifies the number of (most recent) tweets to be grabbed, will grab all available tweets if set to zero. 
Note that this can take up to 20+ minutes when used on an account with lots of tweets like Kim's.

<hr>

#### Appending new tweets to the file:

First, extract the most recent tweet date from the file using `get_last_tweet_date`:

```python
begin_date = get_last_tweet_date(filename='allkim.csv')
```
Then, run `grab_all_tweets` again, with `mode` set to `'a'` and `date_since` set to `begin_date`:

```python
grab_all_tweets(usr_name='KimKardashian', n=0, 
                filename='allkim.csv', mode='a', 
                date_since=begin_date)
```

And finally, finish off by dropping duplicates and sorting the file by date (in a descending fashion) with 
```python
drop_duplicates_and_sort(filename='allkim.csv')
```
<hr>

This literal gold mine now gives us access to ALL of Kim's tweets since the inception of her Twitter account on March 21st, 2009 when she tweeted:


<img src="screenshots/Kim_first_tweet.png" width="450" alt="Kim's first tweet" title="Kim's first tweet" align="center"/>

A true legend. 