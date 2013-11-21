#!/usr/bin/eval PYTHONPATH=/home/stein/modules python
import os, sys

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = "system.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

