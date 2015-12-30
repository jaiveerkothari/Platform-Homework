from django.shortcuts import render
from django.template import loader
from json import loads
import json
# Create your views here.
from django.http import HttpResponse
from .models import TwitterAccounts
import oauth2
import time
import calendar


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    CONSUMER_KEY="fx95oKhMHYgytSBmiAqQ"
    CONSUMER_SECRET="0zfaijLMWMYTwVosdqFTL3k58JhRjZNxd2q0i9cltls"


    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    
    return content
 

def getUnixTime(utc_time):
	temp=time.strptime(utc_time, "%a %b %d %H:%M:%S +0000 %Y")
	return calendar.timegm(temp)

def isValid(t_id):
	"""
	check if id is valid
	"""
	str_id=str(t_id).strip()
	return str_id.isdigit()

	# if not (type(t_id) == int):
	# 	# input id is not a integer. input is invalid

	# user=TwitterAccounts.objects.filter(twitter_id=in_twitter_id)

def index(request):
	template=loader.get_template('tweets/index.html')
	context={}
	return render(request, 'tweets/index.html', context)


#### create 1 view url that takes input, and then make it direct to a restful url that returns the json    


def homeTimeline(request):
	# raise a 404 if id doesnt exist, or just return a json with an error?
	#initially lets make this return the timeline for the given user. no input at this stage

	#get oath token and scret from the db instead of hardcoding
	#in_twitter_id=2305278779
	#print "request.GET is ......",request.GET
	#print "request.GET['t_id'] is ...",request.GET['t_id']
	
	in_twitter_id=request.GET.get('t_id',0)

	#perform validation check

	l=[]
	print "type is " ,type(in_twitter_id)
	# validate the input 
	

	# error if in_twitter_id is not an int. so check that first. 

	if not (isValid(in_twitter_id)):
		d={}
		d['error']="twitter id given is not valid"
		l.append(d)
	else:
		t=str(in_twitter_id).strip()
		u1=TwitterAccounts.objects.filter(twitter_id=t)
		print "firs check u1 is ",u1, len(u1)
		
		if len(u1)<=0:
			print "error "
			d={}
			d['error']="given twitter id does not exist"
			l.append(d)
			print "u1 is ",u1
		else:
			oauth_secret=u1[0].oauth_secret
			oauth_token=u1[0].oauth_token
			home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', oauth_token, oauth_secret)
			home_timeline_json=json.loads(home_timeline)

			for obj in home_timeline_json:
				d={}
				# screen name, date, text, prof img
				d['text']=obj['text']
				d['screen_name']=obj['user']['screen_name']
				d['profile_img_url']=obj['user']['profile_image_url']
				d['unix_time']=getUnixTime(obj['created_at'])
				print d
				l.append(d)


			print len(home_timeline_json), len(l)
	data=json.dumps(l)
	

	
	#print home_timeline
	return HttpResponse(data,content_type="application/json")

def sendTweet(request):
	# check if tweet text is valid. 140 char max, etc other restritions
	# do dict.get() instead !!!
	in_twitter_text=request.POST.get('t_text',0)
	in_twitter_id=request.POST.get('t_id',0)
	l=[]
	d={}
	context={}
	if not (isValid(in_twitter_id)):
		#error
		print "error id not valid"
		
		d['error']="given twitter id does not exist"
		l.append(d)
	elif in_twitter_text==0:
		print "error getting the form fields"
		d['error']="could not get the form input"
		l.append(d)
	else:
		u1=TwitterAccounts.objects.filter(twitter_id=in_twitter_id)
		if len(u1)<=0:
			d={}
			d["error"]="account does not exist"
			l.append(d)
		else:
			status_str="status="+in_twitter_text
			oauth_secret=u1[0].oauth_secret
			oauth_token=u1[0].oauth_token
			post_tweet = oauth_req( 'https://api.twitter.com/1.1/statuses/update.json?', oauth_token, oauth_secret ,"POST",status_str)
			#return HttpResponse(post_tweet,content_type="application/json")
			return render(request,'tweets/sendTweet.html',context)

	data=json.dumps(l)
	#return HttpResponse(data,content_type="application/json")
	context={'l':l}
	return render(request,'tweets/sendTweet.html',context)
	# make a common function to check if a twitterid input is valid and if it exists. django form validors?

	

def view01(request):
	context={}
	return render(request, 'tweets/view01.html', context)

def view02(request):
	context={}
	return render(request, 'tweets/view02.html',context)


