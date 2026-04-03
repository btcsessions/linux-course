---
id: 4
week: 1
title: "Listing Files with ls"
duration_minutes: 15
objectives:
  - "List directory contents using ls with common flags"
  - "Read and interpret the output of ls -l (long format)"
  - "Show hidden files with ls -a and combine options effectively"
commands: [ls, ls -l, ls -la, ls -lh, ls -R, ls -t]
prerequisites: [3]
sandbox_commands: [ls, cd, pwd, whoami, hostname, date, cal, clear, echo, cat]
sandbox_setup: |
  mkdir -p myproject/src myproject/docs myproject/tests
  echo "fn main() {}" > myproject/src/main.rs
  echo "# My Project" > myproject/docs/README.md
  echo "test case 1" > myproject/tests/test1.py
  echo "Short file" > small.txt
  dd if=/dev/zero of=large_file.bin bs=1024 count=100 2>/dev/null
  echo "Medium content for a medium file with some text" > medium.txt
  touch .hidden_config
  echo "secret=value" > .env
  echo ".env" > .gitignore
  touch -t 202301010000 old_file.txt
  touch -t 202312310000 newer_file.txt
  touch recent_file.txt
  mkdir .cache
  echo "cached data" > .cache/data.tmp
---

# Listing Files with ls

## Seeing What Is Inside a Directory

You can navigate the filesystem with `cd` and find out where you are with `pwd`.
But how do you see what is actually *in* a directory? That is the job of `ls` --
short for **list**.

`ls` is one of the commands you will run dozens of times a day. It has many
options, but a handful of them cover the vast majority of use cases.

## Basic ls

With no arguments, `ls` lists the contents of your current directory:

```bash
ls
```

```
Desktop  Documents  Downloads  Music  Pictures  projects  Videos
```

You can also give it a path to list a different directory:

```bash
ls /etc
```

Or list a specific set of files using a pattern:

```bash
ls *.txt
```

By default, `ls` sorts entries alphabetically and displays them in columns. It
also uses colors to help you distinguish file types -- on CachyOS you will
typically see:

- **Blue** for directories
- **White** or default color for regular files
- **Green** for executable files
- **Cyan** for symbolic links
- **Red** for broken symbolic links

**Tip:** The colors come from the `LS_COLORS` environment variable or the
`dircolors` configuration. CachyOS sets this up for you automatically.

## The Long Format: ls -l

The plain `ls` output is compact but limited. To see detailed information about
each file, use the **long format**:

```bash
ls -l
```

```
total 24
drwxr-xr-x  2 alex alex 4096 Mar 27 08:00 Desktop
drwxr-xr-x  5 alex alex 4096 Mar 26 14:32 Documents
drwxr-xr-x  2 alex alex 4096 Mar 25 09:15 Downloads
-rw-r--r--  1 alex alex  215 Mar 27 07:00 notes.txt
-rwxr-xr-x  1 alex alex  892 Mar 26 11:00 script.sh
lrwxrwxrwx  1 alex alex   12 Mar 24 16:00 latest -> notes.txt
```

This is dense with information. Let us break down one line:

```
-rw-r--r--  1 alex alex  215 Mar 27 07:00 notes.txt
```

| Field | Value | Meaning |
|-------|-------|---------|
| `-rw-r--r--` | File type and permissions | First character: `-` = regular file, `d` = directory, `l` = symlink |
| `1` | Hard link count | Number of hard links to this file |
| `alex` | Owner | The user who owns the file |
| `alex` | Group | The group that owns the file |
| `215` | Size | File size in bytes |
| `Mar 27 07:00` | Modification time | When the file was last modified |
| `notes.txt` | Name | The filename |

### Understanding the Permissions String

The permissions string `-rw-r--r--` consists of 10 characters:

```
- rw- r-- r--
│ │   │   │
│ │   │   └── Others (everyone else): read only
│ │   └────── Group: read only
│ └────────── Owner: read and write
└──────────── File type: - = regular file
```

The three permission types are:

- `r` = read
- `w` = write
- `x` = execute

For now, just notice that the first character tells you whether something is a
file (`-`), directory (`d`), or symbolic link (`l`). We will explore permissions
in depth in a later week.

### Directories in Long Format

A directory entry looks like this:

```
drwxr-xr-x  5 alex alex 4096 Mar 26 14:32 Documents
```

The `d` at the beginning marks it as a directory. The `x` permission on a
directory means you can enter it with `cd`.

## Showing Hidden Files: ls -a

In Linux, any file or directory whose name starts with a dot (`.`) is considered
**hidden**. These do not show up in a normal `ls` listing.

Hidden files are commonly used for configuration:

- `.bashrc` -- bash shell configuration
- `.gitignore` -- tells Git which files to ignore
- `.config/` -- directory holding app configurations
- `.ssh/` -- SSH keys and configuration

