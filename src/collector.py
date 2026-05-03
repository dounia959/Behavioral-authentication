import csv
import os
import time
from datetime import datetime

from pynput import keyboard, mouse


SAVE_DIR = "data"
SESSION_NAME = datetime.now().strftime("session_%Y%m%d_%H%M%S")
FILENAME = os.path.join(SAVE_DIR, SESSION_NAME + ".csv")

os.makedirs(SAVE_DIR, exist_ok=True)

with open(FILENAME, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "event_type", "key", "x", "y"])

print(f"[INFO] Recording started -> {FILENAME}")
print("[INFO] Press ESC to stop.\n")


def log(event_type, key=None, x=None, y=None):
    with open(FILENAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.time(), event_type, key, x, y])


def on_press(key):
    try:
        log("key_press", key.char)
    except AttributeError:
        log("key_press", str(key))


def on_release(key):
    log("key_release", str(key))
    if key == keyboard.Key.esc:
        print("\n[INFO] Stopping recording...")
        return False


def on_move(x, y):
    log("mouse_move", x=x, y=y)


def on_click(x, y, button, pressed):
    if pressed:
        log("mouse_click", str(button), x, y)


def on_scroll(x, y, dx, dy):
    log("mouse_scroll", x=x, y=y)


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.stop()
mouse_listener.join()

print(f"[INFO] Data saved in {FILENAME}")
