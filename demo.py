# manage.py
from manager.core import Manager

manager = Manager()

@manager.command
def hello(name="World"):
    print(f"Hello {name}")

if __name__ == "__main__":
    manager.main()
