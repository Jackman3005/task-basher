import yaml


class Config:
    def __init__(self, config_file_path):
        config = yaml.load(open(config_file_path, 'r').read())
        self.tasks = list(map(Task, config['tasks']))
        self.startupTask = next((t for t in self.tasks if t.runOnStartup), None)


class Task:
    def __init__(self, task_config):
        self.name = task_config['name']
        self.script = task_config['script']
        self.hotkey = task_config.get('hotkey', None)
        self.runOnStartup = task_config.get('runOnStartup', False)
