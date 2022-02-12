import tweepy 
import csv
import Twitter_API_Credentials as cred


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
	auth.set_access_token(cred.access_key, cred.access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=500)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before {}".format(oldest))
        
		since = "2011-01-01"
        
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,since_id=since, max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...{} tweets downloaded so far".format(len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.user.screen_name, tweet.id_str, tweet.user.location, tweet.created_at, tweet.user.statuses_count, tweet.favorite_count,  tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('{}_tweets.csv'.format(screen_name), 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["User_name","Tweet_Id","Location","Created_at","Tweet_count","Like_count", "Text"])
		writer.writerows(outtweets)
		print('{}_tweets.csv was successfully created.'.format(screen_name))
	pass


if __name__ == '__main__':
	#username of the account to be extracted
	get_all_tweets("drjosflynn")