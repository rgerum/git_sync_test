import subprocess
import os
import sys


class Git:
    def __init__(self):
        self.current_hash = get_current_commit_hash()

    def check_update(self):
        fetch()
        remote_commit = get_newest_commit_hash()
        if self.current_hash != remote_commit:
            print("hash", self.current_hash, remote_commit)
            self.current_hash = remote_commit
            update_to_head()
            restart_script()


def run_command(command):
    """
    Runs a shell command and returns its output.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Command failed: {command}")
        print(f"Error: {stderr}")
        return None
    return stdout.strip()

def get_current_commit_hash():
    """Retrieves the current commit hash of the repository using Git CLI."""
    return run_command("git rev-parse HEAD")

def get_current_branch():
    # Gets the current branch name using Git CLI.
    return run_command("git rev-parse --abbrev-ref HEAD")

def fetch():
    # Fetch the latest changes from the remote without merging
    run_command("git fetch origin")

def get_newest_commit_hash():
    # Get the latest commit hash from the remote
    remote_commit = run_command("git rev-parse origin/{}".format(get_current_branch()))
    return remote_commit

def restart_script():
    """Restarts the current script."""
    print("Restarting script...")
    os.execv(sys.executable, ['python'] + sys.argv)

def update_to_head():
    run_command("git checkout HEAD --force")  # Now pull the changes
    run_command("git pull origin {}".format(get_current_branch()))  # Now pull the changes
    run_command("bun install")
    run_command("uv pip install -e .")
