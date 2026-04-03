---
id: 8
week: 2
title: "Removing Files and Directories"
duration_minutes: 15
objectives:
  - "Remove files with rm and understand its options"
  - "Recognize the dangers of rm -rf and use it responsibly"
  - "Remove empty directories with rmdir"
commands: [rm, rm -i, rm -r, rm -rf, rmdir]
prerequisites: []
sandbox_commands: [rm, rmdir, ls, cd, pwd, cat, echo, touch, mkdir, cp, mv, whoami, date, clear]
sandbox_setup: |
  mkdir -p trash_me/subdir empty_dir keep_this
  echo "Delete me" > trash_me/file1.txt
  echo "Delete me too" > trash_me/file2.txt
  echo "Nested file" > trash_me/subdir/nested.txt
  echo "Temp file 1" > temp1.txt
  echo "Temp file 2" > temp2.txt
  echo "Temp file 3" > temp3.txt
  echo "Important - don't delete!" > keep_this/important.txt
  echo "Practice safe deletion here" > README.txt
---

# Removing Files and Directories

Deleting files is a necessary part of keeping your system organised. But on
Linux, deletion is **permanent** -- there is no Recycle Bin or Trash when you
remove something from the command line. This lesson teaches you how to delete
safely and how to avoid catastrophic mistakes.

## The Golden Rule

**Warning:** On the Linux command line, deleted files are gone forever. There
is no undo, no Recycle Bin, no "Are you sure?" dialog by default. Always
double-check your command before pressing Enter.

Some desktop environments on CachyOS (like KDE Plasma) do provide a Trash for
files deleted through the file manager, but the `rm` command bypasses all of
that entirely.

## Removing Files with `rm`

The `rm` (remove) command deletes files.

### Basic usage

```bash
rm junk1.txt
```

The file is gone. No output, no confirmation -- just gone.

Verify with `ls`:

```bash
ls junk1.txt
# ls: cannot access 'junk1.txt': No such file or directory
```

### Removing multiple files

Pass several filenames at once:

```bash
rm junk2.txt junk3.log tempfile.txt
```

All three are deleted in one command.

### Interactive mode with `-i`

The `-i` flag asks for confirmation before each deletion:

```bash
rm -i junk1.txt
# rm: remove regular file 'junk1.txt'? y
```

Type `y` and press Enter to confirm, or `n` to skip.

**Tip:** Many experienced Linux users add this alias to their `~/.bashrc`:

```bash
alias rm='rm -i'
```

This way `rm` always asks before deleting. On CachyOS, if you use fish shell,
the equivalent would go in `~/.config/fish/config.fish`:

```fish
alias rm 'rm -i'
```

### Verbose mode with `-v`

See exactly what is being deleted:

```bash
rm -v junk1.txt junk2.txt
# removed 'junk1.txt'
# removed 'junk2.txt'
```

### Force mode with `-f`

The `-f` (force) flag suppresses all prompts and ignores nonexistent files:

```bash
rm -f nonexistent_file.txt    # no error, no output
```

Without `-f`, trying to remove a nonexistent file produces an error. The `-f`
flag is useful in scripts where you want to ensure a clean slate without
worrying about whether files exist.

## Removing Directories

### The problem: `rm` alone refuses directories

```bash
rm old_project/
# rm: cannot remove 'old_project/': Is a directory
```

Plain `rm` only works on files. For directories, you have two options.

### Option 1: `rmdir` for empty directories

The `rmdir` command removes directories, but **only** if they are empty:

```bash
rmdir empty_dir
```

If the directory contains anything -- even a hidden file -- `rmdir` refuses:

```bash
rmdir old_project/
# rmdir: failed to remove 'old_project/': Directory not empty
```

This makes `rmdir` a safe choice. It will never accidentally delete your data.

**Tip:** You can remove a chain of empty directories with `rmdir -p`:

```bash
mkdir -p a/b/c
rmdir -p a/b/c     # removes c, then b, then a (all must be empty)
```

### Option 2: `rm -r` for directories with contents

The `-r` (recursive) flag tells `rm` to descend into a directory and delete
everything inside it, then delete the directory itself:

```bash
rm -r old_project/
```

This removes `old_project/`, `old_project/src/`, `old_project/docs/`, and
every file within them.

You can combine with `-i` for safety:

```bash
rm -ri old_project/
```

This prompts you for every single file and directory inside the tree. It can
be tedious for large directories, but it is the safest recursive delete.

### Combining flags: `rm -rv`

Get verbose output while removing recursively:

```bash
rm -rv old_project/
# removed 'old_project/src/main.py'
# removed 'old_project/src/'
# removed 'old_project/docs/notes.txt'
# removed 'old_project/docs/'
# removed 'old_project/'
```

## The Danger of `rm -rf`

The combination `rm -rf` means: delete recursively, forcefully, without asking
any questions.

```bash
rm -rf old_project/
```

This is the most powerful and **most dangerous** command you will learn.

### Why it is dangerous

