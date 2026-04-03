---
id: 14
week: 3
title: "File Metadata and Types"
duration_minutes: 15
objectives:
  - "Determine file types using the file command"
  - "View detailed file metadata with stat"
  - "Count lines, words, and bytes with wc"
commands: [file, stat, wc, "wc -l", "wc -w", "wc -c"]
prerequisites: []
sandbox_commands: [file, stat, wc, cat, less, head, tail, ls, cd, pwd, echo, touch, mkdir, cp, find, grep, whoami, date, clear]
sandbox_setup: |
  echo "Plain text file" > readme.txt
  echo "#!/bin/bash" > script.sh
  echo "echo 'Hello World'" >> script.sh
  chmod +x script.sh
  echo '{"name": "test", "version": "1.0"}' > data.json
  echo "<html><body>Hello</body></html>" > page.html
  echo "Line 1" > counted.txt
  echo "Line 2 with more words" >> counted.txt
  echo "Line 3 short" >> counted.txt
  echo "Line 4 the final line of this file" >> counted.txt
  mkdir empty_dir
  ln -s readme.txt link_to_readme
  printf '\x89PNG\r\n' > fake_image.png
  echo "Explore file types!" > README.txt
---
# File Metadata and Types

Not every file on a Linux system is plain text. You will encounter scripts, binaries,
images, compressed archives, symlinks, and many other types. Linux does not rely on
file extensions to determine what a file is -- it examines the actual content. This
lesson teaches you three essential commands for understanding what files contain and
how big they are.

## Identifying File Types with `file`

The `file` command inspects a file's content (not its name) and tells you what it is:

```bash
file ~/readme.txt
```

Output:

```
/home/user/readme.txt: ASCII text
```

### Examples with Different File Types

```bash
file ~/backup.sh
```

```
/home/user/backup.sh: Bash script, ASCII text executable
```

```bash
file ~/data.bin
```

```
/home/user/data.bin: data
```

```bash
file ~/readme_link.txt
```

```
/home/user/readme_link.txt: symbolic link to /home/user/readme.txt
```

```bash
file ~/projects
```

```
/home/user/projects: directory
```

### Why This Matters

On Linux, file extensions are **conventions**, not requirements. A file named
`photo.txt` could actually be a JPEG image. The `file` command reads the file's
**magic bytes** (special signatures at the start of a file) to determine the true type:

```bash
# Extension says .txt but file reveals the truth
file suspicious.txt
# Output might be: suspicious.txt: JPEG image data
```

### Useful `file` Options

| Option | Purpose |
|--------|---------|
| `file -i` | Show MIME type (e.g., `text/plain; charset=us-ascii`) |
| `file -b` | Brief output -- omit the filename prefix |
| `file -L` | Follow symbolic links and report the target's type |

```bash
file -i ~/readme.txt
```

```
/home/user/readme.txt: text/plain; charset=us-ascii
```

```bash
file -b ~/backup.sh
```

```
Bash script, ASCII text executable
```

## Viewing Detailed Metadata with `stat`

The `stat` command reveals everything the filesystem knows about a file:

```bash
stat ~/readme.txt
```

Output (abbreviated):

```
  File: /home/user/readme.txt
  Size: 193        Blocks: 8          IO Block: 4096   regular file
Access: (0644/-rw-r--r--)  Uid: (1000/user)   Gid: (1000/user)
Access: 2026-03-27 08:00:00.000000000 +0000
Modify: 2026-03-27 08:00:00.000000000 +0000
Change: 2026-03-27 08:00:00.000000000 +0000
 Birth: 2026-03-27 08:00:00.000000000 +0000
```

### Understanding `stat` Output

