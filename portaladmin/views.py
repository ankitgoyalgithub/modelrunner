import boto3
import csv
import json
import random
import sys
import urllib
import os
import time

from portaladmin import model_util

from django.shortcuts import render
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from background_task.models import Task
from background_task.models_completed import CompletedTask
from datetime import datetime

class JSONResponse(HttpResponse):
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)

"""
Application Home Page
"""
def index(request):
  return render(request, "portaladmin/about.html")

"""
This View Redirects to Page Taking Containing Model Selection Form
"""
def model_selection(request):
  return render(request, "portaladmin/model-selection.html")

"""
This View Redirects to About Page 
"""
def about(request):
  return render(request, "portaladmin/about.html")

"""
Get Submission Details
"""
def fetch_submission_id(request):
  try:
    data = dict()
    data["submission_ids"] =  ['100', '101', '102']
    return HttpResponse(json.dumps(data), content_type="application/json")
  except Exception as e:
    print(e)
    return HttpResponse(json.dumps({"error": "Unable to Fetch Submission Id"}), content_type="application/json")

"""
Get Submission Details
"""
def fetch_submission_text(request, id):
  try:
    data = {
      100: "Submission Text For Id Hundred",
      101: "Submission Text For Id Hundred One",
      102: "Submission Text For Id Hundred Two" 
    }

    if id in data:
      submission_text = data.get(id)
    else:
      return HttpResponse(json.dumps({"error": "Invalid Submission Id"}), content_type="application/json")
    return HttpResponse(json.dumps({"sub_text": submission_text}), content_type="application/json")
  except Exception as e:
    print(e)
    return HttpResponse(json.dumps({"error": "Unable to Fetch Submission Text"}), content_type="application/json")

@api_view(['POST'])
def run_model(request):
    try:
      AWS_SECRET_KEY = settings.AWS_SECRET_KEY
      AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
      MEDIA_URL = settings.MEDIA_ROOT
      s3_client = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
      s3_client.download_file('voyanalytics', 'pageview.csv', MEDIA_URL+'datafiles/pageview.csv')
      model_util.run_model()
      return JSONResponse(json.dumps({"success": "Run Model Complete. Download result file from localhost:8000/media/datafiles/pageview.csv"}))
    except Exception as e:
      print(e)
      return JSONResponse(json.dumps({"error": "Error While Running Model"}))

@api_view(['GET'])
def task_status(request):
	try:
		now = timezone.now()
		pending_tasks_qs = Task.objects.filter(run_at__gt=now)
		running_tasks_qs = Task.objects.filter(locked_at__gte=now)
		completed_tasks_qs = CompletedTask.objects.all()

		task_status_list = list()

		for tasks in pending_tasks_qs:
			task_status_list.append({
				'name': tasks.task_name,
				'status': "PENDING" 
			})
		
		for tasks in running_tasks_qs:
			task_status_list.append({
				'name': tasks.task_name,
				'status': "RUNNING" 
			})

		for tasks in completed_tasks_qs:
			task_status_list.append({
				'name': tasks.task_name,
				'status': "COMPLETED" 
			})
		return JSONResponse(json.dumps({"tasks": task_status_list}))
	except Exception as e:
		print(e)
		return JSONResponse(json.dumps({"error": "Error While Running Model"}))
