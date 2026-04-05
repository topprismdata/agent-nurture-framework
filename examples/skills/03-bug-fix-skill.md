---
name: python-output-buffering-background-scripts
description: |
  Python buffers stdout and stderr when output is not connected to a terminal
  (TTY). This causes log files to appear empty even though the process is
  running and producing output. Use when: (1) Background script log file is
  empty but process is running (visible in ps), (2) Redirecting Python script
  output to a file and output does not appear, (3) Running Python scripts with
  nohup, screen, tmux, or systemd and logs are delayed or missing, (4) Python
  subprocess output not appearing in parent process logs. The fix is to use
  `python -u` flag, set PYTHONUNBUFFERED=1, or call sys.stdout.reconfigure().
author: Community
version: 1.0.0
date: 2026-01-15
tags: [python, debugging, output-buffering, background-process, logging]
---

# Python Output Buffering Trap for Background Scripts

## Problem

When a Python script is run in the background with output redirected to a file,
the log file may remain empty for hours even though the process is actively
running and producing output. This creates a misleading situation where the
process appears to be running correctly (it shows up in `ps`, consumes CPU and
memory) but produces no visible output. Developers waste time investigating
file permissions, path issues, or logging library configuration before
discovering the real cause: Python's output buffering behavior.

## Context / Trigger Conditions

This skill should be triggered when:

- A log file or output file from a Python script is empty or incomplete, but
  the process is confirmed to be running (`ps aux | grep script_name` shows
  an active process)
- Running a Python script with `nohup python script.py > output.log 2>&1 &`
  or similar background execution
- Using systemd, supervisord, or cron to run Python scripts and logs are delayed
- A Python subprocess's stdout/stderr is not appearing in the parent process's
  logs in real time
- Output appears in the log file only after the process terminates or after
  a very long delay

The key diagnostic clue: **the process is running but the log file is empty or
significantly behind real time.**

## Solution

### Root Cause

Python uses different buffering strategies depending on where stdout is connected:

- **Connected to a terminal (TTY):** Line buffering. Output is flushed after
  every newline character. This is the normal interactive behavior.
- **Connected to a file or pipe (not a TTY):** Fully buffered. Output is
  accumulated in a buffer (typically 4KB or 8KB) and only written when the
  buffer fills. For scripts that produce output infrequently (e.g., one line
  per minute during a long computation), the buffer may take hours to fill.

When you run `python script.py > output.log 2>&1 &`, stdout is connected to a
file, not a terminal. Python switches to fully buffered mode, and output is
delayed until the buffer fills.

### Fix Option 1: Unbuffered Flag (Recommended)

Run the script with the `-u` flag, which forces stdin, stdout, and stderr to
be unbuffered:

```bash
python -u script.py > output.log 2>&1 &
```

Or with nohup:

```bash
nohup python -u script.py > output.log 2>&1 &
```

This is the simplest fix and works for all scripts without code changes.

### Fix Option 2: Environment Variable

Set the `PYTHONUNBUFFERED` environment variable before running the script:

```bash
export PYTHONUNBUFFERED=1
python script.py > output.log 2>&1 &
```

Or inline:

```bash
PYTHONUNBUFFERED=1 python script.py > output.log 2>&1 &
```

This is useful when you cannot modify the command line (e.g., the script is
invoked by a wrapper tool) or when you want to apply the setting globally for
a session.

### Fix Option 3: Runtime Configuration

Modify the script to reconfigure stdout buffering at runtime:

```python
import sys

# Force line buffering on stdout
sys.stdout.reconfigure(line_buffering=True)

# Or for both stdout and stderr
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
```

This approach is useful when you control the script source and want the
buffering behavior to be embedded in the code. It is also useful when only
specific scripts need unbuffered output while others benefit from buffering.

### Fix Option 4: Explicit Flush

For fine-grained control, flush output explicitly at critical points:

```python
import sys

print("Processing started", flush=True)
# ... long computation ...
print(f"Result: {result}", flush=True)
```

This is the most targeted approach but requires modifying code at every point
where timely output is needed.

### Verification Commands

After applying the fix, verify that output appears immediately:

```bash
# Start the script in the background with the fix applied
python -u script.py > output.log 2>&1 &
PID=$!

# Wait a moment, then check if the log file has content
sleep 2
cat output.log

# Verify the process is still running
ps -p $PID
```

## Verification

- [ ] The script is running in the background (confirmed via `ps`)
- [ ] The log file contains output within seconds of the script starting
- [ ] Output continues to appear in near-real-time as the script runs
- [ ] The log file is complete after the script finishes (no truncated output)

## Example

### Problem Scenario

```bash
# Launch a long-running training script in the background
$ nohup python train_model.py > training.log 2>&1 &
[1] 42137

# Process is running
$ ps -p 42137
  PID TTY          TIME CMD
42137 pts/0    00:00:05 python

# But the log file is empty after 10 minutes
$ cat training.log
$

# Is it a permissions issue? No, the file exists and was created by the process
$ ls -la training.log
-rw-r--r-- 1 user user 0 Jan 15 10:30 training.log
```

### Resolution

```bash
# Kill the buffered process
$ kill 42137

# Relaunch with -u flag
$ nohup python -u train_model.py > training.log 2>&1 &
[1] 42201

# Output appears immediately
$ sleep 2 && cat training.log
[2026-01-15 10:32:01] Loading dataset...
[2026-01-15 10:32:03] Dataset loaded: 50000 rows, 20 features
[2026-01-15 10:32:03] Starting training...
```

## Notes

- This issue affects Python 2 and Python 3 equally. The `-u` flag works for both.
- The `print()` function in Python 3 has a `flush` parameter: `print("msg", flush=True)`.
- If using the `logging` module, note that `logging.StreamHandler` flushes after
  each emit by default. However, if the underlying stream is buffered, the flush
  may not reach the file immediately. The `-u` flag or `PYTHONUNBUFFERED=1`
  ensures the flush reaches the file.
- For Docker containers, add `ENV PYTHONUNBUFFERED=1` to the Dockerfile to
  ensure all Python processes in the container have unbuffered output.
- See also: `software-development-best-practices` for general debugging methodology
- See also: `logging-configuration-best-practices` for production logging setup

## References

- Python documentation on command line options: https://docs.python.org/3/using/cmdline.html
- Python `sys.stdout` documentation: https://docs.python.org/3/library/sys.html
- Stack Overflow: "Why does stdout need explicit flushing?" -- detailed explanation
  of Python's buffering behavior in different contexts
