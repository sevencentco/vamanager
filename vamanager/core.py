# core.py
import argparse
from .env import load_env

class Manager:
    def __init__(self):
        self.commands = {}

    def command(self, func):
        self.commands[func.__name__] = func
        return func

    def main(self):
        load_env()
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
        namespace = None
        for path, cmd in sorted(self.commands.items(), key=lambda c: (c[0].count('.'), c[0])):
            if cmd.namespace != namespace:
                if cmd.namespace:
                    print(f"\n[{cmd.namespace}]")
                namespace = cmd.namespace
            name = f"  {cmd.name:<20}"  # canh lề trái, rộng 20 ký tự
            print(f"{name} {cmd.description or ''}")