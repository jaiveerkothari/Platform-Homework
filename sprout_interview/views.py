from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	context={}
	return HttpResponse("This is the sprout social coding challenge. Go to the tweets app at http://127.0.0.1:8000/tweets/ ")