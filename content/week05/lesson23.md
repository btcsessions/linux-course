---
id: 23
week: 5
title: "sed -- Stream Editing Basics"
duration_minutes: 15
objectives:
  - "Perform search-and-replace with sed s/old/new/ and s/old/new/g"
  - "Delete lines matching a pattern with /pattern/d"
  - "Edit files in place using sed -i"
  - "Print specific line ranges with sed -n"
commands: ["sed 's/foo/bar/'", "sed 's/foo/bar/g'", "sed -i", "sed '/^#/d'", "sed -n '5,10p'"]
prerequisites: []
sandbox_commands: [sed, grep, cat, ls, cd, pwd, echo, touch, mkdir, cp, head, tail, less, find, wc, sort, uniq, cut, whoami, date, clear, file]
sandbox_setup: |
  echo "# Application Config" > config.conf
  echo "hostname=old-server" >> config.conf
  echo "port=8080" >> config.conf
  echo "# Debug mode" >> config.conf
  echo "debug=true" >> config.conf
  echo "log_level=info" >> config.conf
  echo "database_host=localhost" >> config.conf
  echo "" >> config.conf
  echo "# Cache settings" >> config.conf
  echo "cache_enabled=true" >> config.conf
  echo "cache_ttl=3600" >> config.conf
  for i in $(seq 1 20); do echo "Line $i: some content here" >> lines.txt; done
  echo "Hello World" > greeting.txt
  echo "hello world" >> greeting.txt
  echo "HELLO WORLD" >> greeting.txt
  echo "Hello World Hello World" >> greeting.txt
  echo "Practice sed!" > README.txt
---

# sed -- Stream Editing Basics

## What Is sed?

`sed` stands for **Stream Editor**. While `grep` finds lines that match a
pattern, `sed` goes further -- it can *transform* text as it flows through.
Think of `sed` as a text-processing assembly line: text goes in one end, `sed`
applies your instructions, and the modified text comes out the other end.

`sed` is one of the classic Unix text tools, and it is indispensable for tasks
like:

- Replacing text across files (rename a variable, fix a typo)
- Removing comment lines or blank lines
- Extracting specific line ranges from a file
- Automating edits that would be tedious to do by hand

## Basic Substitution: s/old/new/

The most common `sed` command is substitution. The syntax is:

```bash
sed 's/old/new/' filename
```

This replaces the **first occurrence** of "old" with "new" on each line:

```bash
sed 's/localhost/0.0.0.0/' /tmp/sed-practice/config.conf
```

Output (only showing the changed line):

```
hostname = 0.0.0.0
```

The rest of the file passes through unchanged. By default, `sed` writes its
output to the terminal -- it does **not** modify the original file.

**Tip:** The `s` stands for "substitute." The slashes `/` are delimiters. You
can actually use any character as a delimiter, which is handy when your pattern
contains slashes:

```bash
sed 's|/home/alice|/home/bob|' file.txt
```

## Global Substitution: s/old/new/g

Without the `g` flag, `sed` only replaces the **first** match on each line. Add
`g` to replace **all** occurrences:

```bash
echo "apple banana apple banana" | sed 's/apple/orange/'
```

```
orange banana apple banana
```

Only the first "apple" was replaced. Now with `g`:

```bash
echo "apple banana apple banana" | sed 's/apple/orange/g'
```

```
orange banana orange banana
```

Both occurrences are replaced.

For the messy spaces file, let's replace multiple spaces with a single space:

```bash
sed 's/  */ /g' /tmp/sed-practice/messy.txt
```

```
Hello World
This is a test
Too many spaces here
Normal line
Another messy line
```

The pattern `  *` means "a space followed by zero or more spaces" (effectively
"one or more spaces"), and we replace it with a single space.

## Deleting Lines: d

The `d` command deletes lines that match a pattern:

```bash
sed '/^#/d' /tmp/sed-practice/config.conf
```

This removes all comment lines (lines starting with `#`):

```
hostname = localhost
port = 8080
log_level = INFO
max_connections = 100
database_host = db-server-01
database_port = 5432
database_name = production_db
timeout = 30
retry_count = 3
```

The blank line from the original file remains. To also remove blank lines:

```bash
sed '/^#/d; /^$/d' /tmp/sed-practice/config.conf
```

The semicolon separates two `sed` commands: delete comment lines, then delete
empty lines.

## Printing Specific Lines: -n and p

By default, `sed` prints every line. The `-n` flag suppresses this automatic
output, and the `p` command explicitly prints matching lines:

```bash
sed -n '5,10p' /tmp/sed-practice/config.conf
```

This prints only lines 5 through 10:

```
# debug = true
log_level = INFO
max_connections = 100
database_host = db-server-01
database_port = 5432
database_name = production_db
```

You can also use patterns instead of line numbers:

```bash
sed -n '/database/p' /tmp/sed-practice/config.conf
```

```
database_host = db-server-01
database_port = 5432
database_name = production_db
```

This works like `grep "database" config.conf` -- but it shows that `sed` can
do everything `grep` does, plus much more.

## In-Place Editing: -i

