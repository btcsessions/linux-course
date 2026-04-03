---
id: 15
week: 3
title: "Comparing and Sorting Files"
duration_minutes: 15
objectives:
  - "Compare files using diff and understand unified diff output"
  - "Sort file contents with sort, including numeric and reverse sorting"
  - "Remove duplicate lines with uniq"
  - "Extract specific fields from structured data with cut"
commands: [diff, "diff -u", sort, "sort -n", "sort -r", uniq, "cut -d -f"]
prerequisites: []
sandbox_commands: [diff, sort, uniq, cut, file, stat, wc, cat, less, head, tail, ls, cd, pwd, echo, touch, mkdir, cp, find, grep, whoami, date, clear]
sandbox_setup: |
  echo "alpha=true" > original.conf
  echo "beta=false" >> original.conf
  echo "gamma=100" >> original.conf
  echo "delta=hello" >> original.conf
  cp original.conf modified.conf
  sed -i 's/beta=false/beta=true/' modified.conf
  echo "epsilon=new" >> modified.conf
  echo "banana" > fruits.txt
  echo "apple" >> fruits.txt
  echo "cherry" >> fruits.txt
  echo "apple" >> fruits.txt
  echo "banana" >> fruits.txt
  echo "date" >> fruits.txt
  echo "cherry" >> fruits.txt
  echo "Name:Age:City" > people.csv
  echo "Alice:30:Portland" >> people.csv
  echo "Bob:25:Seattle" >> people.csv
  echo "Carol:35:Denver" >> people.csv
  echo "Dave:28:Austin" >> people.csv
  echo "100" > numbers.txt
  echo "5" >> numbers.txt
  echo "42" >> numbers.txt
  echo "7" >> numbers.txt
  echo "99" >> numbers.txt
  echo "23" >> numbers.txt
  echo "Practice sorting and comparing!" > README.txt
---
# Comparing and Sorting Files

When working with configuration files, log data, or any structured text, you will
frequently need to compare two versions of a file, sort data, remove duplicates, or
extract specific columns. This lesson covers four essential commands that handle these
tasks.

## Comparing Files with `diff`

The `diff` command compares two files line by line and shows the differences:

```bash
diff ~/original.txt ~/modified.txt
```

Output:

```
2c2
< host=localhost
---
> host=192.168.1.100
4,6c4,6
< debug=true
< log_level=INFO
< max_connections=50
---
> debug=false
> log_level=WARNING
> max_connections=100
7a8
> database_url=postgres://localhost:5432/app
```

### Reading `diff` Output

| Symbol | Meaning |
|--------|---------|
| `<` | Line from the first file |
| `>` | Line from the second file |
| `c` | Lines were **changed** |
| `a` | Lines were **added** |
| `d` | Lines were **deleted** |
| `2c2` | Line 2 in file 1 changed to line 2 in file 2 |

### Unified Diff with `diff -u`

The unified format is easier to read and is the standard format for patches:

```bash
diff -u ~/original.txt ~/modified.txt
```

Output:

```diff
--- /home/user/original.txt
+++ /home/user/modified.txt
@@ -1,7 +1,8 @@
 # Server Configuration
-host=localhost
+host=192.168.1.100
 port=8080
-debug=true
-log_level=INFO
-max_connections=50
+debug=false
+log_level=WARNING
+max_connections=100
 timeout=30
+database_url=postgres://localhost:5432/app
```

### Reading Unified Diff

| Symbol | Meaning |
|--------|---------|
| `---` | Original file |
| `+++` | Modified file |
| `@@` | Location marker (line numbers) |
| `-` (red) | Line removed from original |
| `+` (green) | Line added in modified version |
| (no prefix) | Unchanged context line |

> **Tip:** `diff -u` is the format used by `git diff`. Learning to read it now will
> help you enormously when working with version control.

### Other Useful `diff` Options

| Option | Purpose |
|--------|---------|
| `diff -y` | Side-by-side comparison |
| `diff -q` | Only report whether files differ, not how |
| `diff -r dir1 dir2` | Recursively compare two directories |
| `diff --color` | Colorize the output (on CachyOS) |

```bash
diff -q ~/original.txt ~/modified.txt
# Files /home/user/original.txt and /home/user/modified.txt differ

diff -y ~/original.txt ~/modified.txt
# Side-by-side view with | marking changed lines
```

## Sorting File Contents with `sort`

The `sort` command arranges lines in order. By default it sorts alphabetically:

```bash
sort ~/access.log
```

Output:

```
10.0.0.5
10.0.0.5
10.0.0.5
10.0.0.5
172.16.0.1
172.16.0.1
192.168.1.10
192.168.1.10
192.168.1.10
192.168.1.50
```

### Numeric Sorting with `sort -n`

Alphabetic sort treats numbers as text (`9` comes after `80` alphabetically). Use
`-n` for proper numeric ordering:

```bash
sort ~/scores.txt        # alphabetic: 100, 65, 71, 78, ...
sort -n ~/scores.txt     # numeric:    65, 71, 78, 85, ...
```

```bash
sort -n ~/scores.txt
```

