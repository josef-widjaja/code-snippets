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

def print_stack(pid_stack):
    leading_spaces = ""
    while len(pid_stack) > 0:
        pid = pid_stack.pop()
        process_name = psutil.Process(pid).name() if psutil.pid_exists(pid) else "Unknown"
        print(f"{leading_spaces}{pid} {process_name}")
        leading_spaces = leading_spaces + " "

def add_ancestor_processes(pid, pid_stack):
    if pid == 1:  # root process, no ancestors
        return
    try:
        parent_pid = psutil.Process(pid).ppid()  # Get the parent PID of the current process
        pid_stack.append(parent_pid)
        add_ancestor_processes(parent_pid, pid_stack)  # Recursive call for the parent process
    except psutil.NoSuchProcess:
        pass  # If the process no longer exists, exit the recursion

def main():
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
        if process_id <= 0:
            print("Error: pid must be a positive integer.")
            print_usage()
        if not psutil.pid_exists(process_id):
            print(f"Error: Process with PID {process_id} does not exist.")
            print_usage()
    pid_ancestry_stack = deque()
    pid_ancestry_stack.append(process_id)
    add_ancestor_processes(process_id, pid_ancestry_stack)
    print_stack(pid_ancestry_stack)

if __name__ == "__main__":
    main()
