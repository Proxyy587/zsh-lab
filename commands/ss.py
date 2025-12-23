import pyautogui
import os
from datetime import datetime

default_screenshot_dir = os.path.expanduser("~/Downloads/screenshots")

def ensure_dir(dir_path: str) -> str:
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            print(f"Could not create directory '{dir_path}': {e}")
            dir_path = os.getcwd()
    return dir_path

def take_screenshot(filename: str, directory: str = None) -> None:
    if directory is None:
        directory = default_screenshot_dir
    screenshot_dir = ensure_dir(directory)
    save_path = os.path.join(screenshot_dir, filename)
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return
    print(f"Screenshot saved to {save_path}")

def handle(args: list[str]) -> None:
    global default_screenshot_dir
    if not args:
        take_screenshot(datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png")
        return

    if args[0] in ("--dir", "-d"):
        if len(args) < 2:
            print("invalid command: ss -d <directory>")
            return
        default_screenshot_dir = os.path.expanduser(args[1])
        print(f"default screenshot directory set to {default_screenshot_dir}")
        return

    filename = None
    per_screenshot_dir = None
    args_iter = iter(args)
    for arg in args_iter:
        if arg in ("--dir", "-d"):
            try:
                per_screenshot_dir = os.path.expanduser(next(args_iter))
            except StopIteration:
                print("invalid command: ss <filename> --dir <directory>")
                return
        elif filename is None:
            filename = arg
        else:
            break

    if not filename:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    else:
        if not filename.lower().endswith(".png"):
            filename += ".png"

    take_screenshot(filename, per_screenshot_dir)