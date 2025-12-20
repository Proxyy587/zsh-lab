import pyautogui
import os
from datetime import datetime

def get_screenshot_dir() -> str:
    dir_path = os.path.expanduser("~/downloads/screenshots")
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            print(f"Could not create directory '{dir_path}': {e}")
            dir_path = os.getcwd()
    return dir_path

def take_screenshot(filename: str) -> None:
    screenshot_dir = get_screenshot_dir()
    save_path = os.path.join(screenshot_dir, filename)
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return
    print(f"Screenshot saved to {save_path}")

def handle(args: list[str]) -> None:
    if not args:
        take_screenshot(datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png")
        return
    take_screenshot(args[0] + ".png")