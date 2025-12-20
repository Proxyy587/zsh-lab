#!/usr/bin/env python3

import os
import stat
import sys
from typing import List


INSTALL_DIR = os.path.expanduser("~/bin")
COMMAND_NAMES = ["cf", "gpt", "ss"]

def _launcher_script(command_name: str) -> str:
    python = sys.executable          # <— use the python that runs devcli.py
    this_file = os.path.abspath(__file__)
    return f"""#!/usr/bin/env bash
"{python}" "{this_file}" {command_name} "$@"
"""


def install_commands() -> None:
    os.makedirs(INSTALL_DIR, exist_ok=True)

    for name in COMMAND_NAMES:
        path = os.path.join(INSTALL_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(_launcher_script(name))
        # Make executable
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

    print("✅ Commands installed:", ", ".join(COMMAND_NAMES))
    print(f"Launchers created in: {INSTALL_DIR}")
    print("Make sure this directory is on your PATH in zsh, e.g. add:")
    print(f"  export PATH=\"{INSTALL_DIR}:$PATH\" >> ~/.zshrc")


def uninstall_commands() -> None:
    for name in COMMAND_NAMES:
        path = os.path.join(INSTALL_DIR, name)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed: {path}")
        else:
            print(f"Not found (skipped): {path}")


def status_commands() -> None:
    for name in COMMAND_NAMES:
        path = os.path.join(INSTALL_DIR, name)
        if os.path.exists(path):
            print(f"{name}: installed at {path}")
        else:
            print(f"{name}: NOT installed")


def dispatch(argv: List[str]) -> None:
    if not argv:
        print("Usage:")
        print("  python devcli.py install       # install cf / gpt commands")
        print("  python devcli.py uninstall     # remove cf / gpt commands")
        print("  python devcli.py status        # show status")
        print("  python devcli.py cf [random]")
        print('  python devcli.py gpt "prompt"')
        print('  python devcli.py ss [filename] # take a screenshot and save it to the downloads/screenshots directory')
        return

    cmd = argv[0]
    args = argv[1:]

    if cmd in ("install", "--install"):
        install_commands()
        return

    if cmd in ("uninstall", "--uninstall"):
        uninstall_commands()
        return

    if cmd in ("status", "--status"):
        status_commands()
        return

    if cmd == "cf":
        from commands.cf import handle as cf_handle

        cf_handle(args)
        return

    if cmd == "gpt":
        from commands.gpt import handle as gpt_handle

        gpt_handle(args)
        return

    if cmd == "ss":
        from commands.ss import handle as ss_handle

        ss_handle(args)
        return

    print(f"Unknown command: {cmd}")


def main() -> None:
    dispatch(sys.argv[1:])


if __name__ == "__main__":
    main()