So far, `sed` has only printed modified text to the terminal. To actually change
a file, use the `-i` flag:

```bash
sed -i 's/INFO/DEBUG/' /tmp/sed-practice/config.conf
```

This modifies `config.conf` directly. The file is changed on disk.

**Warning:** In-place editing is permanent. There is no undo. Always make a
backup first, or use `-i.bak` to create one automatically:

```bash
sed -i.bak 's/DEBUG/INFO/' /tmp/sed-practice/config.conf
```

This changes the file AND creates `config.conf.bak` with the original content.

**Tip:** On macOS, `sed -i` requires an argument (even an empty string:
`sed -i '' ...`). On CachyOS and other Linux systems with GNU sed, `-i` works
without an argument. If you write scripts that should be portable, use
`sed -i.bak` which works everywhere.

## Using Regular Expressions in sed

`sed` uses the same regular expressions you learned with `grep`. By default it
uses Basic Regular Expressions. For extended regex, use `sed -E`:

```bash
# Replace any sequence of digits with "XXX"
sed -E 's/[0-9]+/XXX/g' /tmp/sed-practice/config.conf
```

### Practical Examples

Remove trailing whitespace from every line:

```bash
sed 's/[[:space:]]*$//' /tmp/sed-practice/messy.txt
```

Add a prefix to every line:

```bash
sed 's/^/>> /' /tmp/sed-practice/names.csv
```

```
>> first_name,last_name,department
>> Alice,Johnson,Engineering
>> Bob,Smith,Marketing
...
```

Change the CSV delimiter from comma to tab:

```bash
sed 's/,/\t/g' /tmp/sed-practice/names.csv
```

## Multiple sed Commands

You can chain multiple operations with `-e` or semicolons:

```bash
# Using -e
sed -e 's/localhost/0.0.0.0/' -e 's/8080/9090/' /tmp/sed-practice/config.conf

# Using semicolons
sed 's/localhost/0.0.0.0/; s/8080/9090/' /tmp/sed-practice/config.conf
```

Both approaches are equivalent. Use `-e` for clarity when commands are complex.

## Address Ranges

You can limit which lines `sed` operates on by specifying addresses:

```bash
# Only substitute on line 4
sed '4s/localhost/0.0.0.0/' /tmp/sed-practice/config.conf

# Substitute on lines 8 through 11
sed '8,11s/database/db/' /tmp/sed-practice/config.conf

# Substitute only on lines matching a pattern
sed '/database/s/production/staging/' /tmp/sed-practice/config.conf
```

The last example is powerful: "On lines containing 'database', replace
'production' with 'staging'."

## Common sed Patterns

Here is a quick reference of `sed` one-liners you will use often:

```bash
# Delete blank lines
sed '/^$/d' file.txt

# Delete comment lines
sed '/^#/d' file.txt

# Print first 20 lines (like head -20)
sed -n '1,20p' file.txt

# Print last line
sed -n '$p' file.txt

# Insert text before line 3
sed '3i\New line of text' file.txt

# Append text after line 5
sed '5a\Appended text' file.txt

# Replace whole lines matching a pattern
sed '/^port/c\port = 9090' file.txt
```

## CachyOS-Specific Notes

CachyOS includes GNU `sed` by default as part of the core system. GNU sed is
the most feature-rich implementation and supports all the commands shown here.

A practical CachyOS example -- temporarily enable a repository in pacman.conf:

```bash
sudo sed -i 's/^#\[multilib\]/[multilib]/' /etc/pacman.conf
```

Or view your pacman.conf without comments or blank lines:

```bash
sed '/^#/d; /^$/d' /etc/pacman.conf
```

## Try It Yourself

Work through these exercises using the sandbox files:

1. Replace "localhost" with "0.0.0.0" in config.conf (print to terminal):
   ```bash
   sed 's/localhost/0.0.0.0/' /tmp/sed-practice/config.conf
   ```

2. Remove all comment lines from config.conf:
   ```bash
   sed '/^#/d' /tmp/sed-practice/config.conf
   ```

3. Print only lines 1 through 5 of names.csv:
   ```bash
   sed -n '1,5p' /tmp/sed-practice/names.csv
   ```

4. Replace commas with pipes in names.csv:
   ```bash
   sed 's/,/|/g' /tmp/sed-practice/names.csv
   ```

5. Clean up the messy.txt file by collapsing multiple spaces:
   ```bash
   sed 's/  */ /g' /tmp/sed-practice/messy.txt
   ```

6. Delete blank lines AND comment lines in one command:
   ```bash
   sed '/^#/d; /^$/d' /tmp/sed-practice/config.conf
   ```

7. Replace "Engineering" with "Eng" only on lines 2 through 4 of names.csv:
   ```bash
   sed '2,4s/Engineering/Eng/' /tmp/sed-practice/names.csv
   ```

8. Use `-i.bak` to make an in-place change and verify the backup was created:
   ```bash
   sed -i.bak 's/8080/9090/' /tmp/sed-practice/config.conf
   cat /tmp/sed-practice/config.conf.bak
   ```

In the next lesson, you will learn advanced `sed` techniques and get introduced
to `awk`, another powerful text-processing tool.
