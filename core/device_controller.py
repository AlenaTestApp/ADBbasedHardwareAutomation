import datetime
import time
from core.adb_controller import run_adb_command


# _________________________________________________________________________________________________
# Text & Tap
# _________________________________________________________________________________________________

def tap(x, y):
    """tap on (x, y) using ADB"""
    return run_adb_command(f"shell input tap {x} {y}")


def input_text(text):
    """input text on the device"""
    return run_adb_command(f"shell input text {text}")


# _________________________________________________________________________________________________
# Swipe gestures
# _________________________________________________________________________________________________
def swipe(x1, y1, x2, y2):
    """swipe by coordinates: from (x1, y1) to (x2, y2)"""
    return run_adb_command(f"shell input swipe {x1} {y1} {x2} {y2}")


def swipe_up():
    """Swipe up gesture"""
    return swipe(500, 1500, 500, 500)


def swipe_down():
    """Swipe down gesture"""
    return swipe(500, 500, 500, 1500)


# _________________________________________________________________________________________________
# System actions
# _________________________________________________________________________________________________
def open_phone_settings():
    """open Android Settings app"""
    return run_adb_command(f"shell am start -n com.android.settings/.Settings")


def unlock_device():
    """unlock device screen"""
    # wake up the device
    run_adb_command("shell input keyevent 224")
    # unlock the device
    run_adb_command("shell keyevent 82")


def take_screenshot(base_name="screenshot"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/Users/kalatsei/IdeaProjects/PythonPixel/{base_name}_{timestamp}.png"
    device_path = f"sdcard/screencap_tmp.png"
    run_adb_command(f"shell screencap -p {device_path}")
    time.sleep(6)
    run_adb_command(f"adb pull {device_path} {filename}")
    # run_adb_command(f"shell rm {device_path}")