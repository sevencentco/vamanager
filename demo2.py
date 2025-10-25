from manager.core import Manager, CLI

manager = Manager()

@manager.command
@manager.prompt("username", "Enter your username", required=True)
@manager.prompt("age", "Your age", type_=int)
def hello(username, age):
    """Ví dụ command có PromptArg"""
    CLI.puts(f"Hello {username}, you are {age} years old!", "green")

if __name__ == "__main__":
    manager.main()
