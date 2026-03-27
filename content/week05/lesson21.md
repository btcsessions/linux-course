---
id: 21
week: 5
title: "grep Fundamentals"
duration_minutes: 15
objectives:
  - "Search for text patterns in files using grep"
  - "Use essential grep flags: -i, -n, -c, -v, -l"
  - "Perform recursive searches with grep -r"
  - "Apply basic regular expressions in grep patterns"
commands: [grep, grep -i, grep -n, grep -v, grep -c, grep -r, grep -l]
prerequisites: []
sandbox_commands: [grep, cat, ls]
sandbox_setup: |
  mkdir -p /tmp/grep-practice/logs
  cat > /tmp/grep-practice/server.log <<'LOGEOF'
  2026-03-01 08:15:22 INFO Server started on port 8080
  2026-03-01 08:15:23 INFO Loading configuration from /etc/app/config.yaml
  2026-03-01 08:16:01 WARNING Disk usage at 85 percent
  2026-03-01 08:17:44 ERROR Failed to connect to database on host db01
  2026-03-01 08:17:45 INFO Retrying database connection...
  2026-03-01 08:17:46 INFO Database connection established
  2026-03-01 08:20:10 WARNING Memory usage above threshold
  2026-03-01 08:25:33 INFO User alice logged in from 192.168.1.10
  2026-03-01 08:30:12 INFO User bob logged in from 192.168.1.25
  2026-03-01 08:35:00 ERROR Timeout waiting for response from api.example.com
  2026-03-01 08:40:22 INFO User charlie logged in from 10.0.0.5
  2026-03-01 08:45:15 WARNING SSL certificate expires in 7 days
  2026-03-01 08:50:00 INFO Scheduled backup started
  2026-03-01 08:55:30 INFO Backup completed successfully
  2026-03-01 09:00:01 ERROR Disk write failed on /dev/sda2
  LOGEOF
  cat > /tmp/grep-practice/users.txt <<'USREOF'
  alice:x:1001:1001:Alice Johnson:/home/alice:/bin/bash
  bob:x:1002:1002:Bob Smith:/home/bob:/bin/zsh
  charlie:x:1003:1003:Charlie Brown:/home/charlie:/bin/bash
  diana:x:1004:1004:Diana Prince:/home/diana:/bin/fish
  eve:x:1005:1005:Eve Adams:/home/eve:/bin/bash
  frank:x:1006:1006:Frank Castle:/home/frank:/bin/zsh
  USREOF
  cat > /tmp/grep-practice/readme.txt <<'RDEOF'
  Project README
  ==============
  This project is a web application built with Python.
  It uses Flask for the backend and React for the frontend.

  Installation
  ------------
  1. Install python3 and pip
  2. Run pip install -r requirements.txt
  3. Set the DATABASE_URL environment variable
  4. Run python3 app.py

  The application listens on port 5000 by default.
  You can change the port with the PORT environment variable.
  For production, use gunicorn instead of the built-in server.

  Contributing
  ------------
  Please read CONTRIBUTING.md before submitting a pull request.
  All Python code must pass flake8 and black formatting.
  RDEOF
  cat > /tmp/grep-practice/logs/app1.log <<'A1EOF'
  ERROR: connection refused
  INFO: request handled in 52ms
  ERROR: timeout after 30s
  INFO: health check passed
  A1EOF
  cat > /tmp/grep-practice/logs/app2.log <<'A2EOF'
  INFO: service started
  WARNING: deprecated API called
  ERROR: null pointer exception
  INFO: request handled in 12ms
  A2EOF
---

# grep Fundamentals

## Why grep Matters

If there is one command that separates casual Linux users from effective ones, it
is `grep`. The name stands for **Global Regular Expression Print**, and its job
is beautifully simple: search through text and print lines that match a pattern.

System administrators use `grep` dozens of times a day -- to hunt through log
files, find configuration settings, locate error messages, and filter command
output. Once you master `grep`, you will wonder how you ever managed without it.

## Basic grep Usage

The simplest form of `grep` takes a pattern and a filename:

```bash
grep "pattern" filename
```

Let's try it with the sample server log:

```bash
grep "ERROR" /tmp/grep-practice/server.log
```

Output:

```
2026-03-01 08:17:44 ERROR Failed to connect to database on host db01
2026-03-01 08:35:00 ERROR Timeout waiting for response from api.example.com
2026-03-01 09:00:01 ERROR Disk write failed on /dev/sda2
```

Only the lines containing the exact string "ERROR" are printed. Everything else
is silently ignored.

## Essential Flags

### Case-Insensitive Search: -i

By default, `grep` is case-sensitive. To ignore case:

```bash
grep -i "error" /tmp/grep-practice/server.log
```

This matches "ERROR", "Error", "error", and any other combination of upper and
lowercase letters. This is particularly useful when you are not sure how a word
was capitalized in a file.

### Show Line Numbers: -n

When working with large files, you need to know *where* a match occurred:

```bash
grep -n "INFO" /tmp/grep-practice/server.log
```

Output:

```
1:2026-03-01 08:15:22 INFO Server started on port 8080
2:2026-03-01 08:15:23 INFO Loading configuration from /etc/app/config.yaml
5:2026-03-01 08:17:45 INFO Retrying database connection...
6:2026-03-01 08:17:46 INFO Database connection established
8:2026-03-01 08:25:33 INFO User alice logged in from 192.168.1.10
9:2026-03-01 08:30:12 INFO User bob logged in from 192.168.1.25
11:2026-03-01 08:40:22 INFO User charlie logged in from 10.0.0.5
13:2026-03-01 08:50:00 INFO Scheduled backup started
14:2026-03-01 08:55:30 INFO Backup completed successfully
```

