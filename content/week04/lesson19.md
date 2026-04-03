---
id: 19
week: 4
title: "Ownership with chown and chgrp"
duration_minutes: 15
objectives:
  - "Change file ownership with chown"
  - "Change group ownership with chgrp or chown :group"
  - "Understand why changing ownership requires sudo"
commands: [chown, "chown user:group", chgrp, "chown -R"]
prerequisites: []
sandbox_commands: [chown, chgrp, chmod, id, groups, whoami, cat, less, grep, ls, cd, pwd, echo, touch, mkdir, cp, head, tail, find, wc, sort, cut, stat, file, clear, date]
sandbox_setup: |
  echo "File to change ownership" > myfile.txt
  echo "Another file" > another.txt
  mkdir mydir
  echo "Dir content" > mydir/content.txt
  echo "Note: chown requires root privileges." > README.txt
  echo "You can see current ownership with ls -l" >> README.txt
---
# Ownership with chown and chgrp

Every file and directory on a Linux system has two ownership attributes: a **user**
(owner) and a **group**. In the previous lessons you learned how to read and change
permissions. This lesson focuses on changing **who** those permissions apply to. The
commands `chown` and `chgrp` let you reassign ownership, and understanding when and
why to use them is an essential sysadmin skill.

## Why Ownership Matters

Recall the permission triplets from Lesson 17: owner, group, others. The permission
bits only matter in the context of **who owns the file**. Consider a file with
permissions `rw-r-----`:

- If **you** own the file, you get `rw-` (read and write).
- If you are in the file's **group** but not the owner, you get `r--` (read only).
- If you are **neither**, you get `---` (no access).

Changing ownership can grant or revoke access without touching a single permission
bit.

## Viewing Ownership

You already know how to see ownership:

```bash
ls -l ~/ownlab/
```

Output:

```
-rw-r--r-- 1 alex alex 17 Mar 27 10:00 index.html
-rw-r--r-- 1 alex alex 16 Mar 27 10:00 app.log
-rw-r--r-- 1 alex alex 16 Mar 27 10:00 db.conf
drwxr-xr-x 2 alex alex 4096 Mar 27 10:00 shared
```

The third and fourth columns show the **owner** and **group** respectively. You can
also use `stat`:

```bash
stat ~/ownlab/index.html
```

Look for the `Uid` and `Gid` fields in the output.

## Changing the Owner with `chown`

The `chown` (change owner) command sets the user who owns a file:

```bash
sudo chown www-data index.html
```

After this, `www-data` is the owner. The group remains unchanged.

### Syntax

```
chown [OPTIONS] NEW_OWNER FILE...
```

You can specify the owner by username or by numeric UID:

```bash
sudo chown 33 index.html    # UID 33 (often www-data)
sudo chown alex index.html   # by username
```

## Changing the Group with `chgrp`

The `chgrp` (change group) command changes only the group ownership:

```bash
sudo chgrp developers db.conf
```

### Syntax

```
chgrp [OPTIONS] NEW_GROUP FILE...
```

Like `chown`, you can use a group name or numeric GID:

```bash
sudo chgrp 1001 db.conf   # by GID
```

> **Tip:** You can change a file's group to any group you belong to **without**
> `sudo`. But changing it to a group you are not a member of requires root privileges.

## Changing Both Owner and Group with `chown`

The most efficient way to change both at once is `chown` with a colon separator:

```bash
sudo chown www-data:www-data index.html
```

This sets the owner to `www-data` and the group to `www-data` in a single command.

### Variations

```bash
sudo chown user:group file    # Change both owner and group
sudo chown user: file         # Change owner; set group to user's login group
sudo chown user file          # Change owner only
sudo chown :group file        # Change group only (same as chgrp)
```

The `:group` form is a convenient alternative to `chgrp`:

```bash
sudo chown :developers db.conf
```

> **Tip:** Some older documentation uses a dot (`.`) instead of a colon, like
> `chown user.group file`. The colon is the modern and preferred separator. The dot
> form is ambiguous when usernames contain dots.

## Why `sudo` Is Required

