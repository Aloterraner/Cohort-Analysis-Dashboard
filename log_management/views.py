from log_management.services.log_service import LogService
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import re
import json
from django.http import JsonResponse

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
            print("Download Log")
        elif "setButton" in request.POST:
            if "log_list" not in request.POST:
                return HttpResponseRedirect(request.path_info)

            filename = request.POST["log_list"]
            if not request.POST._mutable:
                request.POST._mutable = True

            redirect_url = request.path + "?selected_log=" + filename
            redirect(redirect_url)
            return redirect(redirect_url)

    eventlog_list = log_service.getAll()
    my_dict = {"eventlog_list": eventlog_list}
    if("selected_log" in request.GET):
        log = log_service.getLog(request.GET["selected_log"])
        my_dict["selected_log_info"] = log
    return render(request, LOGMANAGEMENT_DIR + '/index.html', context=my_dict)


def get_log_info(request):
    log_service = LogService()

    log_name = request.GET.get('log_name', None)
    data = log_service.getLog(log_name).__dict__
    return JsonResponse(data)