The number before each line tells you exactly which line in the file matched.

### Count Matches: -c

Sometimes you do not need the actual lines -- you just want to know how many
matches there are:

```bash
grep -c "INFO" /tmp/grep-practice/server.log
```

```
9
```

This is much faster than piping to `wc -l` when you only need a count.

### Invert the Match: -v

The `-v` flag shows every line that does **not** match the pattern:

```bash
grep -v "INFO" /tmp/grep-practice/server.log
```

This prints all lines that are NOT informational -- the warnings and errors. It
is a quick way to filter out the noise and focus on problems.

### List Matching Files: -l

When you have many files, sometimes you only need to know *which files* contain
a match, not the matching lines themselves:

```bash
grep -l "ERROR" /tmp/grep-practice/logs/*.log
```

```
/tmp/grep-practice/logs/app1.log
/tmp/grep-practice/logs/app2.log
```

This is extremely useful when scanning a directory full of configuration files
or log files.

## Recursive Search with -r

One of the most powerful features of `grep` is searching through entire directory
trees. The `-r` (recursive) flag tells `grep` to descend into subdirectories:

```bash
grep -r "ERROR" /tmp/grep-practice/
```

This searches every file inside `/tmp/grep-practice/` and all its
subdirectories. The output prefixes each match with the filename:

```
/tmp/grep-practice/server.log:2026-03-01 08:17:44 ERROR Failed to connect...
/tmp/grep-practice/server.log:2026-03-01 08:35:00 ERROR Timeout waiting...
/tmp/grep-practice/server.log:2026-03-01 09:00:01 ERROR Disk write failed...
/tmp/grep-practice/logs/app1.log:ERROR: connection refused
/tmp/grep-practice/logs/app1.log:ERROR: timeout after 30s
/tmp/grep-practice/logs/app2.log:ERROR: null pointer exception
```

**Tip:** You can combine `-r` with other flags. For example, `grep -rn "ERROR"
/tmp/grep-practice/` shows filenames *and* line numbers.

## Combining Flags

You can stack flags together. Here are some common combinations:

```bash
# Case-insensitive search with line numbers
grep -in "warning" /tmp/grep-practice/server.log

# Count non-matching lines
grep -vc "INFO" /tmp/grep-practice/server.log

# Recursive, case-insensitive, with line numbers
grep -rin "error" /tmp/grep-practice/
```

Flags can be combined in a single dash (`-in`) or given separately (`-i -n`).
Both forms work identically.

## Basic Regular Expressions

`grep` does not just match literal strings -- it understands patterns called
**regular expressions** (regex). Here are the basics:

### The Dot: Match Any Character

The `.` (dot) matches any single character:

```bash
grep "User .* logged" /tmp/grep-practice/server.log
```

This matches "User alice logged", "User bob logged", etc.

### Anchors: Start and End of Line

- `^` matches the **start** of a line
- `$` matches the **end** of a line

```bash
# Lines that start with "2026-03-01 09"
grep "^2026-03-01 09" /tmp/grep-practice/server.log

# Lines that end with "bash"
grep "bash$" /tmp/grep-practice/users.txt
```

The `bash$` pattern finds all users whose shell is bash.

### Searching for Literal Special Characters

If you need to search for a character that has special regex meaning (like `.`
or `$`), escape it with a backslash:

```bash
grep "192\.168\.1\.10" /tmp/grep-practice/server.log
```

Without the backslashes, the dots would match *any* character, potentially
giving you false matches.

## Searching Command Output with Pipes

You are not limited to searching files. You can pipe any command's output into
`grep`:

```bash
cat /tmp/grep-practice/users.txt | grep "bash"
```

Or more practically:

```bash
ls -la /tmp/grep-practice/ | grep "log"
```

**Tip:** When searching a single file, pass the filename directly to `grep`
rather than using `cat | grep`. It is more efficient and considered better
practice.

**Warning:** Be careful with `grep -r` in directories that contain binary files
or symbolic links. You may want to add `--include="*.log"` to limit searches to
specific file types:

```bash
grep -r --include="*.log" "ERROR" /tmp/grep-practice/
```

## CachyOS-Specific Notes

On CachyOS (and all Arch-based systems), `grep` is part of the core system and
is always installed. CachyOS also includes GNU grep by default, which supports
all the flags covered in this lesson. If you ever need a faster alternative for
very large codebases, you can install `ripgrep` with:

```bash
sudo pacman -S ripgrep
```

The `rg` command from ripgrep is compatible with many `grep` patterns but adds
speed and smart defaults like automatic recursion and .gitignore awareness.

## Try It Yourself

Open your terminal and work through these exercises using the sandbox files:

1. Find all WARNING lines in `server.log`.
2. Count how many INFO lines are in `server.log` using `grep -c`.
3. Show all lines in `server.log` that are NOT INFO messages.
4. Find all users who use `/bin/bash` in `users.txt`.
5. Search recursively for the word "error" (case-insensitive) in the entire
   `/tmp/grep-practice/` directory.
6. Use `grep -l` to find which log files in `/tmp/grep-practice/logs/` mention
   "timeout" (case-insensitive).
7. Find lines in `users.txt` that start with "alice" using the `^` anchor.
8. Combine `-n` and `-i` to find all lines mentioning "database" in `server.log`
   with their line numbers.

In the next lesson, you will unlock the full power of grep by learning regular
expressions in depth.
