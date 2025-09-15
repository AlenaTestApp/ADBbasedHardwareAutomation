from core.adb_controller import run_adb_command
import os
from dotenv import load_dotenv

load_dotenv()
import uiautomator2 as ui2
from core.device_controller import open_phone_settings

DEVICE_ID = os.getenv("DEVICE_ID")
dut = ui2.Device(DEVICE_ID)


def test_check_eSIM_profile():
    # Test Google Fi eSIM via UI and Telephony registry
    open_phone_settings()
    dut(text="Network & internet").click()
    mobile_data_title = dut(resourceId="android:id/title", text="Mobile data")
    google_fi = mobile_data_title.sibling(resourceId="android:id/summary")
    settings_sim = google_fi.get_text().split('/')[0].strip().lower()
    backend_sim = run_adb_command("shell getprop gsm.operator.alpha").strip(",").lower()
    assert settings_sim == backend_sim
