---
id: 20
week: 4
title: "Process Basics"
duration_minutes: 15
objectives:
  - "List running processes with ps and ps aux"
  - "Monitor system activity interactively with top and htop"
  - "Send signals to processes with kill, kill -9, and killall"
commands: [ps, "ps aux", top, htop, kill, "kill -9", killall, pgrep]
prerequisites: []
sandbox_commands: [ps, kill, pgrep, chown, chgrp, chmod, id, groups, whoami, cat, less, grep, ls, cd, pwd, echo, touch, mkdir, cp, head, tail, find, wc, sort, cut, stat, file, clear, date, sleep]
sandbox_setup: |
  sleep 300 &
  sleep 300 &
  sleep 300 &
  echo "Three background processes started." > README.txt
  echo "Use 'ps' or 'ps aux' to see them." >> README.txt
  echo "Use 'kill <PID>' to stop them." >> README.txt
---
# Process Basics

Every program running on your Linux system is a **process**. Even the shell you are
typing into is a process. Understanding how to view, monitor, and control processes is
a core skill for any Linux user. This lesson introduces the essential tools for
process management on CachyOS.

## What Is a Process?

A process is an instance of a running program. When you type `ls`, the kernel creates
a new process, runs the `ls` binary, and destroys the process when it finishes. Long-
running programs like web servers, editors, and your desktop environment are also
processes -- they just do not exit immediately.

Every process has:

- A **PID** (Process ID) -- a unique number assigned by the kernel.
- A **PPID** (Parent Process ID) -- the PID of the process that started it.
- A **user** -- the account it runs as.
- A **state** -- running, sleeping, stopped, zombie, etc.

## Listing Processes with `ps`

The `ps` command shows a snapshot of current processes. By itself, it shows only
processes attached to your current terminal:

```bash
ps
```

Output:

```
    PID TTY          TIME CMD
   1234 pts/0    00:00:00 bash
   1250 pts/0    00:00:00 ps
```

This is rarely enough information. The real power comes with flags.

### `ps aux` -- The Standard Overview

The most commonly used form is:

```bash
ps aux
```

| Flag | Meaning                          |
|------|----------------------------------|
| `a`  | Show processes from all users    |
| `u`  | Display in user-oriented format  |
| `x`  | Include processes without a terminal (daemons) |

