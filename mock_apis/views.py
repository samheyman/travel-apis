from django.http import HttpResponse
from django.shortcuts import render
import urllib.parse
import urllib.request
import requests
import json
from pprint import pprint
import os
from common import geolocation

def index(request):
    return render(request, 'mock_apis/index.html')
