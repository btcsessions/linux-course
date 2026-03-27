---
id: 26
week: 6
title: "Standard Streams and Redirection"
duration_minutes: 15
objectives:
  - "Understand the three standard streams: stdin, stdout, and stderr"
  - "Redirect output to files using > and >>"
  - "Redirect input from files using <"
  - "Redirect stderr with 2> and combine streams with 2>&1"
commands: [">", ">>", "<", "2>", "2>&1", "&>", /dev/null]
prerequisites: []
sandbox_commands: [cat, echo, ls, grep, sort, wc]
sandbox_setup: |
  #!/bin/bash
  mkdir -p ~/demo
  echo -e "apple\nbanana\ncherry\ndate\nelderberry" > ~/demo/fruits.txt
  echo -e "Charlie\nAlice\nBob\nDiana" > ~/demo/names.txt
  mkdir -p ~/demo/subdir
  echo "secret data" > ~/demo/subdir/hidden.txt
  # Create a file that will produce errors when accessed
  chmod 000 ~/demo/subdir/hidden.txt
---
# Standard Streams and Redirection

Every program you run on a Linux system communicates through three default
channels called **standard streams**. Understanding these streams and learning
to redirect them is one of the most powerful skills you can develop on the
command line. This lesson walks you through the concepts and gives you hands-on
practice on CachyOS.

## The Three Standard Streams

When a process starts, the kernel opens three file descriptors for it
automatically:

| Stream          | File Descriptor | Default Destination | Purpose                     |
|-----------------|:--------------:|---------------------|-----------------------------|
| **stdin**       | 0              | Keyboard            | Input to the program        |
| **stdout**      | 1              | Terminal screen      | Normal output               |
| **stderr**      | 2              | Terminal screen      | Error messages and warnings |

Both stdout and stderr appear on your terminal by default, so they can look
the same. The distinction matters when you start redirecting them to different
places.

```
           ┌──────────────┐
 stdin ──> │              │ ──> stdout
  (0)      │   command    │
           │              │ ──> stderr
           └──────────────┘       (2)
                 (1)
```

## Redirecting stdout with `>` and `>>`

### Overwrite with `>`

The `>` operator sends stdout to a file, **replacing** any existing content:

```bash
echo "Hello, CachyOS!" > greeting.txt
cat greeting.txt
```

Running the same command again will overwrite the file completely.

### Append with `>>`

The `>>` operator **appends** to the file instead of overwriting:

```bash
echo "First line" > notes.txt
echo "Second line" >> notes.txt
cat notes.txt
```

> **Warning:** Be careful with `>`. If you accidentally redirect to an
> important file, its previous contents are lost instantly. There is no undo.

### Redirecting Command Output

Any command's output can be captured this way:

```bash
ls -la ~/demo > listing.txt
sort ~/demo/names.txt > sorted_names.txt
cat sorted_names.txt
```

## Redirecting stdin with `<`

The `<` operator feeds a file into a command's stdin instead of typing input
from the keyboard:

```bash
sort < ~/demo/names.txt
```

This is equivalent to `sort ~/demo/names.txt` for many commands, but some
programs behave differently depending on whether they receive a filename
argument or data on stdin. The `<` operator is also useful in scripts.

You can combine input and output redirection in one command:

```bash
sort < ~/demo/names.txt > ~/demo/sorted.txt
cat ~/demo/sorted.txt
```

## Redirecting stderr with `2>`

Because stderr has file descriptor **2**, you redirect it with `2>`:

```bash
ls ~/demo/nonexistent 2> errors.txt
cat errors.txt
```

The error message goes to `errors.txt` instead of cluttering your terminal.

### Separate stdout and stderr

You can redirect each stream to a different file:

```bash
ls ~/demo ~/demo/nonexistent > output.txt 2> errors.txt
cat output.txt
cat errors.txt
```

The successful listing goes to `output.txt` while the error about the missing
path goes to `errors.txt`.

## Combining Streams with `2>&1` and `&>`

### `2>&1` -- redirect stderr to where stdout is going

This is the classic syntax. The order matters -- set the stdout destination
first, then merge stderr into it:

```bash
ls ~/demo ~/demo/nonexistent > all_output.txt 2>&1
cat all_output.txt
```

If you reverse the order (`2>&1 > file`), stderr still goes to the terminal
because the merge happens before the redirect.

### `&>` -- shorthand for both streams

Bash (and most shells on CachyOS) provides a convenient shortcut:

```bash
ls ~/demo ~/demo/nonexistent &> combined.txt
cat combined.txt
```

This is exactly equivalent to `> combined.txt 2>&1`.

> **CachyOS note:** Whether your default shell is bash or fish, both support
> some form of combined redirection. In fish the syntax is slightly different:
> `command &> file` also works in modern fish versions.

## Discarding Output with `/dev/null`

`/dev/null` is a special file that silently swallows anything written to it.
It is sometimes called the **bit bucket**.

```bash
# Suppress error messages
ls ~/demo/nonexistent 2> /dev/null

# Suppress all output
ls ~/demo &> /dev/null

# Keep errors, discard normal output
ls ~/demo ~/demo/nonexistent > /dev/null
```

This is extremely useful in scripts where you only care about exit codes, not
output.

## Here Documents and Here Strings

A **here document** feeds multiple lines into stdin using `<<`:

```bash
cat << EOF
Line one
Line two
Line three
EOF
```

A **here string** feeds a single string using `<<<`:

```bash
grep "an" <<< "banana"
```

> **Tip:** Here documents are commonly used in shell scripts to embed
> multi-line text or configuration blocks.

## Practical Examples

### Save a command log

```bash
echo "=== Disk usage ===" > report.txt
df -h >> report.txt
echo "" >> report.txt
echo "=== Memory ===" >> report.txt
free -h >> report.txt
```

### Run a command silently

```bash
pacman -Qi base &> /dev/null && echo "Package found" || echo "Not found"
```

### Separate good data from errors

```bash
find /etc -name "*.conf" > configs.txt 2> find_errors.txt
```

## Try It Yourself

1. **Create a file with redirection:**
   ```bash
   echo "Hello from the shell" > ~/demo/hello.txt
   cat ~/demo/hello.txt
   ```

2. **Append more lines:**
   ```bash
   echo "Another line" >> ~/demo/hello.txt
   cat ~/demo/hello.txt
   ```

3. **Redirect sorted output:**
   ```bash
   sort < ~/demo/fruits.txt > ~/demo/sorted_fruits.txt
   cat ~/demo/sorted_fruits.txt
   ```

4. **Capture errors separately:**
   ```bash
   ls ~/demo ~/nonexistent > ~/demo/out.txt 2> ~/demo/err.txt
   cat ~/demo/out.txt
   cat ~/demo/err.txt
   ```

5. **Discard errors:**
   ```bash
   ls ~/nonexistent 2> /dev/null
   echo "Exit code was: $?"
   ```

## Summary

- Every process has three streams: **stdin** (0), **stdout** (1), **stderr** (2).
- `>` overwrites a file with stdout; `>>` appends to it.
- `<` feeds a file into stdin.
- `2>` redirects stderr; `2>&1` merges stderr into stdout.
- `&>` is shorthand for redirecting both stdout and stderr.
- `/dev/null` silently discards anything sent to it.
- Here documents (`<<`) and here strings (`<<<`) supply inline input.
