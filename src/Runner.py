#!/usr/bin/env python

import sys
import os
import readchar
import time

from Config import Config

tmuxSessionName = sys.argv[1]
configFilePath = sys.argv[2]

config = Config(configFilePath)


class Colors:
    default = '\033[49m'
    cyan = '\033[87m'


def send_keys(keys, pane_number='0'):
    os.system('tmux send-keys -t ' + tmuxSessionName + ':.' + pane_number + ' ' + keys)


def ctrl_c():
    send_keys('C-c')


def execute(cmd):
    quote = '\''
    send_keys('-X cancel > /dev/null 2>&1')
    time.sleep(.5)
    ctrl_c()
    send_keys(quote + cmd + quote + ' Enter')


def print_available_tasks(tasks):
    print(Colors.cyan)
    print('Available tasks:')
    print('1 - scroll up')
    print('2 - scroll down')
    for t in tasks:
        print(t.hotkey + ' - ' + t.name)
    print('q - quit' + Colors.default)


def close_tmux():
    print('Goodbye!')
    ctrl_c()
    os.system('TMUX='' tmux attach-session -d')


def scroll_up():
    os.system('tmux copy-mode -t ' + tmuxSessionName + ':.0')
    send_keys('-X page-up')


def scroll_down():
    os.system('tmux copy-mode -t ' + tmuxSessionName + ':.0')
    send_keys('-X page-down')


send_keys("PS1='$(echo -e \"\e[1m\e[32m\$(date +%H:%M:%S)\e[0m | \e[94mTASK BASHER\e[0m | Executing... \")' Enter")
send_keys("unset HISTFILE' Enter")
execute('clear')
os.system('tmux clear-history -t ' + tmuxSessionName + ':.0')

if config.startupTask:
    execute(config.startupTask.script)

print_available_tasks(config.tasks)

print('Choice: ', end='')
sys.stdout.flush()

while True:
    try:
        userInput = readchar.readchar()
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.exit(0)

    if userInput == 'q':
        close_tmux()
        break
    elif userInput == '1':
        scroll_up()
    elif userInput == '2':
        scroll_down()
    else:
        for task in config.tasks:
            if task.hotkey == userInput:
                execute(task.script)
