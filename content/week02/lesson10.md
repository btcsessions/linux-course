---
id: 10
week: 2
title: "Finding Files with find and locate"
duration_minutes: 15
objectives:
  - "Find files by name, type, and size using the find command"
  - "Use locate and plocate for fast filename searches"
  - "Execute commands on found files with find -exec"
commands: [find, locate, plocate]
prerequisites: []
sandbox_commands: [find, ls]
sandbox_setup: |
  mkdir -p ~/practice/project/{src,tests,docs,config,logs}
  mkdir -p ~/practice/project/src/{components,utils}
  touch ~/practice/project/src/main.py
  touch ~/practice/project/src/app.py
  touch ~/practice/project/src/components/header.py
  touch ~/practice/project/src/components/footer.py
  touch ~/practice/project/src/utils/helpers.py
  touch ~/practice/project/tests/test_main.py
  touch ~/practice/project/tests/test_app.py
  touch ~/practice/project/docs/readme.md
  touch ~/practice/project/docs/guide.md
  touch ~/practice/project/docs/api.txt
  touch ~/practice/project/config/settings.conf
  touch ~/practice/project/config/database.conf
  echo "debug info line 1" > ~/practice/project/logs/app.log
  echo "error on line 42" > ~/practice/project/logs/error.log
  dd if=/dev/zero of=~/practice/project/logs/large.log bs=1024 count=200 2>/dev/null
  touch ~/practice/project/.gitignore
  touch ~/practice/project/src/.env
  cd ~/practice
---

# Finding Files with find and locate

As your filesystem grows, remembering exactly where you put a file becomes
impossible. You need tools that can search for files across directories and
even the entire system. Linux provides two main approaches: `find` (thorough
but slower) and `locate`/`plocate` (fast but uses a pre-built database).

## The `find` Command

`find` is the Swiss Army knife of file searching. It walks through a directory
tree in real time, checking each file against criteria you specify.

### Basic syntax

```bash
find [starting-path] [options/tests] [actions]
```

- **starting-path** -- where to begin searching (defaults to `.` if omitted).
- **options/tests** -- what to look for (name, type, size, etc.).
- **actions** -- what to do with matches (print, delete, execute a command).

### Finding files by name

The most common use is searching by filename with `-name`:

```bash
find . -name "main.py"
```
```
./project/src/main.py
```

The `.` means "start searching from the current directory." The search is
recursive -- it descends into every subdirectory.

**Case-insensitive search** with `-iname`:

```bash
find . -iname "readme*"
```
```
./project/docs/readme.md
```

This matches `README.md`, `Readme.md`, `readme.md`, and so on.

### Using wildcards with find

You can use glob patterns inside the `-name` argument, but you **must** quote
them so the shell does not expand them before `find` sees them:

```bash
find . -name "*.py"
```
```
./project/src/main.py
./project/src/app.py
./project/src/components/header.py
./project/src/components/footer.py
./project/src/utils/helpers.py
./project/tests/test_main.py
./project/tests/test_app.py
```

**Warning:** If you forget the quotes, the shell may expand `*.py` to files in
the current directory, and `find` will not search correctly:

```bash
# WRONG -- shell expands *.py before find runs
find . -name *.py

# RIGHT -- quotes protect the pattern
find . -name "*.py"
```

### Finding by file type

The `-type` test filters by file type:

| Flag | Meaning |
|------|---------|
| `-type f` | Regular files |
| `-type d` | Directories |
| `-type l` | Symbolic links |

**Find all directories:**

```bash
find . -type d
```
```
.
./project
./project/src
./project/src/components
./project/src/utils
./project/tests
./project/docs
./project/config
./project/logs
```

**Find only files (not directories) named with "test":**

```bash
find . -type f -name "test*"
```
```
./project/tests/test_main.py
./project/tests/test_app.py
```

### Finding by size

The `-size` test filters by file size:

```bash
find . -size +100k          # files larger than 100 kilobytes
find . -size -1k            # files smaller than 1 kilobyte
find . -size 200k           # files exactly 200 kilobytes (rare)
```

Size suffixes:

