---
id: 11
week: 3
title: "Viewing File Contents"
duration_minutes: 15
objectives:
  - "Display entire file contents using cat, less, and more"
  - "View the beginning or end of files with head and tail"
  - "Monitor log files in real time with tail -f"
commands: [cat, less, more, head, "head -n", tail, "tail -n", "tail -f"]
prerequisites: []
sandbox_commands: [cat, less, head, tail, ls]
sandbox_setup: |
  #!/bin/bash
  # Create a 50-line sample file
  for i in $(seq 1 50); do
    echo "Line $i: This is sample content for demonstration purposes." >> ~/sample.txt
  done
  # Create a fake log file
  for i in $(seq 1 100); do
    ts=$(date -d "-$((100 - i)) minutes" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date '+%Y-%m-%d %H:%M:%S')
    level="INFO"
    if (( i % 10 == 0 )); then level="WARNING"; fi
    if (( i % 25 == 0 )); then level="ERROR"; fi
    echo "$ts [$level] Event number $i occurred in the application." >> ~/app.log
  done
  # Create a short config-style file
  cat > ~/config.conf <<'CONF'
  # Application Configuration
  app_name=MyApp
  version=2.1.0
  debug=false
  log_level=INFO
  max_connections=100
  timeout=30
  CONF
---
# Viewing File Contents

One of the most common tasks on any Linux system is reading files. Whether you are
inspecting configuration files, reviewing scripts, or tailing live logs, knowing the
right tool for the job will save you time and frustration. This lesson covers the
essential commands for viewing file contents on CachyOS and any other Linux
distribution.

## Displaying Entire Files with `cat`

The `cat` (short for **concatenate**) command prints the entire contents of one or
more files to the terminal.

```bash
cat sample.txt
```

You can also number every line with the `-n` flag:

```bash
cat -n sample.txt
```

Or show only non-blank line numbers with `-b`:

```bash
cat -b sample.txt
```

### Concatenating Multiple Files

`cat` can combine several files into one stream:

```bash
cat sample.txt config.conf
```

> **Tip:** `cat` dumps everything at once. For files longer than your terminal
> window, the beginning will scroll off-screen. Use `less` or `more` instead when
> you need to browse through large files.

## Paging Through Files with `less` and `more`

### `less` -- the Preferred Pager

`less` lets you scroll forward **and** backward through a file:

```bash
less sample.txt
```

Key bindings inside `less`:

| Key            | Action                      |
|----------------|-----------------------------|
| `Space` / `f`  | Forward one screen          |
| `b`            | Back one screen             |
| `j` / Down     | Forward one line            |
| `k` / Up       | Back one line               |
| `/pattern`     | Search forward for *pattern*|
| `?pattern`     | Search backward             |
| `n`            | Next search match           |
| `N`            | Previous search match       |
| `g`            | Go to beginning of file     |
| `G`            | Go to end of file           |
| `q`            | Quit                        |

> **CachyOS note:** `less` is installed by default. If you ever encounter a minimal
> container image where it is missing, install it with `sudo pacman -S less`.

### `more` -- the Classic Pager

`more` is an older pager that only scrolls forward:

```bash
more sample.txt
```

Press `Space` to advance one screen, `Enter` for one line, and `q` to quit.
In practice, `less` is almost always the better choice because it supports backward
scrolling and searching.

## Viewing the Start of a File with `head`

`head` prints the **first 10 lines** of a file by default:

```bash
head sample.txt
```

Use `-n` to specify a different number of lines:

```bash
head -n 5 sample.txt
head -n 20 app.log
```

This is perfect for quickly checking the header of a CSV, the shebang of a script,
or the top entries in a log file.

## Viewing the End of a File with `tail`

`tail` prints the **last 10 lines** by default:

```bash
tail sample.txt
```

Specify a custom number of lines:

```bash
tail -n 5 app.log
tail -n 20 app.log
```

### Following Logs in Real Time with `tail -f`

The `-f` flag keeps `tail` running and **follows** new lines as they are appended:

```bash
tail -f app.log
```

This is invaluable for monitoring live application logs, system journals, or any
file that grows over time. Press `Ctrl+C` to stop following.

> **Pro tip:** On CachyOS you can also use `journalctl -f` to follow systemd
> journal logs, but `tail -f` works on any plain text log file.

You can combine `-f` with `-n` to show more context before following:

```bash
tail -n 50 -f app.log
```

## Practical Comparison

| Scenario                        | Best Command           |
|---------------------------------|------------------------|
| Short file (< 1 screen)        | `cat`                  |
| Long file, need to browse       | `less`                 |
| Quick look at the top           | `head` / `head -n N`   |
| Quick look at the bottom        | `tail` / `tail -n N`   |
| Watch a log file live           | `tail -f`              |

## Try It Yourself

1. **View the full sample file:**
   ```bash
   cat -n sample.txt
   ```
   Notice the line numbers on the left.

2. **Page through the log file:**
   ```bash
   less app.log
   ```
   Try searching for `ERROR` by typing `/ERROR` and pressing Enter. Press `q` to
   quit.

3. **Check the first and last 5 lines:**
   ```bash
   head -n 5 app.log
   tail -n 5 app.log
   ```

4. **Follow the log file:**
   ```bash
   tail -f app.log
   ```
   In another terminal, append a line: `echo "NEW EVENT" >> ~/app.log` and watch it
   appear. Press `Ctrl+C` to stop.

5. **Inspect the config file:**
   ```bash
   cat config.conf
   ```

## Summary

- `cat` prints file contents in full -- best for short files.
- `less` is the go-to pager for browsing large files interactively.
- `more` is an older, forward-only pager.
- `head -n N` shows the first N lines; `tail -n N` shows the last N.
- `tail -f` follows a file in real time -- essential for log monitoring.
