---
id: 24
week: 5
title: "Advanced sed and awk Introduction"
duration_minutes: 15
objectives:
  - "Use sed with line-number and pattern-based addresses"
  - "Introduce awk for column-based text processing"
  - "Extract specific fields with awk '{print $1, $3}'"
  - "Use awk with custom field separators via -F"
commands: ["sed '3,5s/a/b/'", "awk '{print $1}'", "awk -F: '{print $1}'", "awk '/pattern/ {print}'"]
prerequisites: []
sandbox_commands: [sed, awk, cat]
sandbox_setup: |
  mkdir -p /tmp/awk-practice
  cat > /tmp/awk-practice/passwd-sample <<'PWEOF'
  root:x:0:0:root:/root:/bin/bash
  daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
  bin:x:2:2:bin:/bin:/usr/sbin/nologin
  sys:x:3:3:sys:/dev:/usr/sbin/nologin
  nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
  alex:x:1000:1000:Alex Thompson:/home/alex:/bin/bash
  maria:x:1001:1001:Maria Garcia:/home/maria:/bin/zsh
  jake:x:1002:1002:Jake Wilson:/home/jake:/bin/fish
  sara:x:1003:1003:Sara Chen:/home/sara:/bin/bash
  PWEOF
  cat > /tmp/awk-practice/scores.txt <<'SCEOF'
  Alice Math 95
  Bob Math 82
  Charlie Math 78
  Alice Science 88
  Bob Science 91
  Charlie Science 85
  Alice English 92
  Bob English 76
  Charlie English 89
  SCEOF
  cat > /tmp/awk-practice/employees.txt <<'EMPEOF'
  ID    Name          Department    Salary
  101   Alice         Engineering   85000
  102   Bob           Marketing     72000
  103   Charlie       Engineering   91000
  104   Diana         Sales         68000
  105   Eve           Marketing     75000
  106   Frank         Engineering   88000
  107   Grace         Sales         71000
  108   Hank          Engineering   95000
  EMPEOF
  cat > /tmp/awk-practice/access.log <<'AEOF'
  192.168.1.10 GET /index.html 200 1024
  192.168.1.25 POST /api/login 200 512
  10.0.0.5 GET /about.html 200 2048
  192.168.1.10 GET /style.css 200 4096
  192.168.1.25 GET /dashboard 403 128
  10.0.0.5 GET /contact.html 404 0
  192.168.1.10 POST /api/data 500 0
  10.0.0.5 GET /index.html 200 1024
  192.168.1.25 GET /profile 200 2048
  AEOF
---

# Advanced sed and awk Introduction

## sed with Addresses

In the previous lesson you learned basic `sed` substitution and deletion. Now
let's explore how to target specific lines with precision using **addresses**.

### Line Number Addresses

You can tell `sed` to operate on specific line numbers:

```bash
# Change only line 4
sed '4s/localhost/0.0.0.0/' /tmp/sed-practice/config.conf

# Change lines 8 through 11
sed '8,11s/database/db/g' /tmp/sed-practice/config.conf
```

### Pattern Addresses

Instead of line numbers, use a pattern to match lines:

```bash
# On lines containing "port", replace the value
sed '/port/s/[0-9]*/9090/' /tmp/sed-practice/config.conf
```

### Address Ranges with Patterns

You can combine patterns to define a range:

```bash
# From the line matching "database" to the line matching "timeout"
sed '/database/,/timeout/s/^/# /' /tmp/sed-practice/config.conf
```

This comments out every line from "database" through "timeout" by adding `# `
at the beginning.

### Negating Addresses with !

The `!` operator inverts an address, applying the command to lines that do NOT
match:

```bash
# Delete all lines that are NOT comments
sed '/^#/!d' /tmp/sed-practice/config.conf
```

This keeps only comment lines -- the opposite of `sed '/^#/d'`.

### The Last Line: $

