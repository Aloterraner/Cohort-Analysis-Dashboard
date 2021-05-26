import os
import shutil
from datetime import datetime

import pandas as pd
# Django Dependencies
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Application Modules
import group_analysis.datetime_utils as dt_utils
import group_analysis.group_managment as gm
import group_analysis.log_import_util as log_import
import group_analysis.plotting as plotting
import group_analysis.utils as utils
from group_analysis.group_managment import Group
from group_analysis.demo import demo_hospital

# Create your views here.

def group_analysis(request):
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    load_log_succes = False

    # TODO Running Example, on how to display Plot

    # Use this to include it in the UI

    #TODO Load the Log Information, else throw/redirect to Log Selection
    if "current_log" in request.session and request.session["current_log"] is not None: 
        log_information = request.session["current_log"]
        print(log_information)


    
    # TODO Get the Groups, from the Post
    if log_information is not None:

        event_log = os.path.join(event_logs_path, log_information["log_name"])
        log_format = log_import.get_log_format(log_information["log_name"])

        # Import the Log considering the given Format
        log, activites = log_import.log_import(event_log, log_format, log_information)

        # Set the activites to the activities of the loaded log.
        request.session["activites"] = list(activites)
        load_log_succes = True

    if request.method == 'POST':
        if "uploadButton" in request.POST:
            print("in request")
        event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")

        if settings.EVENT_LOG_NAME == ':notset:':
            return HttpResponseRedirect(request.path_info)

        return render(request,'group_analysis.html', {'log_name': settings.EVENT_LOG_NAME, 'data':this_data})

    else:

        if load_log_succes:

            context = None

            # Run the Hospital Sepsis Demo
            if log_information["log_name"].lower() == "hospital_sepsis.xes": 
                context = demo_hospital(log, log_format, log_information)

            return render(request, "group_analysis.html", context=context)

        else:

             return render(request, "group_analysis.html")

       
            































