class Application:
    def __init__(self):
        self.commands = {}

    def register_command(self, name, command):
        self.commands[name] = command

    def execute(self, name, **kwargs):
        if name in self.commands:
            self.commands[name](**kwargs).execute()
        else:
            print(f"Unknown command: {name}")
