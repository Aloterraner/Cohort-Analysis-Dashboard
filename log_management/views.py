from log_management.models import SelectedLog
from log_management.services.log_service import LogService
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.http import JsonResponse
from wsgiref.util import FileWrapper
import os

LOGMANAGEMENT_DIR = "log_management"

# Create your views here.
def index(request):
    log_service = LogService()

    if request.method == 'POST':
        if "uploadButton" in request.POST:
            # check if the file is missing
            eventLogIsMissing = "event_log" not in request.FILES
            if eventLogIsMissing:
                return HttpResponseRedirect(request.path_info)

            log = request.FILES["event_log"]
            # Check if the file is valid
            # TODO: Perhaps move this logic inside LogService with an exception being thrown
            isInvalidFile = re.search(".(xes|csv)$", log.name.lower()) == None
            if isInvalidFile:
                return HttpResponseRedirect(request.path_info)
            log_service.saveLog(log)
        elif "deleteButton" in request.POST:
            logname = request.POST["log_list"]
            log_service.deleteLog(logname)
        elif "downloadButton" in request.POST:
            if "log_list" not in request.POST:
                return HttpResponseRedirect(request.path_info)

            filename = request.POST["log_list"]
            file_dir = log_service.getLogFile(filename)

            try:
                wrapper = FileWrapper(open(file_dir, 'rb'))
                response = HttpResponse(wrapper, content_type='application/force-download')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_dir)
                return response
            except Exception as e:
                return None
        elif "setButton" in request.POST:
            if "log_list" not in request.POST:
                return HttpResponseRedirect(request.path_info)
            filename = request.POST["log_list"]
            return redirect('setlog/' + filename + '/')

    eventlog_list = log_service.getAll()
    my_dict = {"eventlog_list": eventlog_list}
    if(request.session['current_log'] != None):
        try:
            my_dict["selected_log_info"] = request.session['current_log']
        except Exception as err:
            print("Oops!  Fetching the log failed: {0}".format(err))
    return render(request, LOGMANAGEMENT_DIR + '/index.html', context=my_dict)

def set_log(request, logname):
    log_service = LogService()

    if request.method == 'POST':
        name = request.POST['logName']
        attribute = request.POST['attribute']
        print("Selected attribute: " + attribute)
        prop = request.POST['property']
        print("Selected property: " + prop)
        # name = request.POST['classifier']
        selected_log = SelectedLog(name, "case_id", "case_concept_name")
        request.session['current_log'] = selected_log.__dict__
        return redirect('/logmanagement/')


    data = log_service.getLogInfo(logname).__dict__
    return render(request, LOGMANAGEMENT_DIR + '/set_log.html', context=data)


def get_log_info(request):
    log_service = LogService()

    log_name = request.GET.get('log_name', None)
    data = log_service.getLogInfo(log_name).__dict__
    return JsonResponse(data)

def log_response(request, log):
    response = HttpResponse("Setting current log")
    response.set_cookie(key="current_log", value=log.log_name)