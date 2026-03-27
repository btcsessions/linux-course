---
id: 6
week: 2
title: "Creating Files and Directories"
duration_minutes: 15
objectives:
  - "Create empty files and update timestamps with touch"
  - "Create directories with mkdir and nested directories with mkdir -p"
  - "Apply Linux file and directory naming conventions and best practices"
commands: [touch, mkdir, mkdir -p]
prerequisites: []
sandbox_commands: [touch, mkdir, ls, pwd]
sandbox_setup: |
  cd ~
---

# Creating Files and Directories

Now that you know how to navigate the filesystem (Week 1), it is time to start
building things. In this lesson you will learn how to create new files and
directories from the command line -- the fundamental building blocks of
organising your work on a Linux system like CachyOS.

## Creating Files with `touch`

The `touch` command is the simplest way to create a new, empty file. Its
original purpose is to update a file's access and modification timestamps, but
if the file does not exist, `touch` creates it.

### Basic usage

```bash
touch newfile.txt
```

This creates an empty file called `newfile.txt` in the current directory. You
can verify it exists with `ls`:

```bash
ls -l newfile.txt
```

### Creating multiple files at once

You can pass several names to `touch` in a single command:

```bash
touch notes.txt ideas.txt todo.txt
```

All three files are created instantly.

### Updating timestamps

If you run `touch` on a file that already exists, the file contents are left
alone -- only its modification timestamp is updated to the current time:

```bash
touch existing_file.txt   # timestamp is now "right now"
```

This is useful when you need a build system or backup tool to treat a file as
recently changed.

### Specifying a timestamp

You can set a specific timestamp with the `-t` flag:

```bash
touch -t 202601011200 scheduled.txt   # sets timestamp to 2026-01-01 12:00
```

The format is `YYYYMMDDhhmm`.

## Creating Directories with `mkdir`

Directories (folders) are created with the `mkdir` command.

### Basic usage

```bash
mkdir projects
```

This creates a single directory called `projects` in the current working
directory. Verify it:

```bash
ls -ld projects
```

The `-d` flag tells `ls` to show the directory entry itself rather than listing
its contents.

### Creating multiple directories

Just like `touch`, you can create several at once:

```bash
mkdir docs scripts configs
```

### The problem with nested paths

What if you want to create a deeply nested structure like
`projects/webapp/src`? If `projects/webapp` does not exist yet, plain `mkdir`
will fail:

```bash
mkdir projects/webapp/src
# mkdir: cannot create directory 'projects/webapp/src': No such file or directory
```

### Solving it with `mkdir -p`

The `-p` (parents) flag tells `mkdir` to create every missing directory in the
path:

```bash
mkdir -p projects/webapp/src
```

This creates `projects`, then `projects/webapp`, then `projects/webapp/src` --
all in one command. If any of those directories already exist, `mkdir -p`
silently skips them instead of throwing an error.

**Tip:** Always use `mkdir -p` when scripting. It is safe to run repeatedly and
avoids errors if part of the path already exists.

### Setting permissions at creation time

You can set the directory permissions immediately with `-m`:

```bash
mkdir -m 700 private_stuff
```

This creates the directory with `rwx------` permissions -- only the owner can
read, write, or enter it.

## File and Directory Naming Conventions

Linux gives you enormous freedom in naming files, but following conventions
will save you headaches.

### Rules enforced by the system

| Rule | Detail |
|------|--------|
| Maximum length | 255 characters per name component |
| Forbidden character | `/` (forward slash) -- it is the path separator |
| Case sensitive | `Report.txt` and `report.txt` are different files |

### Best-practice conventions

1. **Avoid spaces.** Use hyphens or underscores instead:
   ```
   my-project       # good
   my_project       # good
   my project       # works but annoying to type
   ```
   If you must use a space, quote the name or escape it:
   ```bash
   mkdir "my project"
   mkdir my\ project
   ```

2. **Avoid special characters.** Characters like `*`, `?`, `#`, `!`, `&`, `|`,
   `;`, and `$` have special meaning to the shell. Stick to letters, numbers,
   hyphens, underscores, and dots.

3. **Start with a letter or number.** Files starting with a dot (`.`) are
   hidden by default (shown only with `ls -a`). This is fine when intentional
   (e.g., `.bashrc`), but surprising if accidental.

4. **Use lowercase.** Most Linux projects and tools expect lowercase names.
   CachyOS (like all Arch-based systems) follows this convention throughout its
   package ecosystem.

5. **Use extensions for files.** While Linux does not require file extensions,
   they help you (and your tools) identify file types quickly: `.txt`, `.sh`,
   `.conf`, `.log`, etc.

### Hidden files and directories

Any name starting with `.` is hidden:

```bash
touch .secret_notes
mkdir .config
ls          # neither appears
ls -a       # both appear
```

This is how CachyOS stores user configuration -- look in `~/.config/` for
application settings.

## Combining `touch` and `mkdir`

A common real-world pattern is to scaffold a project structure:

```bash
mkdir -p myapp/{src,tests,docs}
touch myapp/src/main.py
touch myapp/tests/test_main.py
touch myapp/docs/README.md
```

The braces `{src,tests,docs}` are **brace expansion** -- the shell expands
them into three separate arguments. You will learn more about this in
Lesson 9.

After running the above, your tree looks like:

```
myapp/
  src/
    main.py
  tests/
    test_main.py
  docs/
    README.md
```

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| `mkdir a/b/c` without `-p` | Error if `a/b` missing | Use `mkdir -p a/b/c` |
| Filename with leading `-` | Commands interpret it as a flag | Use `touch -- -weirdname` or `touch ./-weirdname` |
| Forgetting quotes around spaces | Shell splits into multiple arguments | Quote the name: `touch "my file.txt"` |

## Try It Yourself

Practice these exercises in the sandbox:

1. Create an empty file called `hello.txt`:
   ```bash
   touch hello.txt
   ```

2. Verify it exists:
   ```bash
   ls -l hello.txt
   ```

3. Create three directories at once:
   ```bash
   mkdir alpha beta gamma
   ```

4. Create a nested directory path in one command:
   ```bash
   mkdir -p alpha/one/two/three
   ```

5. List the nested structure:
   ```bash
   ls -R alpha
   ```

6. Create a hidden file and confirm it is hidden:
   ```bash
   touch .hidden_note
   ls          # not visible
   ls -a       # visible
   ```

7. Build a small project scaffold:
   ```bash
   mkdir -p webapp/{css,js,images}
   touch webapp/index.html
   touch webapp/css/style.css
   touch webapp/js/app.js
   ls -R webapp
   ```

## Summary

| Command | Purpose |
|---------|---------|
| `touch file` | Create an empty file (or update its timestamp) |
| `touch a b c` | Create multiple files |
| `mkdir dir` | Create a directory |
| `mkdir -p a/b/c` | Create nested directories, including parents |
| `mkdir -m 700 dir` | Create a directory with specific permissions |

You now know how to create the basic building blocks of the Linux filesystem.
In the next lesson you will learn how to copy and move them around.
