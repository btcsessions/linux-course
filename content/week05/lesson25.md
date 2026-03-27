---
id: 25
week: 5
title: "Putting Text Tools Together"
duration_minutes: 15
objectives:
  - "Chain grep, sed, awk, sort, and uniq into multi-stage pipelines"
  - "Extract and summarize data from realistic log files"
  - "Build reusable text-processing pipelines for common tasks"
commands: ["grep | sed | awk | sort | uniq"]
prerequisites: []
sandbox_commands: [grep, sed, awk, sort, uniq, cat, wc]
sandbox_setup: |
  mkdir -p /tmp/pipeline-practice
  cat > /tmp/pipeline-practice/access.log <<'LOGEOF'
  192.168.1.10 - - [15/Mar/2026:08:01:12 +0000] "GET /index.html HTTP/1.1" 200 5120
  192.168.1.25 - - [15/Mar/2026:08:01:15 +0000] "GET /style.css HTTP/1.1" 200 1024
  10.0.0.5 - - [15/Mar/2026:08:02:00 +0000] "POST /api/login HTTP/1.1" 200 256
  192.168.1.10 - - [15/Mar/2026:08:02:22 +0000] "GET /dashboard HTTP/1.1" 200 8192
  192.168.1.50 - - [15/Mar/2026:08:03:01 +0000] "GET /index.html HTTP/1.1" 200 5120
  10.0.0.5 - - [15/Mar/2026:08:03:45 +0000] "GET /api/users HTTP/1.1" 403 128
  192.168.1.10 - - [15/Mar/2026:08:04:10 +0000] "POST /api/data HTTP/1.1" 500 0
  192.168.1.25 - - [15/Mar/2026:08:05:00 +0000] "GET /profile HTTP/1.1" 200 4096
  10.0.0.5 - - [15/Mar/2026:08:05:30 +0000] "GET /index.html HTTP/1.1" 200 5120
  192.168.1.50 - - [15/Mar/2026:08:06:00 +0000] "GET /about.html HTTP/1.1" 200 3072
  192.168.1.10 - - [15/Mar/2026:08:06:15 +0000] "GET /style.css HTTP/1.1" 200 1024
  192.168.1.25 - - [15/Mar/2026:08:07:00 +0000] "GET /dashboard HTTP/1.1" 200 8192
  10.0.0.5 - - [15/Mar/2026:08:07:30 +0000] "POST /api/login HTTP/1.1" 401 64
  192.168.1.10 - - [15/Mar/2026:08:08:00 +0000] "GET /index.html HTTP/1.1" 200 5120
  192.168.1.50 - - [15/Mar/2026:08:08:30 +0000] "GET /contact.html HTTP/1.1" 404 0
  10.0.0.5 - - [15/Mar/2026:08:09:00 +0000] "GET /api/users HTTP/1.1" 200 2048
  192.168.1.25 - - [15/Mar/2026:08:09:30 +0000] "POST /api/data HTTP/1.1" 200 512
  192.168.1.10 - - [15/Mar/2026:08:10:00 +0000] "GET /dashboard HTTP/1.1" 200 8192
  192.168.1.50 - - [15/Mar/2026:08:10:30 +0000] "GET /index.html HTTP/1.1" 200 5120
  10.0.0.5 - - [15/Mar/2026:08:11:00 +0000] "GET /style.css HTTP/1.1" 200 1024
  LOGEOF
  cat > /tmp/pipeline-practice/syslog.txt <<'SYSEOF'
  Mar 15 08:01:12 cachyos systemd[1]: Started Network Manager.
  Mar 15 08:01:13 cachyos NetworkManager[512]: <info> device (enp3s0): state change: disconnected -> prepare
  Mar 15 08:01:15 cachyos NetworkManager[512]: <info> device (enp3s0): state change: prepare -> config
  Mar 15 08:01:18 cachyos NetworkManager[512]: <info> device (enp3s0): state change: config -> ip-config
  Mar 15 08:01:20 cachyos NetworkManager[512]: <info> device (enp3s0): state change: ip-config -> activated
  Mar 15 08:01:20 cachyos systemd[1]: Started Bluetooth service.
  Mar 15 08:02:00 cachyos sshd[1024]: Accepted publickey for alex from 192.168.1.10 port 54321
  Mar 15 08:05:00 cachyos sshd[1025]: Failed password for root from 10.0.0.99 port 12345
  Mar 15 08:05:01 cachyos sshd[1025]: Failed password for root from 10.0.0.99 port 12345
  Mar 15 08:05:02 cachyos sshd[1025]: Failed password for root from 10.0.0.99 port 12345
  Mar 15 08:10:00 cachyos pacman[2048]: Running 'pacman -Syu'
  Mar 15 08:10:05 cachyos pacman[2048]: upgraded linux-cachyos (6.12.1-1 -> 6.12.2-1)
  Mar 15 08:10:06 cachyos pacman[2048]: upgraded mesa (24.3.1-1 -> 24.3.2-1)
  Mar 15 08:15:00 cachyos crond[256]: (root) CMD (/usr/bin/updatedb)
  Mar 15 08:30:00 cachyos crond[256]: (root) CMD (/usr/bin/updatedb)
  SYSEOF
  cat > /tmp/pipeline-practice/sales.csv <<'SALESEOF'
  date,product,quantity,price
  2026-03-01,Widget,10,25.00
  2026-03-01,Gadget,5,49.99
  2026-03-02,Widget,8,25.00
  2026-03-02,Gizmo,3,99.99
  2026-03-03,Gadget,12,49.99
  2026-03-03,Widget,6,25.00
  2026-03-04,Gizmo,2,99.99
  2026-03-04,Widget,15,25.00
  2026-03-05,Gadget,7,49.99
  2026-03-05,Widget,9,25.00
  SALESEOF