| Suffix | Meaning |
|--------|---------|
| `c` | Bytes |
| `k` | Kilobytes (1024 bytes) |
| `M` | Megabytes |
| `G` | Gigabytes |

**Example -- find large log files:**

```bash
find . -name "*.log" -size +100k
```
```
./project/logs/large.log
```

### Finding by modification time

The `-mtime` test filters by when a file was last modified:

```bash
find . -mtime -1            # modified less than 1 day ago
find . -mtime +7            # modified more than 7 days ago
find . -mtime 0             # modified today
```

For minutes instead of days, use `-mmin`:

```bash
find . -mmin -30            # modified in the last 30 minutes
```

### Combining multiple tests

Tests are combined with AND logic by default:

```bash
find . -type f -name "*.py" -size +0c
```

This finds regular files that end with `.py` and are not empty.

You can use `-o` for OR logic (with parentheses):

```bash
find . \( -name "*.py" -o -name "*.md" \) -type f
```

This finds files ending with `.py` **or** `.md`. The backslashes before the
parentheses prevent the shell from interpreting them.

### Limiting search depth

By default, `find` descends into every nested directory. To limit depth:

```bash
find . -maxdepth 1 -name "*.py"     # current directory only
find . -maxdepth 2 -name "*.py"     # current dir + one level down
```

## Acting on Results with `-exec`

The real power of `find` is combining search with action. The `-exec` flag runs
a command on each matching file.

### Syntax

```bash
find . -name "*.log" -exec command {} \;
```

- `{}` is a placeholder that gets replaced with each matching filename.
- `\;` marks the end of the command (the backslash prevents the shell from
  interpreting the semicolon).

### Examples

**Show details of each Python file:**

```bash
find . -name "*.py" -exec ls -l {} \;
```

**Count lines in each Python file:**

```bash
find . -name "*.py" -exec wc -l {} \;
```

**Delete all `.log` files (be careful):**

```bash
find . -name "*.log" -exec rm {} \;
```

**Copy all config files to a backup directory:**

```bash
mkdir -p backup/
find . -name "*.conf" -exec cp {} backup/ \;
```

### Using `+` instead of `\;` for efficiency

Replacing `\;` with `+` passes multiple filenames to the command at once
instead of running it once per file:

```bash
find . -name "*.py" -exec ls -l {} +
```

This is faster because `ls` runs once with all matching files as arguments,
rather than once per file.

### The `-delete` action

For deleting matched files, `find` has a built-in `-delete` action that is
safer to type than `-exec rm`:

```bash
find . -name "*.tmp" -delete
```

**Warning:** Always test your `find` command **without** `-delete` first to see
what would be matched:

```bash
find . -name "*.tmp"              # check matches first
find . -name "*.tmp" -delete      # then delete
```

## Fast Searching with `locate` and `plocate`

While `find` searches the filesystem in real time, `locate` (and its modern
replacement `plocate`) searches a pre-built database of filenames. This makes
it dramatically faster.

### Installing on CachyOS

CachyOS (being Arch-based) uses `plocate` as the modern replacement for
`mlocate`:

```bash
sudo pacman -S plocate
```

After installation, you need to build the database:

```bash
sudo updatedb
```

### Basic usage

```bash
locate main.py
```
```
/home/alex/practice/project/src/main.py
/home/alex/other_project/main.py
```

`locate` searches the **entire system** and returns results almost instantly.

### Case-insensitive search

```bash
locate -i readme
```

### Limiting results

```bash
locate -n 5 "*.conf"       # show only first 5 matches
```

### Counting matches

```bash
locate -c "*.py"            # count how many .py files exist
```

### The database limitation

The `locate` database is a snapshot. It is typically updated once a day by a
systemd timer. This means:

- **Recently created files** may not appear in results.
- **Recently deleted files** may still appear.

To update the database manually:

```bash
sudo updatedb
```

On CachyOS, the systemd timer `plocate-updatedb.timer` handles automatic
daily updates. You can check its status:

```bash
systemctl status plocate-updatedb.timer
```

## `find` vs `locate`: When to Use Which

