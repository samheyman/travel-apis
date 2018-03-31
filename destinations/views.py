from django.http import HttpResponse
from django.shortcuts import render
from .forms import LocationSearchForm
import urllib.parse
import urllib.request
import requests
import json
from pprint import pprint
import os

def index(request):
    return render(request, 'destinations/index.html')

def points_of_interest(request):
	location = ""
	points_of_interest = {}
	if 'location' in request.GET:
		form = LocationSearchForm(request.GET)
		if form.is_valid():
			location = form.cleaned_data['location']
			points_of_interest = getPointsOfInterest(location,'yapq')
	else:
		form = LocationSearchForm()
		location = ""
	return render(request, 'destinations/points-of-interest.html', {'form': form, 'result': points_of_interest, 'location': location})


def getPointsOfInterest(location, provider):
	if provider is 'yapq':
		api_endpoint = "https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?"
		values = {
			"city_name": location,
			"apikey": os.environ.get("AMADEUS_SANDBOX_KEY")
		}
		api_endpoint = api_endpoint + urllib.parse.urlencode(values)
		req = urllib.request.Request(api_endpoint)
		response = urllib.request.urlopen(req)
		try:
			json_data = json.load(response)
		except:
			json_data = None
			
	elif provider is 'avuxi':
		json_data = json.loads('{}')
	else:
		json_data = None
	return json_data