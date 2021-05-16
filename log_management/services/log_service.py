
from django.conf import settings
import os
from os import listdir
from os.path import isfile, join
from django.core.files.storage import FileSystemStorage
from pm4py.objects.log.importer.xes import importer as xes_importer_factory

EVENT_LOG_PATH = os.path.join(settings.MEDIA_ROOT,"event_logs")
class LogService:
    """
    Returns the list of all event logs
    """
    def getAll(self):
        eventlogs = [f for f in listdir(EVENT_LOG_PATH) if isfile(join(EVENT_LOG_PATH, f))]
        return eventlogs

    """
    Saves an event log to the existing list of event logs
    """
    def saveLog(self, log):
        fs = FileSystemStorage(EVENT_LOG_PATH)
        fs.save(log.name, log)


    """
    Returns the corresponding log with basic information about it
    """
    def getLogInfo(self, log_name):
        file_dir = os.path.join(EVENT_LOG_PATH, log_name)

        xes_log = xes_importer_factory.apply(file_dir)
        attributes = list(xes_log.attributes.keys())
        properties = list(xes_log.properties.keys())
        classifiers = list(xes_log._classifiers.keys())
        return LogDto(log_name, attributes, properties, classifiers)

    """
    Returns the log file
    """
    def getLogFile(self, log_name):
        file_dir = os.path.join(EVENT_LOG_PATH, log_name)
        return file_dir

    """
    Deletes an event log from the existing list of event logs
    """
    def deleteLog(self, log_filename):
        # eventlogs = [f for f in listdir(EVENT_LOG_PATH) if isfile(join(EVENT_LOG_PATH, f))]
        # eventlogs.remove(logFileName)
        file_dir = os.path.join(EVENT_LOG_PATH, log_filename)
        os.remove(file_dir)
        # return eventlogs

class LogDto():
    def __init__(self, log_name, attributes, properties, classifiers):
        self.log_name = log_name
        self.attributes = attributes
        self.properties = properties
        self.classifiers = classifiers