| Field | Meaning |
|-------|---------|
| **Size** | File size in bytes |
| **Blocks** | Number of 512-byte blocks allocated |
| **IO Block** | Filesystem block size |
| **regular file** | File type (could also be directory, symbolic link, etc.) |
| **Access (permissions)** | Octal and symbolic permission notation |
| **Uid / Gid** | Owner user and group |
| **Access time** | Last time the file was read |
| **Modify time** | Last time the file contents changed |
| **Change time** | Last time metadata (permissions, owner) changed |
| **Birth time** | When the file was created (if supported by filesystem) |

### Comparing `stat` and `ls -l`

`ls -l` gives you a quick summary. `stat` gives you the full picture:

```bash
ls -l ~/readme.txt
# -rw-r--r-- 1 user user 193 Mar 27 08:00 /home/user/readme.txt

stat ~/readme.txt
# Shows all of the above plus timestamps with nanosecond precision
```

### `stat` on Directories and Links

```bash
stat ~/projects
stat ~/readme_link.txt
```

For symbolic links, `stat` shows metadata about the link itself. Add `-L` to follow
the link and show the target's metadata:

```bash
stat -L ~/readme_link.txt
```

## Counting with `wc`

The `wc` (word count) command counts lines, words, and bytes in files:

```bash
wc ~/readme.txt
```

Output:

```
  5  29 193 /home/user/readme.txt
```

That means: **5 lines**, **29 words**, **193 bytes**.

### Specific Counts

| Option | Counts |
|--------|--------|
| `wc -l` | Lines only |
| `wc -w` | Words only |
| `wc -c` | Bytes only |
| `wc -m` | Characters only (differs from bytes for multi-byte encodings) |

```bash
wc -l ~/readme.txt
# 5 /home/user/readme.txt

wc -w ~/readme.txt
# 29 /home/user/readme.txt

wc -c ~/readme.txt
# 193 /home/user/readme.txt
```

### Counting Lines in Multiple Files

```bash
wc -l ~/readme.txt ~/scores.csv ~/backup.sh
```

Output:

```
  5 /home/user/readme.txt
  7 /home/user/scores.csv
  5 /home/user/backup.sh
 17 total
```

Notice that `wc` provides a **total** line when given multiple files.

### Common `wc` Patterns

Count how many files are in a directory:

```bash
ls ~/projects | wc -l
```

Count how many lines contain "ERROR" in a log:

```bash
grep ERROR ~/app.log | wc -l
```

Count lines in all `.txt` files:

```bash
wc -l ~/*.txt
```

## Practical Comparison

| Question | Command |
|----------|---------|
| What type of file is this? | `file filename` |
| When was this file last modified? | `stat filename` |
| What permissions does it have (in octal)? | `stat filename` |
| How many lines does this file have? | `wc -l filename` |
| How large is this file in bytes? | `wc -c filename` or `stat filename` |

## Try It Yourself

1. **Identify file types:**
   ```bash
   file ~/readme.txt
   file ~/backup.sh
   file ~/data.bin
   file ~/readme_link.txt
   file ~/projects
   ```
   Notice how each file produces a different description.

2. **Check MIME types:**
   ```bash
   file -i ~/readme.txt
   file -i ~/data.bin
   ```

3. **View full metadata:**
   ```bash
   stat ~/readme.txt
   ```
   Find the file size, permissions, and modification time.

4. **Count lines, words, and bytes:**
   ```bash
   wc ~/readme.txt
   wc -l ~/scores.csv
   ```

5. **Count lines across multiple files:**
   ```bash
   wc -l ~/readme.txt ~/scores.csv ~/backup.sh
   ```

6. **Combine commands:** How many lines does `backup.sh` have?
   ```bash
   wc -l ~/backup.sh
   ```

## Summary

- `file` identifies what a file actually contains, regardless of its extension.
- `stat` shows comprehensive metadata: size, permissions, timestamps, and ownership.
- `wc` counts lines (`-l`), words (`-w`), and bytes (`-c`).
- Linux determines file types by content, not by filename extension.
- Use `file -i` for MIME types and `stat -L` to follow symbolic links.