Output:

```
65
71
78
78
85
88
88
92
92
95
100
100
```

### Reverse Sorting with `sort -r`

```bash
sort -rn ~/scores.txt
```

Output (highest to lowest):

```
100
100
95
92
92
88
88
85
78
78
71
65
```

### Sorting by a Specific Column

Use `-t` to set the delimiter and `-k` to choose the field:

```bash
# Sort employees by salary (field 3), numerically
sort -t',' -k3 -n ~/employees.csv
```

### Other `sort` Options

| Option | Purpose |
|--------|---------|
| `sort -u` | Sort and remove duplicates (combines sort + uniq) |
| `sort -f` | Case-insensitive sort |
| `sort -t',' -kN` | Sort by field N using comma as delimiter |
| `sort -h` | Human-readable numeric sort (1K, 2M, 3G) |

## Removing Duplicates with `uniq`

`uniq` removes **adjacent** duplicate lines. This is why it is almost always used
after `sort`:

```bash
sort ~/access.log | uniq
```

Output:

```
10.0.0.5
172.16.0.1
192.168.1.10
192.168.1.50
```

### Counting Occurrences with `uniq -c`

```bash
sort ~/access.log | uniq -c
```

Output:

```
      4 10.0.0.5
      2 172.16.0.1
      3 192.168.1.10
      1 192.168.1.50
```

### Finding Only Duplicated or Unique Lines

```bash
# Show only lines that appear more than once
sort ~/access.log | uniq -d

# Show only lines that appear exactly once
sort ~/access.log | uniq -u
```

### The Classic `sort | uniq -c | sort -rn` Pattern

This pipeline is one of the most useful in all of Linux. It answers "what appears
most frequently?"

```bash
sort ~/access.log | uniq -c | sort -rn
```

Output (most frequent first):

```
      4 10.0.0.5
      3 192.168.1.10
      2 172.16.0.1
      1 192.168.1.50
```

> **Important:** `uniq` only removes **adjacent** duplicates. If you skip the initial
> `sort`, non-adjacent duplicates will remain. Always pipe through `sort` first.

## Extracting Fields with `cut`

`cut` extracts specific columns (fields) from structured text:

```bash
# Extract the first field (name) from the CSV
cut -d',' -f1 ~/employees.csv
```

Output:

```
name
Alice
Bob
Carol
Dave
Eve
Frank
Grace
```

### Key `cut` Options

| Option | Purpose |
|--------|---------|
| `-d','` | Set the delimiter (comma in this case) |
| `-f1` | Extract field 1 |
| `-f1,3` | Extract fields 1 and 3 |
| `-f2-4` | Extract fields 2 through 4 |

### Examples

```bash
# Extract names and salaries
cut -d',' -f1,3 ~/employees.csv
```

Output:

```
name,salary
Alice,95000
Bob,72000
Carol,105000
Dave,68000
Eve,78000
Frank,92000
Grace,71000
```

```bash
# Extract department and city
cut -d',' -f2,4 ~/employees.csv
```

Output:

```
department,city
Engineering,Portland
Marketing,Seattle
Engineering,Portland
Sales,Denver
Marketing,Seattle
Engineering,Austin
Sales,Denver
```

### Combining `cut` with Other Commands

Find unique departments:

```bash
cut -d',' -f2 ~/employees.csv | tail -n +2 | sort -u
```

Output:

```
Engineering
Marketing
Sales
```

The `tail -n +2` skips the header row.

## Combining Everything: Real-World Pipelines

### Which department has the most employees?

```bash
cut -d',' -f2 ~/employees.csv | tail -n +2 | sort | uniq -c | sort -rn
```

### What are the top 3 most frequent IPs?

```bash
sort ~/access.log | uniq -c | sort -rn | head -n 3
```

### What is the highest score?

```bash
sort -rn ~/scores.txt | head -n 1
```

## Try It Yourself

1. **Compare the two config files:**
   ```bash
   diff ~/original.txt ~/modified.txt
   diff -u ~/original.txt ~/modified.txt
   ```
   Identify which lines were changed, added, or remain the same.

2. **Sort the scores numerically:**
   ```bash
   sort -n ~/scores.txt
   ```

3. **Find unique IP addresses and their frequency:**
   ```bash
   sort ~/access.log | uniq -c | sort -rn
   ```

4. **Extract employee names and cities:**
   ```bash
   cut -d',' -f1,4 ~/employees.csv
   ```

5. **List unique cities:**
   ```bash
   cut -d',' -f4 ~/employees.csv | tail -n +2 | sort -u
   ```

6. **Find the top-scoring value:**
   ```bash
   sort -rn ~/scores.txt | head -n 1
   ```

## Summary

- `diff` compares two files and shows differences; `diff -u` gives unified format.
- `sort` orders lines alphabetically; add `-n` for numeric, `-r` for reverse.
- `uniq` removes adjacent duplicates -- always `sort` first; use `-c` to count.
- `cut -d',' -f1,3` extracts specific fields from delimited data.
- The `sort | uniq -c | sort -rn` pattern finds the most frequent items.