---

# Putting Text Tools Together

## The Power of Pipelines

You have now learned four major text tools:

- **grep** -- find lines matching a pattern
- **sed** -- transform text with substitutions and deletions
- **awk** -- extract and manipulate columnar data
- **sort** and **uniq** -- order and deduplicate data

Each tool does one thing well. The real magic happens when you connect them
with pipes (`|`), building multi-stage processing pipelines. This is the Unix
philosophy in action: small tools, combined freely.

## Refresher: How Pipes Work

The pipe operator `|` sends the output of one command as input to the next:

```
command1 | command2 | command3
```

Data flows left to right. Each command processes the text and passes its output
to the next stage. No temporary files needed.

## sort and uniq Quick Reference

Before diving into pipelines, let's make sure you are comfortable with `sort`
and `uniq`:

```bash
# Sort lines alphabetically
sort file.txt

# Sort numerically
sort -n file.txt

# Sort in reverse
sort -r file.txt

# Sort by the third field (space-delimited)
sort -k3 file.txt

# Remove duplicate adjacent lines
uniq file.txt

# Count duplicates
uniq -c file.txt
```

**Warning:** `uniq` only removes *adjacent* duplicates. Always `sort` first
if you want to eliminate all duplicates:

```bash
sort file.txt | uniq
```

## Pipeline Pattern 1: Find and Count

One of the most common patterns is extracting a field, sorting, and counting
occurrences.

### Example: Top IP Addresses in the Access Log

Which IP addresses made the most requests?

```bash
awk '{print $1}' /tmp/pipeline-practice/access.log | sort | uniq -c | sort -rn
```

```
      5 192.168.1.10
      4 10.0.0.5
      4 192.168.1.50
      4 192.168.1.25
      3 192.168.1.25
```

Let's break this down step by step:

1. `awk '{print $1}'` -- extracts the IP address (first field) from each line
2. `sort` -- groups identical IPs together (required for `uniq`)
3. `uniq -c` -- counts consecutive identical lines
4. `sort -rn` -- sorts the counts numerically in reverse (highest first)

This is the classic "top N" pipeline. You will use it constantly.

### Example: Most Requested URLs

```bash
awk '{print $7}' /tmp/pipeline-practice/access.log | sort | uniq -c | sort -rn | head -5
```

