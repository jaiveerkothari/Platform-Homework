from django.shortcuts import render
from json import loads
import json
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


def index(request):
	context={}
	return render(request, 'tweets/index.html', context)

  


def homeTimeline(request):
	in_twitter_id=request.GET.get('t_id',0)

	l=[]

	if not (isValid(in_twitter_id)):
		d={}
		d['error']="twitter id given is not valid. must be an integer"
		l.append(d)
	else:
		t=str(in_twitter_id).strip()
		u1=TwitterAccounts.objects.filter(twitter_id=t)
		
		if len(u1)<=0:
			d={}
			d['error']="given twitter id does not exist"
			l.append(d)
		else:
			oauth_secret=u1[0].oauth_secret
			oauth_token=u1[0].oauth_token
			home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', oauth_token, oauth_secret)
			home_timeline_json=json.loads(home_timeline)

			for obj in home_timeline_json:
				d={}
				d['text']=obj['text']
				d['screen_name']=obj['user']['screen_name']
				d['profile_img_url']=obj['user']['profile_image_url']
				d['unix_time']=getUnixTime(obj['created_at'])
				l.append(d)
	data=json.dumps(l)
	
	return HttpResponse(data,content_type="application/json")

def sendTweet(request):
	in_twitter_text=request.POST.get('t_text',0)
	in_twitter_id=request.POST.get('t_id',0)
	l=[]
	d={}
	context={}
	if not (isValid(in_twitter_id)):
		d['error']="given twitter id does not exist"
		l.append(d)
	elif in_twitter_text==0:
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
			return render(request,'tweets/sendTweet.html',context)

	data=json.dumps(l)
	context={'l':l}
	return render(request,'tweets/sendTweet.html',context)

	

def view01(request):
	context={}
	return render(request, 'tweets/view01.html', context)

def view02(request):
	context={}
	return render(request, 'tweets/view02.html',context)