The dollar sign represents the last line of a file:

```bash
# Print only the last line
sed -n '$p' /tmp/sed-practice/config.conf

# Delete the last line
sed '$d' /tmp/sed-practice/config.conf
```

## Introducing awk

While `grep` finds lines and `sed` transforms text, `awk` excels at working
with **columnar data**. If your data has fields separated by spaces, tabs,
commas, or colons, `awk` is the tool to reach for.

`awk` is actually a small programming language, but you can get enormous value
from just a few basic patterns.

## How awk Sees Text

`awk` reads input line by line and automatically splits each line into
**fields**:

```
Alice Math 95
  $1    $2  $3
```

- `$1` is the first field ("Alice")
- `$2` is the second field ("Math")
- `$3` is the third field ("95")
- `$0` is the entire line
- `NF` is the number of fields on the current line
- `NR` is the current line number (record number)

By default, fields are separated by whitespace (spaces or tabs).

## Basic awk: Printing Fields

The most fundamental `awk` command is `{print}`:

```bash
awk '{print $1}' /tmp/awk-practice/scores.txt
```

```
Alice
Bob
Charlie
Alice
Bob
Charlie
Alice
Bob
Charlie
```

This prints only the first field (the name) from each line.

Print multiple fields:

```bash
awk '{print $1, $3}' /tmp/awk-practice/scores.txt
```

```
Alice 95
Bob 82
Charlie 78
Alice 88
Bob 91
Charlie 85
Alice 92
Bob 76
Charlie 89
```

This prints names and scores, skipping the subject column.

**Tip:** When you put a comma between fields in `print`, awk inserts a space
(the Output Field Separator). Without the comma, the fields are concatenated
with no separator.

## Custom Field Separators: -F

Many files use delimiters other than spaces. The `-F` flag sets the field
separator:

```bash
awk -F: '{print $1}' /tmp/awk-practice/passwd-sample
```

```
root
daemon
bin
sys
nobody
alex
maria
jake
sara
```

This splits each line on colons (like `/etc/passwd` format) and prints the
username (first field).

Print username and home directory (fields 1 and 6):

```bash
awk -F: '{print $1, $6}' /tmp/awk-practice/passwd-sample
```

```
root /root
daemon /usr/sbin
bin /bin
sys /dev
nobody /nonexistent
alex /home/alex
maria /home/maria
jake /home/jake
sara /home/sara
```

## Pattern Matching in awk

You can filter which lines awk processes by adding a pattern before the action:

```bash
awk '/Engineering/ {print $2}' /tmp/awk-practice/employees.txt
```

```
Alice
Charlie
Frank
Hank
```

This prints the name (field 2) of every employee in the Engineering department.

### Comparison Operators

`awk` supports numeric and string comparisons:

```bash
# Print employees with salary above 80000
awk '$4 > 80000 {print $2, $4}' /tmp/awk-practice/employees.txt
```

```
Alice 85000
Charlie 91000
Frank 88000
Hank 95000
```

```bash
# Print lines where field 3 equals "Engineering"
awk '$3 == "Engineering" {print $0}' /tmp/awk-practice/employees.txt
```

## Formatted Output with printf

For more control over output formatting, use `printf` instead of `print`:

```bash
awk '{printf "%-10s scored %3d in %s\n", $1, $3, $2}' /tmp/awk-practice/scores.txt
```

```
Alice      scored  95 in Math
Bob        scored  82 in Math
Charlie    scored  78 in Math
...
```

The format specifiers work like C's printf:
- `%-10s` -- left-aligned string, 10 characters wide
- `%3d` -- right-aligned integer, 3 digits wide
- `\n` -- newline

## Built-in Variables

`awk` has several useful built-in variables:

| Variable | Meaning                              |
|----------|--------------------------------------|
| `$0`     | The entire current line              |
| `NR`     | Current line (record) number         |
| `NF`     | Number of fields on current line     |
| `FS`     | Input field separator                |
| `OFS`    | Output field separator               |

