import praw
import json
import requests
import tweepy
import time

access_token = 'Your_code_here'
access_token_secret = 'Your_code_here'
consumer_key = 'Your_code_here'
consumer_secret = 'Your_code_here'

#PRAW: The Python Reddit Api Wrapper
def setup_connection_reddit(subreddit):
	print "Setting up connection with Reddit"
	r = praw.Reddit('Sedaghat_python reddit twitter bot ')
	subreddit = r.get_subreddit(subreddit)
	return subreddit

def tweet_creator(subreddit_info):
	post_dict = {}
	post_ids = []
	print "Getting posts from Reddit"
	# Limits the number of posts to 3
	for submission in subreddit_info.get_hot(limit=3):
                # strip_title function is defined later
		post_dict[strip_title(submission.title)] = submission.url
		post_ids.append(submission.id)
	print "Generating short link using goo.gl"
	mini_post_dict = {}
	for post in post_dict:
		post_title = post
		post_link = post_dict[post]   
                # The shorten function is defined in the next function		
		short_link = shorten(post_link)
		mini_post_dict[post_title] = short_link 
	return mini_post_dict, post_ids

#Uses the Google UrlShortener API
def shorten(url):
	headers = {'content-type': 'application/json'}
	payload = {"longUrl": url}
	url = "https://www.googleapis.com/urlshortener/v1/url"
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	link = json.loads(r.text)['id']
	return link

#Makes the title fit Twitter's character limit
def strip_title(title):
	if len(title) < 94:
		return title
	else:
		return title[:93] + "..."

def add_id_to_file(id):
	with open('posted_posts.txt', 'a') as file:
		file.write(str(id) + "\n")

def duplicate_check(id):
	found = 0
	with open('posted_posts.txt', 'r') as file:
		for line in file:
			if id in line:
				found = 1
	return found

def tweeter(post_dict, post_ids):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	for post, post_id in zip(post_dict, post_ids):
		found = duplicate_check(post_id)
		if found == 0:
			print "Posting this link on twitter"
			print post+" "+post_dict[post]
			api.update_status(post+" "+post_dict[post])
			add_id_to_file(post_id)
			time.sleep(30)
		else:
			print "Already posted"

def main():
	subreddit = setup_connection_reddit('Sports')
	post_dict, post_ids = tweet_creator(subreddit)
	tweeter(post_dict, post_ids)

if __name__ == '__main__':
	main()
