from instapy import InstaPy
from instapy import smart_run
from random import shuffle
import random
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

credentials_file = 'credentials.json'
themes_file = 'themes.txt'
hashtags_file = 'hashtags.txt'
comments_file = 'comments.txt'
num_sessions = int(1e7)
session_sleep = 2.5*10*60 #seconds
power_nap_sleep = 2.5*2*60 #seconds

def power_nap():
	sleep_time = random.randint(power_nap_sleep,3*power_nap_sleep)
	print("Taking a nap for "+str(sleep_time)+" seconds.!!")
	time.sleep(sleep_time)
	return

def run_theme_based_smart_tags(session,themes):
	print("<<<RUNNING IN SMART MODE>>>")
	shuffle(themes)
	for theme in themes:
		mode = 'top' if random.randint(1,101)%2 else 'random'
		try:
			print("THEME ::::::: "+theme)
			session.set_smart_hashtags([theme], limit=10, sort=mode, log_tags=True)
			session.like_by_tags(amount=11, use_smart_hashtags=True, interact=True)
			power_nap()
		except:
			sys.stderr.write("Exception occured!\n")
	return

def run_custom_hastags(session,hashtags):
	print("<<<RUNNING IN CUSTOM MODE>>>")
	shuffle(hashtags)
	for hashtag in hashtags:
		print("TAG ::::::: "+hashtag)
		session.like_by_tags([hashtag], amount=11, randomize=True, interact=True)
		power_nap()
	return

def get_file_contents(filepath):
	with open(filepath) as file:
		lines = file.readlines()
	lines = [line.strip() for line in lines]
	return lines

def tune_session(session, min_followers, like_percentage, comment_percetage):
	session.set_relationship_bounds(enabled=True,delimit_by_numbers=True,max_followers=100000,min_followers=min_followers,min_following=100,min_posts=100)
	session.set_do_like(enabled=True, percentage=like_percentage)
	session.set_do_comment(enabled=True, percentage=comment_percetage)
	session.set_do_follow(enabled=True, percentage=1, times=1)
	session.set_quota_supervisor(enabled=True,
                            sleep_after=["likes", "follows", "comments_d"],
                            sleepyhead=True, stochastic_flow=True,
                            notify_me=True,
                            peak_likes=(100, 1000),
                            peak_comments=(21, 250),
                            peak_follows=(200, None))

themes = get_file_contents('themes.txt')
hashtags = get_file_contents('hashtags.txt')
comments = get_file_contents('comments.txt')

tailmsg = "Don't forget to checkout my page :) @freeze_francis."
#tailmsg = "Have a great day!"
comments = [comment.strip()+' '+tailmsg for comment in comments]

with open(credentials_file) as file:
    credentials = json.load(file)

insta_username = credentials['username']
insta_password = credentials['password']

for i in range(num_sessions):
	try:
		session = InstaPy(username=insta_username,
		                  password=insta_password,
		                  headless_browser=False)
		with smart_run(session):
			
			shuffle(comments)
			tune_session(session,1000,100,100)
			session.set_comments(comments)

			if random.randint(1,101) >= 50:
				run_theme_based_smart_tags(session,themes)
			else:
				run_custom_hastags(session,hashtags)
			#session.unfollow_users(amount=50, nonFollowers=True, style="RANDOM", unfollow_after=42*60*60, sleep_delay=700)
	except:
		sys.stderr.write("Exception occured in session!\n")
	time.sleep(random.randint(session_sleep,2*session_sleep))