```bash
# Print line numbers with content
awk '{print NR, $0}' /tmp/awk-practice/scores.txt
```

```
1 Alice Math 95
2 Bob Math 82
3 Charlie Math 78
...
```

```bash
# Print the last field of each line
awk '{print $NF}' /tmp/awk-practice/access.log
```

```
1024
512
2048
4096
128
0
0
1024
2048
```

`$NF` is a clever trick: `NF` holds the number of fields, so `$NF` refers to
the last field regardless of how many fields there are.

## BEGIN and END Blocks

`awk` can execute code before processing starts and after all lines are done:

```bash
awk 'BEGIN {print "=== Score Report ==="} {print $1, $3} END {print "=== End ==="}' /tmp/awk-practice/scores.txt
```

```
=== Score Report ===
Alice 95
Bob 82
Charlie 78
...
=== End ===
```

This is useful for adding headers and footers, or for computing summaries:

```bash
awk '{sum += $3} END {print "Total:", sum, "Average:", sum/NR}' /tmp/awk-practice/scores.txt
```

```
Total: 776 Average: 86.2222
```

## Combining sed and awk

The real power comes from combining tools. Here are some practical examples:

```bash
# Extract usernames with bash shell, sorted
awk -F: '$7 ~ /bash/ {print $1}' /tmp/awk-practice/passwd-sample | sort
```

```
alex
root
sara
```

The `~` operator in awk means "matches the regex." This prints usernames where
field 7 (the shell) contains "bash".

```bash
# Clean up a config file and extract just key-value pairs
sed '/^#/d; /^$/d' /tmp/sed-practice/config.conf | awk -F= '{print $1}'
```

## CachyOS-Specific Notes

CachyOS ships with GNU `awk` (gawk) as the default `awk` implementation. GNU
awk is the most feature-rich version, supporting advanced features like
multidimensional arrays and network I/O. Everything in this lesson works with
any POSIX-compatible awk.

Useful CachyOS examples:

```bash
# List installed packages with their sizes
pacman -Qi | awk '/^Name/ {name=$3} /^Installed Size/ {print name, $4, $5}'

# Show users with real home directories
awk -F: '$6 ~ /^\/home/ {print $1, $6}' /etc/passwd
```

## Try It Yourself

Practice these exercises:

1. Print only usernames from the passwd-sample file:
   ```bash
   awk -F: '{print $1}' /tmp/awk-practice/passwd-sample
   ```

2. Print names and scores (columns 1 and 3) from scores.txt:
   ```bash
   awk '{print $1, $3}' /tmp/awk-practice/scores.txt
   ```

3. Find all Engineering employees and print their names and salaries:
   ```bash
   awk '$3 == "Engineering" {print $2, $4}' /tmp/awk-practice/employees.txt
   ```

4. Print usernames and shells from passwd-sample:
   ```bash
   awk -F: '{print $1, $7}' /tmp/awk-practice/passwd-sample
   ```

5. Calculate the average salary from employees.txt (skip the header):
   ```bash
   awk 'NR > 1 {sum += $4; count++} END {print "Average:", sum/count}' /tmp/awk-practice/employees.txt
   ```

6. Find all 404 errors in the access log:
   ```bash
   awk '$4 == 404 {print $1, $3}' /tmp/awk-practice/access.log
   ```

7. Use sed to comment out lines 8-11 of config.conf, then use awk to show
   only uncommented lines:
   ```bash
   sed '8,11s/^/# /' /tmp/sed-practice/config.conf | awk '/^[^#]/'
   ```

8. Print the total bytes transferred from the access log:
   ```bash
   awk '{sum += $5} END {print "Total bytes:", sum}' /tmp/awk-practice/access.log
   ```

In the next lesson, you will learn how to chain all of these text tools together
into powerful data-processing pipelines.
