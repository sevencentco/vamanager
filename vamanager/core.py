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
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("args", nargs="*")
        ns = parser.parse_args()

        cmd = self.commands.get(ns.command)
        if not cmd:
            print("Command not found")
            return
        cmd(*ns.args)