```
      5 /index.html
      3 /dashboard
      3 /style.css
      2 /api/users
      2 /api/login
```

We added `head -5` at the end to see only the top 5. The `$7` refers to the
URL path in the log format.

## Pipeline Pattern 2: Filter, Transform, Extract

### Example: Find Failed SSH Logins and Extract IPs

```bash
grep "Failed password" /tmp/pipeline-practice/syslog.txt | awk '{print $11}' | sort -u
```

```
10.0.0.99
```

1. `grep "Failed password"` -- filters to only failed login lines
2. `awk '{print $11}'` -- extracts the IP address field
3. `sort -u` -- sorts and removes duplicates (`-u` is shorthand for `sort | uniq`)

### Example: Find All Error Status Codes and Their URLs

```bash
awk '$9 >= 400 {print $9, $7}' /tmp/pipeline-practice/access.log | sort
```

```
401 /api/login
403 /api/users
404 /contact.html
500 /api/data
```

Here `awk` does the filtering (status code in field 9 >= 400) and extraction
in one step.

## Pipeline Pattern 3: Transform and Summarize

### Example: Calculate Total Bytes Transferred per IP

```bash
awk '{ip[$1] += $10} END {for (i in ip) print ip[i], i}' /tmp/pipeline-practice/access.log | sort -rn
```

```
27648 192.168.1.10
13824 192.168.1.25
13312 192.168.1.50
8640 10.0.0.5
```

This uses an `awk` associative array to sum bytes (field 10) by IP address
(field 1), then prints the totals.

### Example: Summarize Products Sold

```bash
grep -v "^date" /tmp/pipeline-practice/sales.csv | awk -F, '{print $2}' | sort | uniq -c | sort -rn
```

```
      5 Widget
      3 Gadget
      2 Gizmo
```

1. `grep -v "^date"` -- skip the header line
2. `awk -F, '{print $2}'` -- extract the product name (comma-separated)
3. `sort | uniq -c` -- count each product
4. `sort -rn` -- show most frequent first

## Pipeline Pattern 4: Clean and Reformat

### Example: Extract Clean Key-Value Pairs from a Config

```bash
sed '/^#/d; /^$/d' /tmp/sed-practice/config.conf | sed 's/ *= */=/' | sort
```

This removes comments and blank lines, then normalizes the spacing around `=`
signs, and sorts the result.

### Example: Convert Log Timestamps

```bash
grep "GET" /tmp/pipeline-practice/access.log | sed 's/\[//; s/\]//' | awk '{print $4, $7}'
```

This extracts the timestamp and URL from GET requests, stripping the square
brackets from the date field.

## Pipeline Pattern 5: Reporting

### Example: Quick Log Summary

```bash
echo "=== Access Log Summary ==="
echo "Total requests: $(wc -l < /tmp/pipeline-practice/access.log)"
echo "Unique IPs: $(awk '{print $1}' /tmp/pipeline-practice/access.log | sort -u | wc -l)"
echo "Error requests (4xx/5xx):"
awk '$9 >= 400 {print "  " $9, $7}' /tmp/pipeline-practice/access.log
echo "Top 3 requested pages:"
awk '{print $7}' /tmp/pipeline-practice/access.log | sort | uniq -c | sort -rn | head -3 | sed 's/^/  /'
```

```
=== Access Log Summary ===
Total requests: 20
Unique IPs: 4
Error requests (4xx/5xx):
  403 /api/users
  500 /api/data
  401 /api/login
  404 /contact.html
Top 3 requested pages:
      5 /index.html
      3 /dashboard
      3 /style.css
```

## Building Pipelines Incrementally

**Tip:** Never try to write a complex pipeline all at once. Build it one stage
at a time:

1. Start with the first command and check its output
2. Add the next pipe stage and verify
3. Continue until you get the result you need

For example, to find the busiest hour:

