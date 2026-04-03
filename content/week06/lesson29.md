---
id: 29
week: 6
title: "Job Control and Background Processes"
duration_minutes: 15
objectives:
  - "Run commands in the background with &"
  - "Manage jobs with jobs, fg, bg, and Ctrl+Z"
  - "Keep processes running after logout with nohup and disown"
commands: ["&", jobs, fg, bg, "Ctrl+Z", nohup, disown]
prerequisites: []
sandbox_commands: [sleep, jobs, fg, bg, nohup, disown, ps, kill, cat, echo, ls, cd, pwd, grep, wc, touch, mkdir, whoami, date, clear, bash]
sandbox_setup: |
  echo '#!/bin/bash' > counter.sh
  echo 'for i in $(seq 1 10); do echo "Count: $i"; sleep 1; done' >> counter.sh
  chmod +x counter.sh
  echo "Try: sleep 30 &" > README.txt
  echo "Then: jobs" >> README.txt
  echo "Then: fg %1" >> README.txt
---
# Job Control and Background Processes

So far, every command you have run has taken over the terminal until it
finished. That works fine for quick commands like `ls` or `grep`, but what
about a process that takes minutes -- or hours? You do not want to sit and
wait. Linux gives you a set of **job control** tools that let you pause, resume,
and juggle multiple tasks from a single terminal.

## Foreground vs. Background

When you run a command normally, it runs in the **foreground**. The shell waits
for it to finish before giving you a new prompt:

```bash
sleep 30        # the terminal is frozen for 30 seconds
```

A **background** process runs without blocking your prompt. You can keep working
while it does its thing.

## Starting a Command in the Background with `&`

Append an ampersand `&` to any command to launch it in the background:

```bash
sleep 30 &
```

The shell immediately prints two pieces of information and returns your prompt:

```
[1] 12345
$
```

- `[1]` is the **job number** (used by `fg`, `bg`, `jobs`).
- `12345` is the **PID** (process ID), used by `kill` and other tools.

You can now run other commands while `sleep` counts down silently.

### Launching multiple background tasks

```bash
~/demo/counter.sh &
~/demo/download_sim.sh > /tmp/download.log &
```

Each gets its own job number.

## Listing Jobs with `jobs`

At any time, see what the current shell is managing:

```bash
jobs
```

Sample output:

```
[1]-  Running                 sleep 30 &
[2]+  Running                 ./counter.sh &
```

The `+` marks the **current** (most recent) job; `-` marks the **previous** job.

Useful flags:

| Flag | Purpose |
|---|---|
| `jobs -l` | Show PIDs alongside job info |
| `jobs -r` | List only running jobs |
| `jobs -s` | List only stopped (suspended) jobs |

## Suspending a Foreground Process with Ctrl+Z

If a command is already running in the foreground and you want your prompt back,
press **Ctrl+Z**. This sends the `SIGTSTP` signal, which **suspends** (pauses)
the process:

```bash
sleep 120       # oops, this will take a while
# press Ctrl+Z
```

Output:

```
[1]+  Stopped                 sleep 120
$
```

The process is not dead -- it is frozen in place, waiting to be resumed.

## Resuming Jobs: `fg` and `bg`

### `fg` -- bring a job to the foreground

```bash
fg              # resumes the most recent job (+) in the foreground
fg %1           # resumes job number 1 specifically
fg %2           # resumes job number 2
```

### `bg` -- resume a stopped job in the background

If you suspended a process with Ctrl+Z but actually want it to keep running
without blocking your terminal:

```bash
bg              # resumes the most recent stopped job in the background
bg %1           # resumes job 1 in the background
```

This is the classic workflow for "I forgot the `&`":

1. Start a command: `./long_task.sh`
2. Realize it will take ages. Press **Ctrl+Z**.
3. Resume it in the background: `bg`
4. Carry on with other work.

## Job Identifiers

You can refer to jobs in several ways:

| Identifier | Meaning |
|---|---|
| `%1` | Job number 1 |
| `%+` or `%%` | Current (most recent) job |
| `%-` | Previous job |
| `%string` | Job whose command starts with *string* |
| `%?string` | Job whose command contains *string* |