1. **No confirmation.** Every file is deleted silently.
2. **No recovery.** Deleted files cannot be retrieved.
3. **It follows your instructions exactly.** A typo can be catastrophic.

### Horror stories and how to avoid them

Consider the difference between these two commands:

```bash
rm -rf /home/alex/old_project    # deletes old_project -- intended
rm -rf /home/alex /old_project   # deletes your ENTIRE home directory + /old_project
```

That accidental space just wiped out everything in `/home/alex`.

Even worse:

```bash
rm -rf /     # attempts to delete EVERYTHING on the system
```

Modern versions of `rm` include a safety check (`--preserve-root`) that
prevents `rm -rf /` from working. But `rm -rf /*` would still be devastating.

**Warning:** Never run `rm -rf` with variables that might be empty:

```bash
# DANGEROUS -- if $DIR is empty, this becomes 'rm -rf /'
rm -rf $DIR/
```

### Safe practices

| Practice | Why |
|----------|-----|
| Use `rm -ri` instead of `rm -rf` when possible | Prompts before each deletion |
| Always `ls` first to see what will be deleted | `ls old_project/` before `rm -r old_project/` |
| Use full paths and double-check them | Avoids deleting the wrong thing |
| Avoid using `rm -rf` with shell variables | A blank variable can expand to `/` |
| Consider `trash-cli` as a safer alternative | Moves to trash instead of deleting |

### The `trash-cli` alternative

On CachyOS you can install `trash-cli` from the Arch repositories:

```bash
sudo pacman -S trash-cli
```

Then use `trash-put` instead of `rm`:

```bash
trash-put old_file.txt       # moves to trash
trash-list                   # shows trashed files
trash-restore                # restore from trash
```

This gives you a safety net similar to the desktop Recycle Bin.

## Practical Patterns

### Clean up temporary files

```bash
rm -v *.tmp *.log
```

### Remove an old project

```bash
# Step 1: verify what you are about to delete
ls -R old_project/

# Step 2: delete it
rm -rv old_project/
```

### Remove empty directories left behind

After deleting files, you may have empty directories to clean up:

```bash
rmdir leftover_dir/
```

### Remove a file whose name starts with a dash

```bash
rm -- -weirdfile.txt
# or
rm ./-weirdfile.txt
```

The `--` tells `rm` that everything after it is a filename, not an option.

## Common Mistakes

| Mistake | Consequence | Prevention |
|---------|------------|------------|
| `rm -rf /` or `rm -rf /*` | Destroys the entire system | Triple-check paths; never use bare `/` |
| Space before path: `rm -rf / home/alex` | Deletes root directory | Proofread carefully |
| Forgetting `-r` for directories | Error message (harmless) | Remember: dirs need `-r` |
| Using `rm` when you meant `mv` | File deleted instead of moved | Slow down and read your command |
| Empty variable in `rm -rf $VAR/` | Could delete `/` | Always quote: `rm -rf "$VAR/"` and validate |

## CachyOS-Specific Notes

CachyOS ships with GNU coreutils, which includes the `--preserve-root` safety
feature enabled by default. This prevents `rm -rf /` from executing. However,
this does **not** protect against `rm -rf /*` or mistyped paths.

If you are using the fish shell (common on CachyOS), it does not expand `$VAR`
the same way bash does, which provides slightly more safety against the
empty-variable problem. But you should still be careful.

## Try It Yourself

Practice in the sandbox (all files here are disposable):

1. List what is available:
   ```bash
   ls -R
   ```

2. Remove a single file:
   ```bash
   rm junk1.txt
   ls
   ```

3. Remove with confirmation:
   ```bash
   rm -i junk2.txt
   ```

4. Try `rmdir` on a non-empty directory:
   ```bash
   rmdir old_project/
   ```
   (It should fail -- why?)

5. Remove an empty directory:
   ```bash
   rmdir empty_dir/
   ls
   ```

6. Remove a directory tree verbosely:
   ```bash
   rm -rv old_project/
   ```

7. Try removing a file that does not exist:
   ```bash
   rm nonexistent.txt       # error
   rm -f nonexistent.txt    # no error
   ```

8. Practice the "ls first" habit:
   ```bash
   touch a.tmp b.tmp c.tmp
   ls *.tmp                 # verify
   rm -v *.tmp              # then delete
   ```

## Summary

| Command | Purpose |
|---------|---------|
| `rm file` | Remove a file (permanent, no confirmation) |
| `rm -i file` | Remove with confirmation prompt |
| `rm -v file` | Remove with verbose output |
| `rm -f file` | Remove without errors for missing files |
| `rm -r dir/` | Remove a directory and all its contents |
| `rm -rf dir/` | Remove recursively and forcefully (use with extreme care) |
| `rmdir dir/` | Remove an empty directory only |
| `rmdir -p a/b/c` | Remove a chain of empty nested directories |

Deletion is the one operation where caution truly matters. Build the habit of
checking with `ls` before running `rm`, and consider using `rm -i` as your
default. In the next lesson, you will learn about wildcards and globbing --
powerful patterns that make commands like `rm *.log` possible.
