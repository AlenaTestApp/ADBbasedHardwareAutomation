from core.adb_controller import run_adb_command
import time
from utils.helpers import prepare_wifi_for_test
import os
from dotenv import load_dotenv
load_dotenv()


DEVICE_ID = os.getenv("DEVICE_ID")
SSID_1 = os.getenv("SSID_1")
SSID_2 = os.getenv("SSID_2")


def test_adb_devices():
    # Check for ADB Devices
    output = run_adb_command("devices")
    assert DEVICE_ID in output, f"Device ID: {DEVICE_ID} not found in output"


def test_wifi_toggle():
    # Test turns Wi-Fi OFF/ON and check corresponding output
    run_adb_command("shell svc wifi disable")
    output = run_adb_command("shell dumpsys wifi | grep 'Wi-Fi'")
    assert "Wi-Fi is disabled" or "Wi-Fi is disabling" in output

    run_adb_command("shell svc wifi enable")
    output = run_adb_command("shell dumpsys wifi | grep 'Wi-Fi'")
    assert "Wi-Fi is enabled" or "Wi-Fi is enabling" in output


def test_list_of_ssid():
    # Verify that the expected SSIDs are present in the Wi-Fi scan results
    prepare_wifi_for_test()
    output = run_adb_command("shell cmd wifi list-scan-results")
    ssids = [SSID_1, SSID_2]
    for ssid in ssids:
        assert any(ssid.lower() in line.lower() for line in output.splitlines()), f"Expected {ssid} but it was not found"


def test_wifi_toggle_stability():
    # Test that toggling Wi-Fi multiple times does not cause any crashes
    prepare_wifi_for_test()
    for _ in range(5):
        run_adb_command("shell svc wifi disable")
        output = run_adb_command("shell dumpsys wifi | grep 'Wi-Fi'")
        assert "Wi-Fi is disabled" or "Wi-Fi is disabling" in output

        run_adb_command("shell svc wifi enable")
        output = run_adb_command("shell dumpsys wifi | grep 'Wi-Fi'")
        assert "Wi-Fi is enabled" or "Wi-Fi is enabling" in output


def test_wifi_persistence_after_reboot():
    # Verify Wi-Fi reconnected after reboot
    prepare_wifi_for_test()
    run_adb_command("reboot")
    time.sleep(90)  # wait for reboot: Moto takes too long to reboot

    state_after_reboot = run_adb_command("shell settings get global wifi_on")
    assert state_after_reboot == "1", "Wi-Fi did not stay enabled after reboot"


def test_ssid_frequency():
    output = run_adb_command("shell cmd wifi list-scan-results")
    allowed = [(2400, 2500), (5000, 5900), (5925, 7125)]

    for line in output.splitlines()[1:]:  # пропускаем заголовок
        ssid, freq = line.split()[:2]
        freq = int(freq)
        if not any(low <= freq <= high for low, high in allowed):
            raise AssertionError(f"{ssid} has invalid frequency {freq} MHz")