Sample output:

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1 169836 13200 ?        Ss   09:00   0:01 /sbin/init
root           2  0.0  0.0      0     0 ?        S    09:00   0:00 [kthreadd]
alex        1234  0.0  0.1  10456  5600 pts/0    Ss   09:05   0:00 /bin/bash
alex        5678  2.3  1.5 412000 60000 ?        Sl   09:10   0:30 /usr/bin/firefox
```

### Understanding the Columns

| Column  | Meaning                                              |
|---------|------------------------------------------------------|
| USER    | The user who owns the process                        |
| PID     | Process ID                                           |
| %CPU    | CPU usage percentage                                 |
| %MEM    | Memory usage percentage                              |
| VSZ     | Virtual memory size (KB)                             |
| RSS     | Resident set size -- actual physical memory used (KB)|
| TTY     | Terminal associated with the process (`?` = none)    |
| STAT    | Process state (see below)                            |
| START   | When the process started                             |
| TIME    | Total CPU time consumed                              |
| COMMAND | The command that launched the process                 |

### Process States (STAT Column)

| Code | Meaning                                       |
|------|-----------------------------------------------|
| `R`  | Running or runnable                           |
| `S`  | Sleeping (waiting for an event)               |
| `D`  | Uninterruptible sleep (usually I/O)           |
| `T`  | Stopped (e.g., by Ctrl+Z)                     |
| `Z`  | Zombie (terminated but not yet reaped)        |

Additional modifiers appear after the main code:

| Modifier | Meaning                        |
|----------|--------------------------------|
| `s`      | Session leader                 |
| `l`      | Multi-threaded                 |
| `+`      | In the foreground process group|
| `<`      | High priority                  |
| `N`      | Low priority (nice)            |

### Filtering `ps` Output with `grep`

To find a specific process:

```bash
ps aux | grep firefox
```

> **Tip:** This also matches the `grep` command itself. To avoid that:
> ```bash
> ps aux | grep [f]irefox
> ```
> The bracket trick makes the grep pattern different from the literal string, so
> grep does not match its own process.

## Finding Processes with `pgrep`

A cleaner alternative to `ps | grep` is `pgrep`:

```bash
pgrep firefox
```

This returns just the PID(s). Useful options:

```bash
pgrep -l firefox      # Show PID and process name
pgrep -u alex         # Processes owned by user alex
pgrep -a sleep        # Show PID and full command line
```

## Interactive Monitoring with `top`

While `ps` gives a snapshot, `top` provides a **live, updating** view of system
activity:

```bash
top
```

The display refreshes every few seconds and shows:

- **System summary:** uptime, load averages, CPU percentages, memory usage.
- **Process table:** sorted by CPU usage by default.

### Key Commands Inside `top`

| Key   | Action                              |
|-------|-------------------------------------|
| `q`   | Quit                                |
| `k`   | Kill a process (prompts for PID)    |
| `M`   | Sort by memory usage                |
| `P`   | Sort by CPU usage (default)         |
| `u`   | Filter by user                      |
| `h`   | Help screen                         |
| `1`   | Toggle per-CPU core display         |

### Understanding Load Averages

At the top of `top` you will see something like:

```
load average: 0.52, 0.38, 0.41
```

These three numbers represent the average number of processes in the run queue over
the last 1, 5, and 15 minutes. As a rule of thumb:

- **Below your CPU count:** the system is underloaded.
- **Equal to your CPU count:** the system is fully utilised.
- **Above your CPU count:** processes are waiting for CPU time.

Check your CPU count with `nproc`.

## Better Monitoring with `htop`

`htop` is an improved, colourful alternative to `top`. It is pre-installed on CachyOS:

```bash
htop
```

Advantages of `htop` over `top`:

- Colour-coded CPU and memory bars.
- Horizontal and vertical scrolling through the process list.
- Mouse support for selecting processes.
- Tree view showing parent-child relationships (`F5`).
- Easier process killing (select a process, press `F9`).

### Useful `htop` Keys

| Key    | Action                         |
|--------|--------------------------------|
| `F5`   | Toggle tree view               |
| `F6`   | Choose sort column             |
| `F9`   | Send a signal (kill)           |
| `F10`  | Quit                           |
| `/`    | Search for a process           |
| `t`    | Toggle tree view (alternate)   |

> **Tip:** If `htop` is not installed, install it with:
> ```bash
> sudo pacman -S htop
> ```

## Signals and the `kill` Command

Despite its name, `kill` does not always kill processes. It sends **signals** to them.
The process decides how to handle the signal (unless the signal is uncatchable).

### Common Signals

| Signal  | Number | Name     | Default Action                    |
|---------|--------|----------|-----------------------------------|
| SIGTERM | 15     | Terminate| Graceful shutdown (default)       |
| SIGKILL | 9      | Kill     | Immediate termination (uncatchable)|
| SIGHUP  | 1      | Hangup   | Often causes daemons to reload config|
| SIGSTOP | 19     | Stop     | Pause the process (uncatchable)   |
| SIGCONT | 18     | Continue | Resume a stopped process          |
| SIGINT  | 2      | Interrupt| Same as pressing Ctrl+C           |

### Using `kill`

The basic syntax is:

```bash
kill PID
```

This sends `SIGTERM` (signal 15), asking the process to shut down gracefully. The
process can catch this signal and perform cleanup before exiting.

If a process ignores `SIGTERM`, force it with `SIGKILL`:

```bash
kill -9 PID
```

Or equivalently:

```bash
kill -SIGKILL PID
```

> **Warning:** `kill -9` should be a **last resort**. It terminates the process
> immediately without giving it a chance to save data, close files, or clean up
> temporary files. Always try a regular `kill` first and wait a few seconds.

### Killing by Name with `killall`

Instead of looking up PIDs, you can kill all processes with a given name:

```bash
killall firefox
```

This sends `SIGTERM` to every process named `firefox`. You can also specify a signal:

```bash
killall -9 firefox
```

> **Warning:** Be careful with `killall`. If the process name matches more than you
> expect, you could kill important processes. Use `pgrep -l name` first to verify
> what you are about to kill.

## Putting It All Together

Here is a typical workflow for dealing with a misbehaving application:

1. **Find the process:**
   ```bash
   pgrep -a problematic-app
   ```

2. **Check its resource usage:**
   ```bash
   ps aux | grep problematic-app
   ```

3. **Try a graceful termination:**
   ```bash
   kill 12345
   ```

4. **Wait a few seconds and check if it stopped:**
   ```bash
   pgrep problematic-app
   ```

5. **Force kill if necessary:**
   ```bash
   kill -9 12345
   ```

## Keyboard Shortcuts for Process Control

When running a command in the terminal, these shortcuts send signals directly:

| Shortcut   | Signal  | Effect                        |
|------------|---------|-------------------------------|
| `Ctrl+C`   | SIGINT  | Interrupt (usually terminates)|
| `Ctrl+Z`   | SIGTSTP | Suspend (pause) the process   |
| `Ctrl+\`   | SIGQUIT | Quit with core dump           |

After pressing `Ctrl+Z`, the process is stopped. You can resume it:

```bash
fg          # Resume in the foreground
bg          # Resume in the background
```

## Try It Yourself

1. **List all running processes:**
   ```bash
   ps aux
   ```

2. **Find the background sleep processes:**
   ```bash
   pgrep -a sleep
   ```

3. **Check the process details:**
   ```bash
   ps aux | grep sleep
   ```

4. **Send a graceful termination signal:**
   ```bash
   kill $(cat /tmp/sleep1.pid)
   pgrep -a sleep
   ```
   One of the sleep processes should be gone.

5. **Force kill the other:**
   ```bash
   kill -9 $(cat /tmp/sleep2.pid)
   pgrep -a sleep
   ```

6. **Try `top` briefly:**
   ```bash
   top
   ```
   Press `q` to quit. Notice how the display updates automatically.

## Summary

- A **process** is a running instance of a program, identified by a unique PID.
- `ps aux` shows a snapshot of all processes on the system with user, CPU, memory,
  and state information.
- `pgrep` finds process IDs by name, avoiding the need for `ps | grep`.
- `top` and `htop` provide live, interactive process monitoring. `htop` is the more
  user-friendly option on CachyOS.
- `kill PID` sends SIGTERM (graceful shutdown). `kill -9 PID` sends SIGKILL (forced).
- `killall name` kills all processes matching a name.
- Always try a graceful `kill` before resorting to `kill -9`.
- `Ctrl+C` interrupts a foreground process; `Ctrl+Z` suspends it.
