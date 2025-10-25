import argparse

class Manager:
    def __init__(self):
        self.commands = {}

    def command(self, func):
        self.commands[func.__name__] = func
        return func

    def main(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("command", nargs="?")
        parser.add_argument("args", nargs=argparse.REMAINDER)
        namespace = parser.parse_args()

        if not namespace.command or namespace.command in ("-h", "--help", "help"):
            return self.usage()

        cmd = self.commands.get(namespace.command)
        if not cmd:
            print(f"Command '{namespace.command}' not found.\n")
            return self.usage()

        # Nếu command là callable, gọi trực tiếp
        if callable(cmd):
            cmd(*namespace.args)
        else:
            cmd.parse(namespace.args)


    def usage(self):
        print("Usage: manage.py <command> [<args>]\n")

        if not self.commands:
            print("No commands available.")
            return

        print("Available commands:")
        for name, cmd in sorted(self.commands.items()):
            # Nếu hàm có docstring, lấy làm description
            desc = getattr(cmd, "__doc__", "") or ""
            print(f"  {name:<20} {desc}")