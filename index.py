from rich.console import Console

from config import Configuration
from cli import Arguments, CLI

console = Console()

def welcome():
    print()
    console.print("👋 Welcome to the Viexly CLI!!", style="bold")
    print()

welcome()


cli = CLI(config=Configuration("viexly.conf"))

args = Arguments(cli=cli)
try:
    args.run()
except KeyboardInterrupt:
    console.print("\n\n👋 Goodbye!", style="bold")
    print()
    exit(0)