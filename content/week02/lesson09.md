---
id: 9
week: 2
title: "Wildcards and Globbing"
duration_minutes: 15
objectives:
  - "Use *, ?, and [...] glob patterns to match filenames"
  - "Apply brace expansion {a,b} to generate multiple arguments"
  - "Combine globs with commands like ls, cp, and mv"
commands: [ls, cp, mv]
prerequisites: []
sandbox_commands: [ls, cp, mv, touch, echo]
sandbox_setup: |
  mkdir -p ~/practice/reports
  touch ~/practice/file1.txt ~/practice/file2.txt ~/practice/file3.txt
  touch ~/practice/file1.log ~/practice/file2.log ~/practice/file3.log
  touch ~/practice/image.png ~/practice/photo.jpg ~/practice/icon.gif
  touch ~/practice/report_a.csv ~/practice/report_b.csv ~/practice/report_c.csv
  touch ~/practice/notes.md ~/practice/readme.md
  touch ~/practice/script.sh ~/practice/deploy.sh
  cd ~/practice
---

# Wildcards and Globbing

So far, every command you have typed has named files explicitly. But what if you
want to work with dozens of `.txt` files at once? Or copy everything that starts
with "report"? Typing each filename would be tedious and error-prone.

This is where **globbing** comes in -- using special wildcard characters to
match multiple filenames in a single pattern.

## What Is Globbing?

Globbing (also called filename expansion or pathname expansion) is a feature of
the **shell** -- not of individual commands. When you type a pattern like
`*.txt`, the shell expands it into a list of matching filenames **before** the
command even runs.

For example, when you type:

```bash
ls *.txt
```

The shell first expands `*.txt` into `file1.txt file2.txt file3.txt`, then runs:

```bash
ls file1.txt file2.txt file3.txt
```

The `ls` command never sees the `*` -- it only receives the expanded list of
filenames.

## The Star Wildcard: `*`

The `*` matches **zero or more characters** in a filename.

### Examples

```bash
ls *.txt
```
```
file1.txt  file2.txt  file3.txt
```

Matches any file ending with `.txt`.

```bash
ls file*
```
```
file1.log  file1.txt  file2.log  file2.txt  file3.log  file3.txt
```

Matches any file starting with `file`.

```bash
ls *.csv
```
```
report_a.csv  report_b.csv  report_c.csv
```

Matches any file ending with `.csv`.

```bash
ls *report*
```
```
report_a.csv  report_b.csv  report_c.csv
```

Matches any file containing "report" anywhere in the name.

### Using `*` with other commands

Globs work with **any** command, not just `ls`:

```bash
cp *.csv reports/        # copy all CSV files into reports/
mv *.log /tmp/           # move all log files to /tmp/
rm *.tmp                 # delete all .tmp files
```

## The Question Mark Wildcard: `?`

The `?` matches **exactly one character**.

### Examples

```bash
ls file?.txt
```
```
file1.txt  file2.txt  file3.txt
```

Matches `file` + any single character + `.txt`. This would **not** match
`file10.txt` (because `10` is two characters).

```bash
ls file?.log
```
```
file1.log  file2.log  file3.log
```

```bash
ls ????.sh
```

Matches any `.sh` file whose base name is exactly four characters (e.g.,
`deploy` would not match because it is six characters, but if you had `test.sh`
it would).

### Combining `*` and `?`

You can mix wildcards in the same pattern:

```bash
ls file?.*
```
```
file1.log  file1.txt  file2.log  file2.txt  file3.log  file3.txt
```

This matches `file` + one character + `.` + anything.

## Character Classes: `[...]`

Square brackets match **any one character** from a specified set.

### A set of characters

```bash
ls file[12].txt
```
```
file1.txt  file2.txt
```

Matches `file1.txt` or `file2.txt` but not `file3.txt`.

### A range of characters

```bash
ls file[1-3].txt
```
```
file1.txt  file2.txt  file3.txt
```

The dash inside brackets defines a range. Common ranges:

| Pattern | Matches |
|---------|---------|
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit |
| `[a-zA-Z]` | Any letter |
| `[aeiou]` | Any vowel |

### Negating a character class

Use `!` or `^` inside the brackets to match any character **except** those
listed:

```bash
ls file[!3].txt
```
```
file1.txt  file2.txt
```

Matches `file` + any character that is not `3` + `.txt`.

```bash
ls report_[!a].csv
```
```
report_b.csv  report_c.csv
```

### Real-world examples

```bash
ls *.[jp][pn][g]          # matches .jpg, .png (roughly)
ls [A-Z]*.txt             # files starting with an uppercase letter
ls *[0-9].log             # log files ending with a digit
```

## Brace Expansion: `{a,b,c}`

Brace expansion is different from globbing -- it generates strings regardless
of whether matching files exist. The shell expands braces **before** checking
the filesystem.

### Basic syntax

```bash
echo {apple,banana,cherry}
```
```
apple banana cherry
```

### Practical uses

**Create multiple files at once:**

```bash
touch report_{jan,feb,mar,apr}.csv
ls report_*.csv
```
```
report_apr.csv  report_feb.csv  report_jan.csv  report_mar.csv
```

**Create a directory structure:**

```bash
mkdir -p project/{src,tests,docs,config}
```

**Copy a file to a backup:**

