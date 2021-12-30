from holy_greetings_bot import HolyGreetingsBot
import sys

if __name__ == "__main__":
    """
    Start bot with python main.py [token].
    """
    b = HolyGreetingsBot(sys.argv[1])
    b.run()
