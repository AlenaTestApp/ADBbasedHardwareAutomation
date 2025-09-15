import subprocess


def run_adb_command(command):
    """Runs shell adb commands and returns the output -> str
    Args -> str: adb command without adb prefix"""

    cmd = ['adb'] + command.split()
    try:
        res = subprocess.run(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"


if __name__ == "__main__":
    print(run_adb_command("devices"))
