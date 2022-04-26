from datetime import datetime
import subprocess

def print_to_system(string_to_print):
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]: ")
    print(current_time + string_to_print)

def run_in_command_line(command):
    command = command.split(" ")
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.communicate()
    return process