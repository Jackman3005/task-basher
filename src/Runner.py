#!/usr/bin/env python

import sys
from threading import Thread
from Config import Config
from ControlPane import ControlPane
from SessionManager import SessionManager

tmuxSessionName = sys.argv[1]
configFilePath = sys.argv[2]

config = Config(configFilePath)
sessionManager = SessionManager(tmuxSessionName)


# class Colors:
#     default = '\033[49m'
#     cyan = '\033[87m'


def initialize():
    sessionManager.resize_pane(1, 10)
    sessionManager.send_keys(
        "PS1='$(echo -e \"\e[1m\e[32m\$(date +%H:%M:%S)\e[0m | \e[94mTASK BASHER\e[0m | Executing... \")' Enter")
    sessionManager.clear_pane()

    if config.startupTask:
        sessionManager.execute(config.startupTask.script)


Thread(target=initialize).start()

ControlPane(sessionManager, config.tasks)
