# terminal logic

import os
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <command>")
        return
    command = sys.argv[1]
    if command == "cf":
        from commands.cf import handle as cf_handle
        cf_handle()
    elif command == "gpt":
        from commands.gpt import handle as gpt_handle
        gpt_handle()
    elif command == "ss":
        from commands.ss import handle as ss_handle
        ss_handle()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()