On Linux, only root can change file ownership. This is a deliberate security
restriction:

1. **Preventing quota evasion:** Without this restriction, a user could create a
   large file and then `chown` it to someone else, consuming their disk quota.

2. **Preventing privilege escalation:** If you could give a file to root and set the
   setuid bit, you could create a program that runs as root.

3. **Maintaining accountability:** File ownership tracks who is responsible for a
   file. Allowing arbitrary changes would undermine auditing.

As a result, nearly every `chown` command you run will start with `sudo`:

```bash
sudo chown newowner file
```

The exception is `chgrp` (or `chown :group`) when the target group is one you already
belong to.

## Recursive Ownership Changes with `-R`

Like `chmod`, both `chown` and `chgrp` support the `-R` flag for recursive
operations:

```bash
sudo chown -R www-data:www-data /var/www/html/
```

This changes the owner and group of the directory and everything inside it.

```bash
sudo chgrp -R developers ~/ownlab/shared/
```

This changes only the group, recursively.

> **Warning:** Double-check your path before running recursive `chown` or `chgrp`.
> Running `sudo chown -R` on the wrong directory (especially system directories like
> `/etc` or `/`) can break your system in ways that are difficult to recover from.

## Practical Scenarios

### Scenario 1: Web Server Files

A web server (like nginx) runs as the `http` user on CachyOS. To let it read your
site files:

```bash
sudo chown -R http:http /srv/http/mysite/
```

### Scenario 2: Shared Team Directory

You have a project directory that should be accessible to everyone in the
`developers` group:

```bash
sudo chown -R :developers /home/shared/project/
sudo chmod -R 770 /home/shared/project/
```

Now only the owner and `developers` group members can access the files.

### Scenario 3: Reclaiming Ownership After Sudo Operations

Sometimes you create files with `sudo` and they end up owned by root:

```bash
sudo touch /home/alex/config.yaml
ls -l /home/alex/config.yaml
# -rw-r--r-- 1 root root 0 ... config.yaml
```

Reclaim them:

```bash
sudo chown alex:alex /home/alex/config.yaml
```

This is a very common real-world task, especially after running `sudo` commands that
produce output files in your home directory.

### Scenario 4: Fixing Permissions After Extracting an Archive

Archives sometimes preserve the original owner's UID, which may not exist on your
system:

```bash
sudo chown -R $(whoami):$(whoami) ~/extracted-project/
```

The `$(whoami)` substitution fills in your current username automatically.

## Checking Group Memberships

Before assigning group ownership, confirm the group exists and see who belongs to it:

```bash
getent group developers
```

Or check your own groups:

```bash
groups
id
```

To see all groups on the system:

```bash
cat /etc/group
```

## Try It Yourself

1. **View current ownership:**
   ```bash
   ls -l ~/ownlab/
   ```

2. **Change the group of a file (if you have a second group):**
   ```bash
   id
   sudo chgrp wheel ~/ownlab/db.conf
   ls -l ~/ownlab/db.conf
   ```

3. **Change owner and group at once:**
   ```bash
   sudo chown root:root ~/ownlab/app.log
   ls -l ~/ownlab/app.log
   ```

4. **Reclaim the file:**
   ```bash
   sudo chown $(whoami):$(whoami) ~/ownlab/app.log
   ls -l ~/ownlab/app.log
   ```

5. **Recursive group change:**
   ```bash
   sudo chgrp -R wheel ~/ownlab/shared/
   ls -l ~/ownlab/shared/
   ```

6. **Verify with stat:**
   ```bash
   stat ~/ownlab/index.html
   ```

## Summary

- Every file has an **owner** (user) and a **group**. These determine which permission
  triplet applies to each user.
- `chown owner file` changes the file's owner. `chown owner:group file` changes both.
- `chgrp group file` changes the group. Alternatively, use `chown :group file`.
- Changing ownership requires `sudo` (except when changing to a group you belong to
  with `chgrp`).
- Use `-R` for recursive changes, but always verify the path first.
- Common use cases include web server setup, shared team directories, and reclaiming
  files created under `sudo`.