Example:

```bash
sleep 100 &
vim notes.txt   # then Ctrl+Z to suspend vim
fg %sleep       # brings the sleep job forward
fg %?notes      # brings the vim job forward
```

## Killing Background Jobs

Use `kill` with the job number or PID:

```bash
kill %1          # send SIGTERM to job 1
kill 12345       # send SIGTERM to PID 12345
kill -9 %2       # send SIGKILL (forceful) to job 2
```

## Surviving Logout: `nohup` and `disown`

Background jobs started with `&` are still tied to your terminal session. If
you close the terminal or log out, the shell sends `SIGHUP` (hangup signal)
to all its jobs, which usually kills them.

### `nohup` -- start a command immune to hangup

```bash
nohup ~/demo/counter.sh &
```

`nohup` does two things:

1. Ignores the `SIGHUP` signal so the process survives logout.
2. Redirects stdout and stderr to a file called `nohup.out` (unless you
   redirect them yourself).

```bash
nohup ~/demo/counter.sh > /tmp/counter.log 2>&1 &
```

> **Tip:** Always redirect output when using `nohup`. Otherwise `nohup.out`
> grows without limit in your current directory.

### `disown` -- detach an already-running job

If you forgot to use `nohup`, you can retroactively detach a running background
job:

```bash
~/demo/counter.sh &        # started without nohup
disown %1                  # remove job 1 from the shell's job table
```

After `disown`, the shell will not send `SIGHUP` to that process when you log
out. However, stdout/stderr are still connected to the terminal, so redirect
them beforehand if needed:

```bash
~/demo/counter.sh > /tmp/output.log 2>&1 &
disown %1
```

### `nohup` vs. `disown` -- when to use which

| Scenario | Use |
|---|---|
| Starting a new long-running task | `nohup command &` |
| Already running, forgot `nohup` | `disown %jobnumber` |
| Want to redirect output automatically | `nohup` (creates nohup.out) |
| Want full control over redirection | `disown` with manual redirects |

## Practical Example: A Real Workflow

Imagine you are compiling a large program on CachyOS:

```bash
# Start the build
make -j$(nproc)

# It is taking forever. Suspend it.
# Press Ctrl+Z

# Resume in the background
bg

# Check on it occasionally
jobs

# Realize you need to log out. Detach it.
disown %1

# Log out safely -- the build continues
```

## Common Pitfalls

> **Warning:** Background processes that write to the terminal can produce
> jumbled output mixed with your typing. Redirect their output to a file:
> ```bash
> noisy_command > /tmp/output.log 2>&1 &
> ```

> **Warning:** `Ctrl+Z` does **not** kill a process. If you suspend many
> processes and forget about them, they sit in memory doing nothing. Use
> `jobs` regularly to check and `kill` what you no longer need.

## Try It Yourself

1. **Background a sleep.** Run `sleep 60 &`, then verify it with `jobs -l`.
   Note the PID, then kill it with `kill %1`.

2. **Suspend and resume.** Run `sleep 120` (no &). Press Ctrl+Z to suspend
   it. Then resume it in the background with `bg`. Confirm with `jobs`.

3. **Use nohup.** Start the counter script with nohup:
   ```bash
   nohup ~/demo/counter.sh > /tmp/nohup_test.log 2>&1 &
   ```
   Wait a few seconds, then check the log:
   ```bash
   cat /tmp/nohup_test.log
   ```

4. **Practice disown.** Start `sleep 300 &`, then run `disown %1`. Run `jobs`
   to confirm it no longer appears. Use `ps aux | grep sleep` to verify the
   process is still running.

5. **Multi-job juggling.** Start three sleep commands with different durations
   in the background. Use `jobs` to list them, bring one to the foreground
   with `fg %2`, suspend it with Ctrl+Z, then resume with `bg`.

> **Key takeaway:** Job control lets you multitask inside a single terminal.
> Learn the Ctrl+Z, `bg`, `fg` dance and you will never feel stuck waiting for
> a slow command again.
