from core.adb_controller import run_adb_command


def prepare_wifi_for_test():
    # Function verifies the current wi-fi state
    current_state = run_adb_command("shell settings get global wifi_on")
    if current_state != "1":
        run_adb_command("shell svc wifi enable")


def precondition_for_cellular():
    # Function verifies the current wi-fi state
    current_state = run_adb_command("shell settings get global wifi_on")
    if current_state == "1":
        run_adb_command("shell svc wifi disable")