```bash
# Step 1: See what the raw data looks like
cat /tmp/pipeline-practice/access.log

# Step 2: Extract the time field
awk '{print $4}' /tmp/pipeline-practice/access.log

# Step 3: Extract just the hour
awk '{print $4}' /tmp/pipeline-practice/access.log | sed 's/.*://' | sed 's/:.*//'

# Hmm, that's not right. Let me try differently:
awk '{print $4}' /tmp/pipeline-practice/access.log | awk -F: '{print $2}'

# Step 4: Count and sort
awk '{print $4}' /tmp/pipeline-practice/access.log | awk -F: '{print $2}' | sort | uniq -c | sort -rn
```

Building incrementally helps you catch mistakes early and understand what each
stage does.

## Avoiding Common Pipeline Mistakes

1. **Forgetting to sort before uniq.** `uniq` only removes adjacent duplicates.
   Always pipe through `sort` first unless the data is already sorted.

2. **Wrong field numbers.** Field numbers depend on the delimiter. A CSV file
   parsed with `awk -F,` has different field numbers than the same file parsed
   with default whitespace splitting.

3. **Quoting issues.** In complex pipelines, be careful with quotes:
   ```bash
   # This works -- each command is quoted properly
   grep "ERROR" log.txt | awk '{print $1}'

   # This does NOT work -- the pipe is inside the quotes
   grep "ERROR log.txt | awk '{print $1}'"
   ```

4. **Forgetting that grep uses regex.** If searching for a literal dot or
   bracket, escape it: `grep "version 1\.2"` not `grep "version 1.2"`.

## Real-World Applications

These pipeline patterns are used every day in real system administration:

- **Security monitoring:** Find repeated failed login attempts
- **Performance analysis:** Identify slow API endpoints from access logs
- **Capacity planning:** Track disk usage trends from monitoring data
- **Data migration:** Reformat CSV files for import into databases
- **Configuration management:** Audit settings across multiple servers

## CachyOS-Specific Notes

CachyOS uses `journalctl` for system logs, but the output is plain text that
works perfectly with grep/sed/awk pipelines:

```bash
# Find all pacman operations today
journalctl --since today | grep pacman

# Count SSH connection attempts by IP
journalctl -u sshd | grep "Failed" | awk '{print $11}' | sort | uniq -c | sort -rn
```

You can also use pipelines with pacman:

```bash
# List explicitly installed packages sorted by size
pacman -Qi | awk '/^Name/ {name=$3} /^Installed Size/ {print $4, $5, name}' | sort -rn | head -20
```

## Try It Yourself

Work through these exercises using the sandbox files:

1. Find the top 3 IP addresses by request count in access.log:
   ```bash
   awk '{print $1}' /tmp/pipeline-practice/access.log | sort | uniq -c | sort -rn | head -3
   ```

2. List all unique HTTP status codes in the access log:
   ```bash
   awk '{print $9}' /tmp/pipeline-practice/access.log | sort -u
   ```

3. Find how many requests returned a 200 status:
   ```bash
   awk '$9 == 200' /tmp/pipeline-practice/access.log | wc -l
   ```

4. Extract the IP addresses of all failed SSH logins from syslog.txt:
   ```bash
   grep "Failed" /tmp/pipeline-practice/syslog.txt | awk '{print $11}' | sort -u
   ```

5. Count the total quantity of each product sold in sales.csv:
   ```bash
   grep -v "^date" /tmp/pipeline-practice/sales.csv | awk -F, '{qty[$2] += $3} END {for (p in qty) print qty[p], p}' | sort -rn
   ```

6. Find all services mentioned in syslog.txt (the process name before the PID):
   ```bash
   awk '{print $5}' /tmp/pipeline-practice/syslog.txt | sed 's/\[.*//' | sort -u
   ```

7. Show all URLs that returned errors (status >= 400), with counts:
   ```bash
   awk '$9 >= 400 {print $7}' /tmp/pipeline-practice/access.log | sort | uniq -c | sort -rn
   ```

8. Challenge: Build a one-liner that shows the total bytes transferred per URL
   path, sorted by bytes descending.

Congratulations -- you now have a solid toolkit for text processing on the Linux
command line. The combination of grep, sed, awk, sort, and uniq can handle the
vast majority of text-processing tasks you will encounter as a Linux user.
