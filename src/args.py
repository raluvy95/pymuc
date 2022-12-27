import argparse

def argument():
    parser = argparse.ArgumentParser(description="Pymuc - a Python 3 variant of original program, Muc")
    parser.add_argument("--count", '-c', default=10, type=int, required=False, help="Limit rows to show list of commands used")
    parser.add_argument("--file", '-f', type=str, required=True, help="File to a history shell file, use $HISTFILE for your current shell's history")
    parser.add_argument("--count_sudo", '-C', action='store_const', required=False, help="Whenever or not count sudo or doas", default=False, const=True)
    parser.add_argument("--bar", '-b', type=str, required=False, help="Set custom bar", default="▮")
    parser.add_argument("--bar_empty", '-be', type=str, required=False, help="Set custom empty display bar", default=" ")
    parser.add_argument("--bar_open", '-bo', type=str, required=False, help="Set custom open display bar", default="[")
    parser.add_argument("--bar_close", '-bc', type=str, required=False, help="Set custom close display bar", default="]")
    return parser