```bash
cp config.conf{,.bak}
# expands to: cp config.conf config.conf.bak
```

This is a beloved trick among Linux users. The comma with nothing before it
means "empty string", so the expansion produces the original name and the name
with `.bak` appended.

### Numeric ranges

Braces also support numeric sequences:

```bash
touch file{1..5}.txt
ls file*.txt
```
```
file1.txt  file2.txt  file3.txt  file4.txt  file5.txt
```

You can specify a step:

```bash
echo {0..20..5}
```
```
0 5 10 15 20
```

And alphabetic sequences:

```bash
echo {a..f}
```
```
a b c d e f
```

## Glob vs Brace Expansion: Key Differences

| Feature | Glob (`*`, `?`, `[]`) | Brace expansion (`{}`) |
|---------|----------------------|----------------------|
| Matches existing files | Yes | No -- generates strings |
| Expansion depends on filesystem | Yes | No |
| No match behavior | Pattern stays literal (or error in some shells) | Always expands |
| Processed by | Shell, after brace expansion | Shell, before globbing |

Because brace expansion happens first, you can combine them:

```bash
ls {file,report}*.txt
# expands braces first: ls file*.txt report*.txt
# then globs expand against the filesystem
```

## What Happens When Nothing Matches?

The behavior depends on your shell:

**In bash:** If a glob pattern matches nothing, it is passed to the command as
a literal string:

```bash
ls *.xyz
# ls: cannot access '*.xyz': No such file or directory
```

**In fish (CachyOS default):** An error is raised if no files match:

```bash
ls *.xyz
# fish: No matches for wildcard '*.xyz'.
```

**In zsh:** Similar to fish -- an error by default.

**Tip:** In bash, you can enable the `failglob` option to get an error when
nothing matches, or `nullglob` to have the pattern expand to nothing:

```bash
shopt -s nullglob      # unmatched globs expand to empty
shopt -s failglob      # unmatched globs produce an error
```

## Hidden Files and Globs

By default, `*` does **not** match hidden files (those starting with `.`):

```bash
touch .hidden_file
ls *                    # .hidden_file does NOT appear
ls .*                   # matches hidden files
ls -a                   # shows everything
```

If you need to match both hidden and non-hidden files, you must be explicit:

```bash
ls .* *                 # hidden and non-hidden
```

**Warning:** Be careful with `.*` -- it matches `.` (current directory) and
`..` (parent directory). A command like `rm -r .*` could do serious damage.

## Common Patterns in Practice

| Task | Command |
|------|---------|
| List all Python files | `ls *.py` |
| Copy all images | `cp *.{jpg,png,gif} images/` |
| Remove all log files | `rm *.log` |
| Move numbered files | `mv file[0-9].txt archive/` |
| Create month directories | `mkdir {01..12}_month` |
| Backup a config file | `cp config.conf{,.bak}` |

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Quoting a glob: `ls "*.txt"` | Shell does not expand it | Remove quotes: `ls *.txt` |
| Using globs in `mkdir` | Matches existing files, not intended names | Use brace expansion instead |
| `rm -rf *` in wrong directory | Deletes everything | Check `pwd` first |
| Forgetting `.*` excludes hidden | Hidden files silently skipped | Add `.*` if needed |

## CachyOS-Specific Notes

If you are using the fish shell on CachyOS, note that fish handles glob
expansion slightly differently from bash:

- Fish raises an error when a glob matches nothing (instead of passing the
  literal pattern).
- Fish uses `**` for recursive globbing by default (e.g., `ls **/*.txt` finds
  `.txt` files in all subdirectories).
- Brace expansion in fish works the same way as in bash.

In bash, you need to enable `globstar` (`shopt -s globstar`) to use `**` for
recursive matching.

## Try It Yourself

1. List all `.txt` files:
   ```bash
   ls *.txt
   ```

2. List all files starting with "file":
   ```bash
   ls file*
   ```

3. List only `.txt` files with a single-digit number:
   ```bash
   ls file?.txt
   ```

4. List CSV files for reports a and b only:
   ```bash
   ls report_[ab].csv
   ```

5. List all files that are NOT `.log` files:
   ```bash
   ls *.[!l]*
   ```
   (This is imperfect -- can you think of why?)

6. Use brace expansion to create files:
   ```bash
   touch test_{alpha,beta,gamma}.txt
   ls test_*.txt
   ```

7. Use a numeric range:
   ```bash
   touch chapter{1..5}.md
   ls chapter*.md
   ```

8. Copy all CSV files to the reports directory:
   ```bash
   cp *.csv reports/
   ls reports/
   ```

9. Combine brace expansion and a command:
   ```bash
   touch config.conf
   cp config.conf{,.backup}
   ls config*
   ```

## Summary

| Pattern | Matches |
|---------|---------|
| `*` | Zero or more characters |
| `?` | Exactly one character |
| `[abc]` | One character: a, b, or c |
| `[a-z]` | One character in the range a through z |
| `[!abc]` | One character that is NOT a, b, or c |
| `{a,b,c}` | Generates strings a, b, and c (brace expansion) |
| `{1..5}` | Generates 1 2 3 4 5 (sequence expansion) |

Wildcards and globbing are one of the shell's most powerful time-savers. Master
them and you will rarely need to type individual filenames again. In the next
lesson, you will learn to find files anywhere on the system with `find` and
`locate`.
