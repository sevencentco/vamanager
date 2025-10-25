# env.py
import os
def load_env(filename=".env"):
    if not os.path.exists(filename):
        return
    with open(filename) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v)
