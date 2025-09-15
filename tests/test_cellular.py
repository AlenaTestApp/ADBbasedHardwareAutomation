from core.adb_controller import run_adb_command
import time
from utils.helpers import precondition_for_cellular
from dotenv import load_dotenv
load_dotenv()


def test_cellular_connectivity():
    # Test cellular connectivity on the device, voice and data services available
    voice, data = '', ''
    precondition_for_cellular()
    output = run_adb_command("shell dumpsys telephony.registry | grep 'mServiceState'")
    for line in output.splitlines():
        for part in line.split(","):
            part = part.strip()
            if "mVoiceRegState" in part:
                voice = part
            elif "mDataRegState" in part:
                data = part

    assert "IN_SERVICE" in voice, f"Voice not in service: {voice}"
    assert "IN_SERVICE" in data, f"Data not in service: {data}"


def test_cellular_5G_NSA_connectivity():
    # Test 5G NSA cellular connectivity on the device.
    precondition_for_cellular()
    run_adb_command("shell settings put global preferred_network_mode 26")
    time.sleep(5)
    current_mode = run_adb_command("shell settings get global preferred_network_mode").strip()
    assert current_mode == "26", f"Network mode is not 5G NSA: {current_mode}"


def test_cellular_5g_SA_connectivity():
    # Test 5G SA cellular connectivity on the device.
    precondition_for_cellular()
    # Remember default, should be NSA - 26
    default = run_adb_command("shell settings get global preferred_network_mode").strip()
    # Set to SA - 20
    run_adb_command("shell settings put global preferred_network_mode 20")
    time.sleep(5)
    current = run_adb_command("shell settings get global preferred_network_mode").strip()
    assert current == "20", f"Network mode is not 5G SA: {current}"
    # Return to default
    run_adb_command(f"shell settings put global preferred_network_mode {default}")
    time.sleep(5)
    default = run_adb_command("shell settings get global preferred_network_mode").strip()
    assert default == "26", f"Network mode is not 5G NSA: {default}"


