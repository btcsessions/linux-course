---
id: 16
week: 4
title: "Users and Groups"
duration_minutes: 15
objectives:
  - "Understand the Linux user model: root, regular, and system users"
  - "View user and group information with id and groups"
  - "Switch users with su and execute commands as root with sudo"
commands: [id, groups, su, sudo, "cat /etc/passwd", "cat /etc/group", whoami]
prerequisites: []
sandbox_commands: [id, groups, whoami, cat, less, grep]
sandbox_setup: |
  #!/bin/bash
  # Create sample passwd and group files for safe exploration
  cp /etc/passwd ~/sample_passwd
  cp /etc/group ~/sample_group
---
# Users and Groups

Linux is a multi-user operating system. Every process runs as a specific user, and
every file is owned by a specific user and group. Understanding how users and groups
work is foundational to system security and daily administration. This lesson walks
you through the user model on CachyOS and shows you how to inspect and switch
between accounts.

## The Three Types of Users

Linux recognises three broad categories of user accounts:

| Type          | UID Range      | Purpose                                      |
|---------------|----------------|----------------------------------------------|
| **root**      | 0              | The superuser -- unlimited privileges         |
| **System**    | 1 -- 999       | Services like `http`, `dbus`, `systemd-journal` |
| **Regular**   | 1000+          | Human users who log in interactively          |

> **CachyOS note:** CachyOS follows the Arch Linux convention where the first regular
> user created during installation receives UID 1000.

### root -- The Superuser

The `root` account (UID 0) can read, write, and execute any file on the system,
regardless of permissions. Because a single mistake as root can destroy your
installation, you should **never run a regular desktop session as root**. Instead,
use `sudo` to perform individual privileged commands.

### System Users

System users own background services (daemons). They typically have no password and
cannot log in interactively. You will see them listed in `/etc/passwd` with low UIDs
and shells set to `/usr/bin/nologin` or `/bin/false`.

### Regular Users

These are the accounts for people. Each one has a home directory under `/home/`, a
login shell, and a UID of 1000 or above.

## Viewing Your Identity with `id` and `whoami`

The simplest way to check who you are is `whoami`:

```bash
whoami
```

For more detail, use `id`:

```bash
id
```

Sample output:

```
uid=1000(alex) gid=1000(alex) groups=1000(alex),998(wheel),986(video),985(render)
```

This tells you:

- **uid** -- your numeric user ID and username
- **gid** -- your primary group
- **groups** -- every group you belong to

You can also query another user:

```bash
id root
```

## Listing Your Groups with `groups`

The `groups` command is a quick shortcut to see group memberships:

```bash
groups
```

Output might look like:

```
alex wheel video render
```

Check another user's groups:

```bash
groups root
```

## Inside `/etc/passwd`

Every user account is defined in `/etc/passwd`. Each line has seven colon-separated
fields:

```
username:x:UID:GID:comment:home_directory:shell
```

Example line:

```
alex:x:1000:1000:Alex:/home/alex:/bin/bash
```

View the file:

```bash
cat /etc/passwd
```

> **Tip:** Despite the name, `/etc/passwd` does **not** contain passwords. Hashed
> passwords live in `/etc/shadow`, which only root can read.

### Filtering with `grep`

To find a specific user quickly:

```bash
grep alex /etc/passwd
```

## Inside `/etc/group`

Groups are defined in `/etc/group` with four fields:

```
group_name:x:GID:member_list
```

Example:

```
wheel:x:998:alex
```

The `wheel` group is special on CachyOS -- members are allowed to use `sudo`.

View all groups:

```bash
cat /etc/group
```

Find groups for a user:

```bash
grep alex /etc/group
```

## Switching Users with `su`

The `su` (substitute user) command opens a shell as another user:

```bash
su - alex
```

The `-` flag (or `-l` / `--login`) starts a full login shell, loading the target
user's environment. Without it, you inherit the current environment, which often
causes confusion.

To switch to root:

```bash
su -
```

You will be prompted for the **root password**. On CachyOS, the root account may be
locked by default, meaning you should use `sudo` instead.

> **Warning:** Using `su` to become root gives you an unrestricted root shell.
> Prefer `sudo` for individual commands so that each action is logged and you avoid
> accidentally running destructive commands.

## Running Commands as Root with `sudo`

`sudo` (superuser do) lets an authorised user execute a single command as root:

```bash
sudo pacman -Syu
```

After typing your **own** password (not root's), the command runs with root
privileges. `sudo` caches your credentials for a few minutes so you are not prompted
repeatedly.

### Why `sudo` is Preferred over `su`

1. **Least privilege** -- you elevate only when needed.
2. **Audit trail** -- every `sudo` invocation is logged to the journal.
3. **No shared root password** -- each user authenticates with their own password.
4. **Granular control** -- `/etc/sudoers` can limit which commands a user may run.

### Checking `sudo` Access

```bash
sudo -l
```

This lists the commands you are permitted to run via `sudo`.

### The `wheel` Group on CachyOS

On Arch-based systems including CachyOS, adding a user to the `wheel` group and
uncommenting the appropriate line in `/etc/sudoers` (via `visudo`) grants `sudo`
access:

```
%wheel ALL=(ALL:ALL) ALL
```

> **Warning:** Never edit `/etc/sudoers` directly. Always use `sudo visudo`, which
> validates syntax before saving. A broken sudoers file can lock you out of `sudo`
> entirely.

## Try It Yourself

1. **Check your identity:**
   ```bash
   whoami
   id
   ```

2. **List your groups:**
   ```bash
   groups
   ```

3. **Explore the passwd file:**
   ```bash
   cat ~/sample_passwd
   ```
   Count how many users have `/bin/bash` as their shell:
   ```bash
   grep '/bin/bash' ~/sample_passwd
   ```

4. **Look at group definitions:**
   ```bash
   cat ~/sample_group
   ```
   Find the `wheel` group:
   ```bash
   grep wheel ~/sample_group
   ```

5. **Check your sudo privileges:**
   ```bash
   sudo -l
   ```

## Summary

- Linux has three user types: **root** (UID 0), **system** (UID 1--999), and
  **regular** (UID 1000+).
- `id` and `groups` show your UID, GID, and group memberships.
- `/etc/passwd` defines user accounts; `/etc/group` defines groups.
- `su -` switches to another user's login shell (requires their password).
- `sudo` runs a single command as root using **your** password -- prefer it over `su`.
- On CachyOS, membership in the `wheel` group grants `sudo` access.