| Aspect | `find` | `locate` / `plocate` |
|--------|--------|---------------------|
| Speed | Slower (real-time search) | Very fast (database lookup) |
| Accuracy | Always current | May be stale |
| Search scope | Any directory you specify | Entire system |
| Filters | Name, type, size, time, permissions, etc. | Name only |
| Actions | `-exec`, `-delete`, etc. | Print only |
| Installation | Always available | May need `sudo pacman -S plocate` |

**Rule of thumb:**

- Use `locate` when you just need to find where a file lives on the system.
- Use `find` when you need precise, up-to-date results or want to filter by
  more than just the name.

## Practical Patterns

### Find all files modified today in a project

```bash
find ~/project -type f -mtime 0
```

### Find and remove old log files

```bash
find /var/log -name "*.log" -mtime +30 -exec rm {} \;
```

### Find empty files and directories

```bash
find . -empty -type f          # empty files
find . -empty -type d          # empty directories
```

### Find files by permission

```bash
find . -perm 755               # exact permission match
find . -perm -u+x              # user has execute permission
```

### Find hidden files (dotfiles)

```bash
find . -name ".*" -type f
```
```
./project/.gitignore
./project/src/.env
```

### Quick "where is this file?" with locate

```bash
locate pacman.conf
```
```
/etc/pacman.conf
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `find -name *.py` without quotes | Shell expands the glob | Quote it: `find -name "*.py"` |
| Forgetting `\;` at the end of `-exec` | Syntax error | Always end with `\;` or `+` |
| Running `-delete` without testing first | Wrong files deleted | Test with just `find` first |
| Relying on `locate` for recent files | File not in database yet | Run `sudo updatedb` or use `find` |
| Searching from `/` without depth limits | Very slow on large systems | Use `-maxdepth` or start from a specific directory |

## CachyOS-Specific Notes

CachyOS uses `plocate` rather than the older `mlocate`. The commands are the
same (`locate` is a symlink to `plocate`), but `plocate` is significantly
faster and uses less disk space for its database.

If `locate` is not available after installation, make sure the database has
been built with `sudo updatedb`. The `plocate-updatedb.timer` systemd unit
will keep it updated daily going forward.

## Try It Yourself

1. Find all Python files in the practice directory:
   ```bash
   find . -name "*.py"
   ```

2. Find all directories:
   ```bash
   find . -type d
   ```

3. Find files larger than 100k:
   ```bash
   find . -size +100k
   ```

4. Find all `.conf` files and list their details:
   ```bash
   find . -name "*.conf" -exec ls -l {} \;
   ```

5. Find hidden files:
   ```bash
   find . -name ".*" -type f
   ```

6. Find all Markdown files and count them:
   ```bash
   find . -name "*.md" | wc -l
   ```

7. Find files modified in the last 60 minutes:
   ```bash
   find . -mmin -60 -type f
   ```

8. Limit search to the top two levels:
   ```bash
   find . -maxdepth 2 -name "*.py"
   ```

9. Find empty directories:
   ```bash
   find . -type d -empty
   ```

10. Combine criteria -- find Python test files:
    ```bash
    find . -name "test_*.py" -type f
    ```

## Summary

| Command | Purpose |
|---------|---------|
| `find . -name "pattern"` | Find files by name |
| `find . -iname "pattern"` | Case-insensitive name search |
| `find . -type f` | Find regular files only |
| `find . -type d` | Find directories only |
| `find . -size +100k` | Find files larger than 100KB |
| `find . -mtime -1` | Find files modified in the last day |
| `find . -name "*.py" -exec cmd {} \;` | Run a command on each match |
| `find . -name "*.tmp" -delete` | Delete matching files |
| `find . -maxdepth 2` | Limit search depth |
| `locate filename` | Fast search using pre-built database |
| `sudo updatedb` | Rebuild the locate database |

You now have the tools to find any file on your system, no matter how deeply
it is buried. Combined with the wildcards you learned in Lesson 9, you can
work with files efficiently at any scale. This concludes Week 2 -- you have
gone from creating files and directories to copying, moving, deleting, pattern
matching, and searching for them.
