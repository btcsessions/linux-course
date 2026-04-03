---
id: 17
week: 4
title: "Understanding File Permissions"
duration_minutes: 15
objectives:
  - "Read and interpret the rwxrwxrwx permission string"
  - "Explain the meaning of read, write, and execute for files versus directories"
  - "Recognise special permissions: setuid, setgid, and the sticky bit"
commands: [ls -l, stat]
prerequisites: []
sandbox_commands: [id, groups, whoami, cat, less, grep, ls, cd, pwd, echo, touch, mkdir, cp, head, tail, find, wc, sort, cut, stat, file, clear, date, chmod]
sandbox_setup: |
  echo "Public file" > public.txt
  chmod 644 public.txt
  echo "Private file" > private.txt
  chmod 600 private.txt
  echo "#!/bin/bash" > script.sh
  echo "echo Hello" >> script.sh
  chmod 755 script.sh
  mkdir shared_dir personal_dir
  chmod 755 shared_dir
  chmod 700 personal_dir
  echo "Shared content" > shared_dir/readme.txt
  echo "Personal content" > personal_dir/secret.txt
  echo "Explore permissions with ls -l!" > README.txt
---
# Understanding File Permissions

File permissions are the cornerstone of Linux security. They determine who can read,
modify, or execute every file and directory on the system. Before you can change
permissions (covered in the next lesson), you need to be able to **read** them. This
lesson teaches you how to decode the permission string you see in `ls -l` output and
understand what each bit means.

## The `ls -l` Output Decoded

Run `ls -l` in any directory:

```bash
ls -l ~/permlab/
```

You will see output similar to:

```
-rwxr-xr-x 1 alex alex   38 Mar 27 10:00 greet.sh
-rw-r--r-- 1 alex alex   14 Mar 27 10:00 readme.txt
drwxr-x--- 2 alex alex 4096 Mar 27 10:00 docs
lrwxrwxrwx 1 alex alex   26 Mar 27 10:00 link_to_readme -> readme.txt
```

Each line begins with a 10-character permission string. Let us break it down.

## The 10-Character Permission String

```
d rwx r-x ---
^ ^^^ ^^^ ^^^
|  |   |   |
|  |   |   +-- Others (everyone else)
|  |   +------ Group
|  +---------- Owner (user)
+------------- File type
```

### Position 1 -- File Type

| Character | Meaning          |
|-----------|------------------|
| `-`       | Regular file     |
| `d`       | Directory        |
| `l`       | Symbolic link    |
| `c`       | Character device |
| `b`       | Block device     |
| `p`       | Named pipe       |
| `s`       | Socket           |

### Positions 2--10 -- Permission Triplets

The remaining nine characters form three groups of three, called **triplets**:

| Triplet   | Applies to                |
|-----------|---------------------------|
| Positions 2--4 | **Owner** (the user who owns the file) |
| Positions 5--7 | **Group** (members of the file's group) |
| Positions 8--10 | **Others** (everyone else) |

Each position is either a permission letter or a `-` (denied):

| Letter | Meaning   |
|--------|-----------|
| `r`    | Read      |
| `w`    | Write     |
| `x`    | Execute   |
| `-`    | Denied    |

### Worked Example

```
-rw-r--r--
```

- File type: `-` (regular file)
- Owner: `rw-` -- read and write, no execute
- Group: `r--` -- read only
- Others: `r--` -- read only

## What r, w, x Mean for Files

| Permission | Effect on a regular file                              |
|------------|-------------------------------------------------------|
| `r` (read) | Can view / copy the file's contents                  |
| `w` (write) | Can modify or truncate the file                     |
| `x` (execute) | Can run the file as a program or script            |

A script or binary needs the **execute** bit set before the kernel will allow you to
run it:

```bash
./greet.sh      # works only if x is set
```

Without `x`, you get `Permission denied`.

> **Tip:** A file can be writable but not readable. This is unusual but valid -- you
> could append to a log file without being able to read its contents.

## What r, w, x Mean for Directories

Directories behave differently. This catches many beginners off guard:

| Permission | Effect on a directory                                     |
|------------|-----------------------------------------------------------|
| `r` (read) | Can list the names of files inside (`ls`)                |
| `w` (write) | Can create, rename, or delete files inside              |
| `x` (execute) | Can enter the directory (`cd`) and access file metadata |

### Key Insight: `x` Without `r`

If a directory has `--x` but no `r`, you can `cd` into it and access files **if you
know their names**, but you cannot list its contents with `ls`. This is sometimes
used for restricted shared directories.

### Key Insight: `r` Without `x`

If a directory has `r--` but no `x`, you can list file names but cannot access any
file metadata (sizes, permissions) or read file contents. This combination is rarely
useful.

> **Warning:** To delete a file, you need **write and execute** permission on the
> **parent directory**, not on the file itself. This surprises many new users.

## Inspecting Permissions with `stat`

While `ls -l` gives a human-readable summary, `stat` provides the full picture:

```bash
stat ~/permlab/readme.txt
```

Sample output:

```
  File: /home/alex/permlab/readme.txt
  Size: 14          Blocks: 8          IO Block: 4096   regular file
Device: 254,1       Inode: 1048601     Links: 1
Access: (0644/-rw-r--r--)  Uid: (1000/   alex)   Gid: (1000/   alex)
Access: 2026-03-27 10:00:00.000000000 +0000
Modify: 2026-03-27 10:00:00.000000000 +0000
Change: 2026-03-27 10:00:00.000000000 +0000
```

The `Access` line shows both the **octal** (`0644`) and **symbolic** (`-rw-r--r--`)
representation. You will learn what the octal numbers mean in the next lesson on
`chmod`.

## Special Permissions (Overview)

Beyond the basic nine bits, Linux has three special permission bits:

| Bit        | Symbol in `ls -l`   | Octal | Purpose                                     |
|------------|---------------------|-------|---------------------------------------------|
| **setuid** | `s` in owner's `x`  | 4000  | File runs as the file's owner, not the caller |
| **setgid** | `s` in group's `x`  | 2000  | File runs as the file's group; on dirs, new files inherit the directory's group |
| **sticky** | `t` in others' `x`  | 1000  | On dirs, only the file owner can delete their own files |

### Common Examples

- `/usr/bin/passwd` has setuid so any user can change their own password:
  ```
  -rwsr-xr-x 1 root root 68208 ... /usr/bin/passwd
  ```
  Notice the `s` replacing the owner's `x`.

- `/tmp` has the sticky bit so users cannot delete each other's files:
  ```
  drwxrwxrwt 20 root root 4096 ... /tmp
  ```
  Notice the `t` replacing the others' `x`.

> **Tip:** If you see an uppercase `S` or `T` instead of `s` or `t`, it means the
> special bit is set but the underlying execute bit is **not** -- this is usually a
> misconfiguration.

## Try It Yourself

1. **List permissions in the lab directory:**
   ```bash
   ls -l ~/permlab/
   ```
   Identify the file type, owner, group, and others permissions for each entry.

2. **Decode the script permissions:**
   Look at `greet.sh`. It should show `-rwxr-xr-x`. Who can execute it?
   Answer: everyone (owner, group, and others all have `x`).

3. **Inspect the restricted directory:**
   ```bash
   ls -l ~/permlab/docs/
   stat ~/permlab/docs/internal.txt
   ```
   What octal permission does `internal.txt` have?

4. **Check the symbolic link:**
   ```bash
   ls -l ~/permlab/link_to_readme
   stat ~/permlab/link_to_readme
   ```
   Notice that symbolic links always show `lrwxrwxrwx`. The actual access is
   determined by the target file's permissions.

5. **Look at /tmp permissions:**
   ```bash
   ls -ld /tmp
   ```
   Can you spot the sticky bit?

## Summary

- The 10-character permission string shows file type + three rwx triplets (owner,
  group, others).
- For **files**: `r` = read contents, `w` = modify, `x` = execute as program.
- For **directories**: `r` = list contents, `w` = create/delete files, `x` = enter
  and access metadata.
- `stat` gives both octal and symbolic permission representations.
- Special bits (setuid, setgid, sticky) add extra security controls.
- Symbolic links always display `lrwxrwxrwx`; effective permissions come from the
  target.