To see hidden files, use the `-a` (all) flag:

```bash
ls -a
```

```
.  ..  .bashrc  .config  .gitignore  Desktop  Documents  Downloads
```

Notice the `.` and `..` entries. These are the current directory and parent
directory references you learned about in the previous lesson. They appear in
every directory.

If you want to see hidden files **without** the `.` and `..` entries, use `-A`
(almost all):

```bash
ls -A
```

```
.bashrc  .config  .gitignore  Desktop  Documents  Downloads
```

## Combining Flags

You can combine multiple flags together. The most common combination is:

```bash
ls -la
```

This gives you the long format **and** shows hidden files. You can also write it
as:

```bash
ls -l -a
```

Both forms are equivalent.

Another popular combination:

```bash
ls -lah
```

This adds the `-h` flag for **human-readable** file sizes.

## Human-Readable Sizes: ls -lh

By default, `ls -l` shows file sizes in bytes. For large files, this is hard to
read:

```
-rw-r--r--  1 alex alex 1073741824 Mar 27 08:00 big_file.iso
```

One billion bytes -- how many gigabytes is that? With `-h`, the output becomes:

```bash
ls -lh
```

```
-rw-r--r--  1 alex alex 1.0G Mar 27 08:00 big_file.iso
```

Much better. The `-h` flag converts sizes to K (kilobytes), M (megabytes), G
(gigabytes), and so on.

## Sorting Options

### By Modification Time: ls -lt

To see the most recently modified files first:

```bash
ls -lt
```

The newest files appear at the top. This is extremely useful when you want to
find what changed recently.

To reverse the order (oldest first), add `-r`:

```bash
ls -ltr
```

### By File Size: ls -lS

To sort by file size (largest first):

```bash
ls -lS
```

## Recursive Listing: ls -R

To see the contents of a directory **and** all of its subdirectories:

```bash
ls -R
```

```
.:
Desktop  Documents  Downloads

./Documents:
report.txt  school  work

./Documents/school:
math  history
```

This can produce a lot of output for large directory trees. Use it judiciously.

**Tip:** For a better tree view, try the `tree` command if it is installed. On
CachyOS you can install it with:

```bash
sudo pacman -S tree
```

Then run:

```bash
tree
```

## Listing Specific Files

You can use **glob patterns** (wildcards) with `ls`:

```bash
ls *.py          # All Python files
ls *.md          # All Markdown files
ls test_*        # All files starting with "test_"
ls -l *.txt      # Long format for all text files
```

The `*` matches any sequence of characters. We will cover glob patterns in more
detail later in the course.

## Useful ls Recipes

Here are the most common `ls` invocations you will use daily:

| Command | Purpose |
|---------|---------|
| `ls` | Quick look at the current directory |
| `ls -l` | Detailed listing with permissions and sizes |
| `ls -la` | Detailed listing including hidden files |
| `ls -lah` | Detailed listing with human-readable sizes and hidden files |
| `ls -lt` | Detailed listing sorted by modification time (newest first) |
| `ls -ltr` | Detailed listing sorted by modification time (oldest first) |
| `ls -lS` | Detailed listing sorted by size (largest first) |
| `ls -R` | Recursive listing of all subdirectories |
| `ls -d */` | List only directories (not their contents) |

## CachyOS-Specific Notes

- CachyOS typically aliases `ls` to `ls --color=auto` in the default shell
  configuration, so you get colored output automatically.
- If you are using fish, `ls` output may appear slightly different due to fish's
  own handling of colors and formatting.
- Some CachyOS editions come with `exa` or `eza` pre-installed, which are modern
  replacements for `ls` with enhanced features like Git integration and better
  formatting. Try `eza -la --git` if it is available on your system.

**Warning:** Do not confuse `ls -l` with `ll`. Many distributions create an
alias `ll` that maps to `ls -l` or `ls -la`. CachyOS may or may not have this
alias depending on your shell configuration. If `ll` does not work, just use
`ls -l`.

## Try It Yourself

Navigate to the sandbox and explore:

1. `cd /tmp/sandbox/myproject` and run `ls` to see the visible files.
2. Run `ls -a` to reveal hidden files like `.gitignore`, `.env`, and `.git`.
3. Run `ls -l` and identify which entries are files, directories, and symlinks.
4. Run `ls -lh` and compare the size column to `ls -l`.
5. Run `ls -lt` to see files sorted by modification time.
6. Run `ls -R` to see the entire project tree recursively.
7. Run `ls -la src/` to see the contents of the src directory in detail.
8. Try `ls *.md` to list only Markdown files.
9. Navigate to `docs/` and run `ls -l` -- can you spot the symbolic link?
10. Run `ls -d */` to list only subdirectories.

You can now see everything that is inside a directory. In the next lesson, you
will learn how to get help when you do not remember what a command does or what
options it supports.
