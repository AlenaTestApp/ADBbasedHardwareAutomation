📡 Android Hardware & Connectivity Tests

Automated tests focused on hardware automation, network connectivity, and eSIM/SIM properties on Android devices.

🔹 Features

✅ Cellular connectivity hardware tests

✅ Wi-Fi connectivity hardware tests

✅ eSIM / Google Fi verification via UI and backend (ADB)



🛠 Requirements

Android device with USB debugging enabled

Python 3.8+

Install dependencies:

pip install --upgrade uiautomator2 pytest python-dotenv


Create a .env file in the project root for sensitive data:

DEVICE_ID=<your_device_id>


Note: .env is included in .gitignore to protect the device info.

🚀 Running Tests

Run all tests:

pytest tests/ -v

Run suite:

pytest tests/test_settings_ui.py
