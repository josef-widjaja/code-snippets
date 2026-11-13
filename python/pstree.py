#!/usr/bin/env python3
import argparse
import os
import sys
from collections import deque

import psutil


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

def print_ancestor_tree(pid):
    pid_ancestry_stack = deque()
    pid_ancestry_stack.append(pid)
    add_ancestor_processes(pid, pid_ancestry_stack)
    print_stack(pid_ancestry_stack)

def print_children(pid, level):
    try:
        process = psutil.Process(pid)
        print(f"{' ' * level}{pid} {process.name()}")
        for child in process.children():
            print_children(child.pid, level + 1)
    except psutil.NoSuchProcess:
        pass  # If the process no longer exists, exit the recursion

def print_descendant_tree(pid):
    print_children(pid, 0) # Start printing from the given PID with an initial indentation level of 0

def main():
    parser = argparse.ArgumentParser(description="Print process tree.")
    parser.add_argument("-d", "--descendants", action="store_true",
                        help="Print descendant processes instead of ancestor processes.")
    parser.add_argument("pid", nargs="?", type=int,
                        help="The process ID for which all ancestor processes will be printed.")

    args = parser.parse_args()
    if args.pid is None:
        process_id = os.getpid()  # Get the current process ID
    else:
        try:
            process_id= int(args.pid)
        except ValueError:
            print("Error: pid must be an integer.")
            sys.exit(1)
        if process_id <= 0:
            print("Error: pid must be a positive integer.")
            sys.exit(1)
        if not psutil.pid_exists(process_id):
            print(f"Error: Process with PID {process_id} does not exist.")
            sys.exit(1)

    if args.descendants:
        print_descendant_tree(process_id)
    else:
        print_ancestor_tree(process_id)

if __name__ == "__main__":
    main()
