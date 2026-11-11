#!/usr/bin/env python3
import os
import sys
from collections import deque

import psutil


def print_usage():  
    print("Usage: pstree [pid]")
    print("  pid: Optional. The process ID for which all ancestor processes will be printed.")
    print("      If no pid is provided, pid is set to the current process ID")
    print("  Example: pstree 1234")
    print("      process tree will be printed starting from root process to pid 1234")
    sys.exit(1)

if len(sys.argv) > 2:
    print_usage()
if len(sys.argv) == 1:
    process_id = os.getpid()  # Get the current process ID
if len(sys.argv) == 2:
    try:
        process_id= int(sys.argv[1])
    except ValueError:
        print("Error: pid must be an integer.")
        print_usage()

    if psutil.pid_exists(process_id):
        process_name = psutil.Process(process_id).name()
    else:
        print(f"Error: Process with PID {process_id} does not exist.")
        print_usage()

parent_pid = os.getppid()

pid_stack = deque()
pid_stack.append(process_id)
pid_stack.append(parent_pid)
while parent_pid != 1:  # Continue until we reach the root process (PID 1)
    try:
        parent_process = psutil.Process(parent_pid)
        parent_pid = parent_process.ppid()  # Get the parent PID of the current process
        pid_stack.append(parent_pid)
    except psutil.NoSuchProcess:
        break  # If the process no longer exists, exit the loop

leading_spaces = ""
while len(pid_stack) > 0:
    pid = pid_stack.pop()
    process_name = psutil.Process(pid).name() if psutil.pid_exists(pid) else "Unknown"
    print(f"{leading_spaces}{pid} {process_name}")
    leading_spaces = leading_spaces + " "
    