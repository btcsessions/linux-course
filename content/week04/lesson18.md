---
id: 18
week: 4
title: "Changing Permissions with chmod"
duration_minutes: 15
objectives:
  - "Change file permissions using symbolic mode (u+x, go-w, a=r)"
  - "Change file permissions using octal mode (755, 644)"
  - "Apply permission changes recursively with -R"
commands: [chmod, "chmod +x", "chmod 755", "chmod -R"]
prerequisites: []
sandbox_commands: [chmod, id, groups, whoami, cat, less, grep, ls, cd, pwd, echo, touch, mkdir, cp, head, tail, find, wc, sort, cut, stat, file, clear, date]
sandbox_setup: |
  echo "#!/bin/bash" > myscript.sh
  echo "echo 'Hello World'" >> myscript.sh
  chmod 644 myscript.sh
  echo "Config data" > config.txt
  chmod 666 config.txt
  echo "Secret data" > secret.txt
  chmod 644 secret.txt
  mkdir project
  echo "Project file 1" > project/file1.txt
  echo "Project file 2" > project/file2.txt
  chmod 644 project/file1.txt project/file2.txt
  echo "Practice chmod!" > README.txt
---
# Changing Permissions with chmod

Now that you can read permission strings (Lesson 17), it is time to learn how to
**change** them. The `chmod` (change mode) command is the primary tool for adjusting
file and directory permissions on Linux. This lesson covers two ways to express
permission changes -- symbolic mode and octal mode -- plus recursive operations.

## Symbolic Mode

Symbolic mode lets you describe permission changes in a human-readable way. The
general syntax is:

```bash
chmod WHO OPERATOR PERMISSION file
```

### WHO -- Which Triplet to Modify

