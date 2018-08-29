import urwid

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),
]


class ControlPane:
    def __init__(self, session_manager, tasks):
        self.tasks = tasks
        self.sessionManager = session_manager

        task_list = self.build_task_list(self.tasks)

        padded_task_list = urwid.Padding(task_list, left=2, right=2)
        main = urwid.Overlay(padded_task_list, urwid.SolidFill(' '),
                            align='left', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)

        urwid.MainLoop(main, palette=[('reversed', 'standout', '')], unhandled_input=self.handle_keypress).run()

        # loop = urwid.MainLoop(task_list, palette, unhandled_input=self.handle_keypress)
        # loop.run()

    def handle_keypress(self, key):
        if key in ('q', 'Q'):
            self.sessionManager.exit()
        elif key in ('k'):
            self.taskListWalker.get_focus()
            self.taskListWalker.set_focus(2)

    def build_task_list(self, tasks):
        title = "Tasks"
        body = [urwid.Text(title), urwid.Divider()]
        for task in tasks:
            button = urwid.Button(task.name)
            urwid.connect_signal(button, 'click', self.task_chosen, task)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        quit_button = urwid.Button('Quit')

        urwid.connect_signal(quit_button, 'click', lambda _: self.sessionManager.exit(), None)
        body.append(urwid.AttrMap(quit_button, None, focus_map='reversed'))

        self.taskListWalker = urwid.SimpleFocusListWalker(body)
        return urwid.ListBox(self.taskListWalker)

    def task_chosen(self, button, task):
        self.sessionManager.ctrl_c()
        self.sessionManager.execute(task.script)

# def exit_program(button):
#     raise urwid.ExitMainLoop()
#
#
# main = urwid.Padding(menu(u'Pythons', choices), left=2, right=2)
# top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
#                     align='center', width=('relative', 60),
#                     valign='middle', height=('relative', 60),
#                     min_width=20, min_height=9)
# urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
