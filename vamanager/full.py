# -*- coding: utf-8 -*-
import argparse
import os

from .env import load_env
# ==========================
# CLI helper (màu, prompt)
# ==========================
class CLI:
    @staticmethod
    def puts(msg, color=None):
        colors = {
            "red": "\033[91m", "green": "\033[92m",
            "blue": "\033[94m", "end": "\033[0m"
        }
        if color:
            msg = f"{colors[color]}{msg}{colors['end']}"
        print(msg)

    @staticmethod
    def prompt(message, default=None, required=False, type_=str):
        while True:
            raw = input(f"{message} "
                        f"{'(default: '+str(default)+') ' if default else ''}: ").strip()
            if not raw and default is not None:
                return default
            if not raw and required:
                CLI.puts("This field is required.", "red")
                continue
            try:
                return type_(raw)
            except ValueError:
                CLI.puts(f"Invalid type, expected {type_.__name__}", "red")


# ==========================
# PromptArg class
# ==========================
class PromptArg:
    def __init__(self, name, message=None, type_=str, required=False, default=None):
        self.name = name
        self.message = message or name
        self.type_ = type_
        self.required = required
        self.default = default

    def prompt(self):
        return CLI.prompt(
            self.message, default=self.default,
            required=self.required, type_=self.type_
        )


# ==========================
# Manager
# ==========================
class FullManager:
    def __init__(self):
        self.commands = {}
        self.prompt_args = {}

    # decorator để đăng ký command
    def command(self, func):
        self.commands[func.__name__] = func
        return func

    # decorator để đăng ký prompt args
    def prompt(self, name, message=None, **kwargs):
        def wrapper(func):
            self.prompt_args.setdefault(func.__name__, [])
            self.prompt_args[func.__name__].append(PromptArg(name, message, **kwargs))
            return func
        return wrapper

    def main(self):
        load_env()
        parser = argparse.ArgumentParser()
        parser.add_argument("command", help="command to run")
        parser.add_argument("args", nargs="*")
        ns = parser.parse_args()

        if ns.command not in self.commands:
            CLI.puts(f"Unknown command: {ns.command}", "red")
            CLI.puts("Available commands:\n" + "\n".join(self.commands.keys()), "blue")
            return

        func = self.commands[ns.command]
        prompts = self.prompt_args.get(ns.command, [])
        kwargs = {}

        for p in prompts:
            kwargs[p.name] = p.prompt()

        func(*ns.args, **kwargs)
