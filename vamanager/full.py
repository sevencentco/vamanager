# -*- coding: utf-8 -*-
import argparse
import os

from .env import load_env
from .core import Manager
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
class FullManager(Manager):
    def __init__(self):
        super().__init__()
        self.prompt_args = {}

    # decorator để đăng ký prompt args
    def prompt(self, name, message=None, **kwargs):
        def wrapper(func):
            self.prompt_args.setdefault(func.__name__, [])
            self.prompt_args[func.__name__].append(PromptArg(name, message, **kwargs))
            return func
        return wrapper
    
def main(self):
    # 1️⃣ Nạp biến môi trường từ file .env
    load_env(filename=".env")

    # 2️⃣ Cấu hình argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    namespace = parser.parse_args()

    # 3️⃣ Xử lý trường hợp không có lệnh hoặc yêu cầu help
    if not namespace.command or namespace.command in ("-h", "--help", "help"):
        return self.usage()

    # 4️⃣ Tìm lệnh trong danh sách
    cmd = self.commands.get(namespace.command)
    if not cmd:
        CLI.puts(f"Unknown command: {namespace.command}", "red")
        CLI.puts("Available commands:\n" + "\n".join(self.commands.keys()), "blue")
        return self.usage()

    # 5️⃣ Nếu lệnh có các prompt tương tác (yêu cầu nhập thêm)
    prompts = self.prompt_args.get(namespace.command, [])
    kwargs = {}
    for p in prompts:
        kwargs[p.name] = p.prompt()

    # 6️⃣ Thực thi command
    if callable(cmd):
        cmd(*namespace.args, **kwargs)
    else:
        # Giữ tương thích với các command có parse() riêng
        cmd.parse(namespace.args)