| Letter | Meaning                        |
|--------|--------------------------------|
| `u`    | User (the file's owner)        |
| `g`    | Group                          |
| `o`    | Others (everyone else)         |
| `a`    | All (equivalent to `ugo`)      |

### OPERATOR -- What to Do

| Operator | Meaning                         |
|----------|---------------------------------|
| `+`      | Add the permission              |
| `-`      | Remove the permission           |
| `=`      | Set exactly these permissions   |

### PERMISSION -- Which Bits

| Letter | Meaning  |
|--------|----------|
| `r`    | Read     |
| `w`    | Write    |
| `x`    | Execute  |

### Examples

Make a script executable for the owner:

```bash
chmod u+x deploy.sh
```

Remove write permission for group and others:

```bash
chmod go-w app.conf
```

Give everyone read permission and nothing else:

```bash
chmod a=r README
```

Add read and execute for the group:

```bash
chmod g+rx deploy.sh
```

You can combine multiple changes with a comma:

```bash
chmod u+x,go-w deploy.sh
```

> **Tip:** When you download or create a shell script, it usually does not have the
> execute bit set. The quick shorthand `chmod +x script.sh` is equivalent to
> `chmod a+x script.sh` and is one of the most common commands you will ever type.

## Octal (Numeric) Mode

Octal mode represents all nine permission bits as a three-digit number. Each digit
corresponds to one triplet (owner, group, others) and is calculated by adding the
values of the permissions you want:

| Permission | Value |
|------------|-------|
| Read (r)   | 4     |
| Write (w)  | 2     |
| Execute (x)| 1     |
| None       | 0     |

### Building an Octal Number

To figure out the octal digit for a triplet, add up the values:

```
rwx = 4 + 2 + 1 = 7
rw- = 4 + 2 + 0 = 6
r-x = 4 + 0 + 1 = 5
r-- = 4 + 0 + 0 = 4
--- = 0 + 0 + 0 = 0
```

Then combine three digits, one for each triplet:

```
Owner  Group  Others
  7      5      5     = 755
```

### Common Octal Patterns

| Octal | Symbolic     | Typical Use                            |
|-------|-------------|----------------------------------------|
| `755` | `rwxr-xr-x` | Executable files, directories          |
| `644` | `rw-r--r--` | Regular files (configs, documents)     |
| `700` | `rwx------` | Private directories or scripts         |
| `600` | `rw-------` | Private files (SSH keys, secrets)      |
| `750` | `rwxr-x---` | Shared directories for a group         |
| `664` | `rw-rw-r--` | Files shared with a group              |

### Examples

```bash
chmod 755 deploy.sh
```

This sets the permissions to `rwxr-xr-x`: owner can do everything, group and others
can read and execute.

```bash
chmod 600 secrets.env
```

This restricts the file to `rw-------`: only the owner can read or write it.

```bash
chmod 644 app.conf
```

Standard read-write for the owner, read-only for everyone else.

> **Tip:** When in doubt, use `644` for regular files and `755` for directories and
> executables. These are sensible defaults on most Linux systems.

## Octal vs. Symbolic -- When to Use Which

| Situation                                  | Recommended Mode |
|--------------------------------------------|-----------------|
| Setting all permissions from scratch        | Octal           |
| Adding or removing a single bit             | Symbolic        |
| Scripts that need to be portable and clear   | Octal           |
| Quick one-off adjustments                    | Symbolic        |

Octal mode replaces **all** permission bits at once. Symbolic mode modifies only what
you specify, leaving the rest unchanged.

```bash
# These are NOT equivalent:
chmod 755 file.sh    # Sets exact permissions: rwxr-xr-x
chmod u+x file.sh    # Adds x for owner only, leaves everything else as-is
```

## Recursive Changes with `-R`

The `-R` (recursive) flag applies permission changes to a directory and everything
inside it:

```bash
chmod -R 755 ~/chmodlab/project/
```

This sets `755` on the directory itself **and** every file and subdirectory within it.

> **Warning:** Be careful with recursive chmod. Applying `755` recursively is
> generally safe, but applying `777` recursively is almost always a mistake -- it
> makes everything readable, writable, and executable by everyone. Also, blindly
> applying the same permissions to files and directories can cause problems since
> directories typically need the execute bit while data files do not.

### A Safer Recursive Approach

If you want directories to be `755` and files to be `644`, use `find` with `chmod`:

```bash
find ~/chmodlab/project -type d -exec chmod 755 {} \;
find ~/chmodlab/project -type f -exec chmod 644 {} \;
```

This is a common pattern in web server deployments and shared project directories.

## Verifying Your Changes

Always verify permission changes with `ls -l` or `stat`:

```bash
ls -l deploy.sh
stat deploy.sh
```

The `stat` command shows both the octal and symbolic representations, which is
especially helpful when learning:

```
Access: (0755/-rwxr-xr-x)  Uid: (1000/   alex)   Gid: (1000/   alex)
```

## Common Mistakes

1. **Forgetting `+x` on scripts:** You write a script, try to run it, and get
   "Permission denied". Solution: `chmod +x script.sh`.

2. **Using `777` everywhere:** This removes all security. Never use `777` unless you
   have a very specific reason and understand the consequences.

3. **Recursive chmod on `/`:** Running `chmod -R` on the root directory will break
   your system. Always double-check the path before pressing Enter.

4. **Confusing symbolic and octal:** `chmod 644` and `chmod u=rw,go=r` do the same
   thing, but mixing them up in your head leads to errors. Pick one for each task.

## CachyOS Notes

CachyOS follows standard Arch Linux permission conventions. The default umask
(typically `022`) means newly created files get `644` and directories get `755`. You
can check your current umask with:

```bash
umask
```

The umask subtracts permissions from the maximum (`666` for files, `777` for
directories). A umask of `022` removes write from group and others.

## Try It Yourself

1. **Make a script executable:**
   ```bash
   ls -l ~/chmodlab/deploy.sh
   chmod u+x ~/chmodlab/deploy.sh
   ls -l ~/chmodlab/deploy.sh
   ```
   Notice the `x` appearing in the owner triplet.

2. **Lock down a secrets file:**
   ```bash
   chmod 600 ~/chmodlab/secrets.env
   ls -l ~/chmodlab/secrets.env
   ```
   Confirm only the owner has read and write access.

3. **Set exact permissions with octal mode:**
   ```bash
   chmod 755 ~/chmodlab/deploy.sh
   stat ~/chmodlab/deploy.sh
   ```

4. **Fix the project directory recursively:**
   ```bash
   ls -l ~/chmodlab/project/
   chmod -R 644 ~/chmodlab/project/
   ls -l ~/chmodlab/project/
   ```
   What happened to the directory's execute bit? Try `cd ~/chmodlab/project/`.

5. **Restore proper directory permissions:**
   ```bash
   chmod 755 ~/chmodlab/project
   ls -ld ~/chmodlab/project
   ```

## Summary

- `chmod` changes file and directory permissions using symbolic or octal notation.
- **Symbolic mode** (`u+x`, `go-w`, `a=r`) modifies specific bits and is best for
  quick adjustments.
- **Octal mode** (`755`, `644`, `600`) sets all bits at once and is best for explicit,
  predictable results.
- Use `-R` for recursive changes, but be cautious -- directories and files often need
  different permissions.
- Always verify changes with `ls -l` or `stat`.
- The default umask on CachyOS (`022`) gives files `644` and directories `755`.
