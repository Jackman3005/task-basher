import os
import time


class SessionManager:
    def __init__(self, tmux_session_name):
        self.tmuxSessionName = tmux_session_name

    def send_keys(self, keys, pane_number=0):
        os.system('tmux send-keys -t ' + self._pane_id(pane_number) + ' ' + keys)

    def execute(self, cmd):
        quote = '\''
        self.send_keys('-X cancel > /dev/null 2>&1')
        time.sleep(.5)
        self.ctrl_c()
        self.send_keys(quote + cmd + quote + ' Enter')

    def ctrl_c(self):
        self.send_keys('C-c')

    def exit(self):
        self.ctrl_c()
        os.system('TMUX='' tmux attach-session -d')

    def scroll_up(self, pane_number=0):
        os.system('tmux copy-mode -t ' + self._pane_id(pane_number))
        self.send_keys('-X page-up')

    def scroll_down(self, pane_number=0):
        os.system('tmux copy-mode -t ' + self._pane_id(pane_number))
        self.send_keys('-X page-down')

    def resize_pane(self, pane_number, new_vertical_size):
        os.system('tmux resize-pane -t ' + self._pane_id(pane_number) + ' -y ' + str(new_vertical_size))

    def clear_pane(self, pane_number=0):
        self.execute('clear')
        os.system('tmux clear-history -t ' + self._pane_id(pane_number)
                  )

    def _pane_id(self, pane_number):
        return self.tmuxSessionName + ':.' + str(pane_number)