#!/usr/bin/env python

import sys
import os
import readchar
import time
import yaml

tmuxSessionName = sys.argv[1]

config = yaml.load(open('runner.yml', 'r').read())

print(config)

def send_keys(keys):
    pane_number = '0'
    os.system('tmux send-keys -t ' + tmuxSessionName + ':.' + pane_number + ' ' + keys)


def ctrl_c():
    send_keys('C-c' + ' Enter')


def execute(cmd):
    quote = '\''
    send_keys('-X cancel')
    time.sleep(.5)
    ctrl_c()
    send_keys(quote + cmd + quote + ' Enter')


def print_available_commands(cmds):
    print('')
    print('Available commands:')
    print('1 - scroll up')
    print('2 - scroll down')
    for cmd in cmds:
        print(cmd)
    print('q - quit')


def close_tmux():
    print('Goodbye!')
    ctrl_c()
    os.system('tmux kill-session -t ' + tmuxSessionName)


def scroll_up():
    os.system('tmux copy-mode -t ' + tmuxSessionName + ':.0')
    send_keys('-X page-up')


def scroll_down():
    os.system('tmux copy-mode -t ' + tmuxSessionName + ':.0')
    send_keys('-X page-down')


availableCommands = []
for _command in config['commands']:
    if 'runOnStart' in _command and _command['runOnStart']:
        execute(_command['script'])
    availableCommands.append(_command['key'] + ' - ' + _command['name'])

print_available_commands(availableCommands)

print('enter command: ', end='')
sys.stdout.flush()

while True:
    try:
        command = readchar.readchar()
    except KeyboardInterrupt:
        sys.exit(0)

    if command == 'q':
        close_tmux()
        break
    elif command == '1':
        scroll_up()
    elif command == '2':
        scroll_down()
    else:
        for _command in config['commands']:
            if _command['key'] == command:
                execute(_command['script'])

