from argparse import Namespace
from os import path
import math
import colorama

class Error(TypeError):
    pass

def list_of_commands(histfile: str, count_sudo: bool):
    if not path.exists(histfile):
        raise Error("The history file is not found.")
    with open(histfile, mode='r', encoding='unicode_escape') as f:
        rawlines = f.readlines()
        f.close()
    commands: list[str] = []

    # zsh history file
    if rawlines[0].startswith(": "):
        for line in rawlines:
            try:
                _, date_and_command, *args = line.split(" ")
                _, command = date_and_command.split(";")
                if command == "sudo" or command == "doas":
                    commands.append(args[0].replace("\n", ''))
                    if count_sudo:
                        commands.append(command.replace("\n", ''))
                else:
                    commands.append(command.replace("\n", ''))
            except ValueError:
                continue
    else:
        for line in rawlines:
            actual_command, *args = line.split(" ")
            if actual_command == "sudo" or actual_command == "doas":
                commands.append(args[0].replace("\n", ''))
            else:
                commands.append(actual_command.replace("\n", ''))
    return commands
        
def count_used(cmds: list[str]):
    used: list[dict[str, int]] = []
    for command in cmds:
        exists = False
        for exist in used:
            if command in exist:
                exist[command] += 1
                exists = True
        if not exists:        
            used.append({command: 1})
    return used

def progress_bar(total: int, used: int, args: Namespace):
    fill = args.bar
    empty = args.bar_empty
    fill_number = math.floor(used / total * 10)
    empty_number = 10 - fill_number
    progress = fill * fill_number + empty * empty_number
    colorful_progress = colorama.Fore.BLUE + progress[1:3] + colorama.Fore.YELLOW + progress[4:7] + colorama.Fore.RED + progress[8:] + colorama.Fore.RESET
    return args.bar_open + colorful_progress + args.bar_close

def print_commands(cmds: list[dict[str, int]], total_cmds: list[str], count: int, args: Namespace):
    total_cmds_count = len(total_cmds)
    formatted_number = format(total_cmds_count, ",")
    print(f"{formatted_number} commands used")
    sort_cmd = sorted(cmds, key=lambda k: list(k.values()), reverse=True)
    remaining = 0
    highest_sorted_usage_list = [list(i.values())[0] for i in sort_cmd[:count]]
    highest_sorted_usage_count = max(*highest_sorted_usage_list)
    for commands in sort_cmd[:count]:
        display_command = list(commands.keys())[0]
        display_count = list(commands.values())[0]
        percent = "{:.2f}".format((display_count / total_cmds_count) * 100)
        progress = progress_bar(highest_sorted_usage_count, display_count, args)
        print(f"{progress} {' ' if len(percent) < 5 else ''}{percent}% {' ' * (len(str(highest_sorted_usage_count)) - len(str(display_count)))}{colorama.Fore.BLACK + str(display_count) + colorama.Fore.RESET} {colorama.Style.BRIGHT + display_command + colorama.Style.RESET_ALL}")
        remaining += display_count
    remaining_percent = "{:.2f}".format(((total_cmds_count - remaining) / total_cmds_count) * 100)
    print(colorama.Fore.BLACK + f"... {total_cmds_count - remaining} (~{remaining_percent}%) others" + colorama.Fore.RESET)

def main(args: Namespace):
    count = args.count
    file = args.file
    list_cmds = list_of_commands(file, args.count_sudo)
    cmds = count_used(list_cmds)
    print_commands(cmds, list_cmds, count, args)