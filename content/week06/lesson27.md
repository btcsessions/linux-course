---
id: 27
week: 6
title: "Pipes -- Connecting Commands"
duration_minutes: 15
objectives:
  - "Use the pipe operator | to chain commands together"
  - "Build multi-stage pipelines that process data step by step"
  - "Duplicate output streams with tee"
  - "Convert stdin to command arguments with xargs"
commands: ["|", tee, xargs]
prerequisites: []
sandbox_commands: [cat, echo, ls, grep, sort, wc, head, tail, uniq, tee, xargs, cut, tr, cd, pwd, touch, mkdir, cp, mv, find, sed, awk, whoami, date, clear, file, stat]
sandbox_setup: |
  for i in $(seq 1 50); do
    ip="192.168.1.$((RANDOM % 20 + 100))"
    code=$((RANDOM % 3))
    status="200"
    if [ $code -eq 1 ]; then status="404"; fi
    if [ $code -eq 2 ]; then status="500"; fi
    echo "$ip - - [15/Jan/2024:10:$(printf '%02d' $((i % 60))):00] \"GET /page$((i % 10)) HTTP/1.1\" $status $((RANDOM % 5000 + 100))" >> access.log
  done
  echo "apple" > words.txt
  echo "banana" >> words.txt
  echo "CHERRY" >> words.txt
  echo "date" >> words.txt
  echo "elderberry" >> words.txt
  echo "apple" >> words.txt
  echo "banana" >> words.txt
  mkdir output
  touch file1.txt file2.txt file3.txt file4.txt file5.txt
  echo "Practice pipes!" > README.txt
---
# Pipes -- Connecting Commands

The pipe operator `|` is one of the defining features of the Unix philosophy:
build small tools that do one thing well, then combine them. On CachyOS and
every other Linux system, pipes let you connect the stdout of one command
directly to the stdin of another, forming powerful data-processing chains
without temporary files.

## How Pipes Work

When you write:

```bash
command1 | command2
```

the shell creates a **pipe** -- a kernel buffer that connects the stdout of
`command1` to the stdin of `command2`. Both commands run at the same time; the
kernel handles the flow of data between them.

```
 command1  ──stdout──>  [pipe]  ──stdin──>  command2
```

### A Simple Example

```bash
ls -la ~/demo | head -5
```

This lists the files in `~/demo` and passes the output to `head`, which prints
only the first five lines. Without the pipe, you would need to save to a
temporary file first.

## Building Multi-Stage Pipelines

You can chain as many commands as you need:

```bash
cat ~/demo/access.log | grep "404" | wc -l
```

This pipeline:

1. `cat` reads the log file.
2. `grep "404"` keeps only lines containing 404 errors.
3. `wc -l` counts the remaining lines.

### Analyzing Text Data

Count unique words sorted by frequency:

```bash
cat ~/demo/words.txt | sort | uniq -c | sort -rn
```

Step by step:

| Stage          | What It Does                              |
|----------------|-------------------------------------------|
| `cat`          | Reads the word list                       |
| `sort`         | Sorts lines alphabetically (required for `uniq`) |
| `uniq -c`      | Collapses adjacent duplicates, counts them |
| `sort -rn`     | Sorts numerically in reverse (most frequent first) |

### Extracting Fields

Get the list of IP addresses that received a 404 error:

```bash
grep "404" ~/demo/access.log | cut -d' ' -f1 | sort -u
```

Here `cut -d' ' -f1` splits each line on spaces and takes the first field (the
IP address), and `sort -u` removes duplicates.

## Saving and Viewing with `tee`

Sometimes you want to see output on the terminal **and** save it to a file at
the same time. That is what `tee` does:

```bash
ls -la ~/demo | tee listing.txt
```

The output appears on screen and is also written to `listing.txt`.

### Appending with `tee -a`

Just like `>>` for redirection, use `-a` to append:

```bash
echo "Run 1" | tee -a results.txt
echo "Run 2" | tee -a results.txt
cat results.txt
```

### `tee` in the Middle of a Pipeline

`tee` is especially useful for debugging or saving intermediate results:

```bash
cat ~/demo/access.log | grep "404" | tee 404_lines.txt | wc -l
```

This saves all 404 lines to a file **and** passes them along to `wc -l` for
counting.

## Converting Input to Arguments with `xargs`

Many commands expect their input as **arguments**, not on stdin. `xargs` bridges
that gap by reading stdin and converting each line (or word) into arguments for
another command.

### Basic Usage

```bash
echo "file1.txt file2.txt file3.txt" | xargs ls -la
```

This is equivalent to running `ls -la file1.txt file2.txt file3.txt`.

### Processing Files Found by Another Command

```bash
ls ~/demo/file*.txt | xargs wc -l
```

This counts lines in every matching file.

### Using `-I {}` for Placement Control

The `-I {}` flag lets you place each input item at a specific position:

```bash
echo -e "file1.txt\nfile2.txt\nfile3.txt" | xargs -I {} echo "Processing: {}"
```

### Handling Filenames with Spaces

If filenames contain spaces or special characters, use `-0` combined with a
null-delimited source:

```bash
find ~/demo -name "*.txt" -print0 | xargs -0 wc -l
```

The `-print0` flag in `find` and `-0` in `xargs` use the null character as a
delimiter, which is safe for any filename.

> **Warning:** Without `-0`, filenames containing spaces will be split
> incorrectly and can cause unexpected behavior or even data loss.

## Pipes vs. Redirection

| Feature       | Pipe `\|`                         | Redirect `>` / `<`              |
|---------------|-----------------------------------|---------------------------------|
| Connects      | Command to command                | Command to file (or file to command) |
| Runs          | Both sides simultaneously         | One command at a time           |
| Use case      | Chaining filters                  | Saving or loading data          |

You can combine them:

```bash
sort < ~/demo/words.txt | uniq -c | sort -rn > word_freq.txt
```

## Common Pipeline Patterns

### Count lines matching a pattern

```bash
grep "ERROR" /var/log/pacman.log 2>/dev/null | wc -l
```

### Find the largest files in a directory

```bash
ls -lS ~/demo | head -5
```

### Remove duplicate lines from a file

```bash
sort ~/demo/words.txt | uniq > ~/demo/unique_words.txt
```

### Get top IP addresses from a log

```bash
cut -d' ' -f1 ~/demo/access.log | sort | uniq -c | sort -rn | head -5
```

## Try It Yourself

1. **Count 404 errors in the log:**
   ```bash
   grep "404" ~/demo/access.log | wc -l
   ```

2. **Find the top 3 most frequent words:**
   ```bash
   cat ~/demo/words.txt | sort | uniq -c | sort -rn | head -3
   ```

3. **Save and display at the same time:**
   ```bash
   ls ~/demo | tee ~/demo/filelist.txt
   cat ~/demo/filelist.txt
   ```

4. **Use xargs to show file sizes:**
   ```bash
   ls ~/demo/file*.txt | xargs wc -l
   ```

5. **Build a three-stage pipeline:**
   ```bash
   cut -d' ' -f1 ~/demo/access.log | sort | uniq -c | sort -rn | head -5
   ```

## Summary

- The pipe `|` connects stdout of one command to stdin of the next.
- Multi-stage pipelines let you process data step by step without temporary files.
- `tee` duplicates output to both a file and the next command in the pipeline.
- `xargs` converts stdin lines into command-line arguments for another command.
- Use `xargs -0` with `find -print0` for safe handling of special filenames.
- Pipes and redirection complement each other and can be used together.
