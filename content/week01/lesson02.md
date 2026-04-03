---
id: 2
week: 1
title: "Where Am I? -- pwd and the Filesystem Tree"
duration_minutes: 15
objectives:
  - "Understand the Linux filesystem hierarchy and its major directories"
  - "Use the pwd command to display the current working directory"
  - "Distinguish between absolute paths and relative paths"
commands: [pwd, ls]
prerequisites: [1]
sandbox_commands: [pwd, ls, whoami, hostname, date, cal, clear, echo, cd]
sandbox_setup: |
  mkdir -p home/user/documents home/user/pictures home/user/downloads
  mkdir -p etc var/log tmp usr/bin
  echo "Sample config" > etc/config.conf
  echo "System log entry 1" > var/log/syslog
  echo "Hello world" > home/user/documents/readme.txt
  echo "My photo list" > home/user/pictures/list.txt
  echo "Downloaded file" > home/user/downloads/file.zip
  echo "Welcome" > welcome.txt
---

# Where Am I? -- pwd and the Filesystem Tree

## Everything Is a File

One of the foundational ideas in Linux is that **everything is a file**. Your
documents are files. Your directories (folders) are files. Even hardware devices
like your keyboard, your hard drive, and your network card are represented as
special files somewhere in the system.

All of these files live inside a single, unified tree structure called the
**filesystem hierarchy**. Understanding this tree is the first step toward
navigating your system with confidence.

## The Filesystem Tree

On Windows you have drive letters: `C:\`, `D:\`, and so on. Linux does it
differently. There is exactly **one root**, and it is simply `/` (a single
forward slash). Everything branches out from there.

Here is a simplified view of the top of the tree:

```
/
├── bin        -> essential command binaries
├── boot       -> bootloader and kernel files
├── dev        -> device files
├── etc        -> system configuration files
├── home       -> user home directories
│   ├── alex
│   └── maria
├── lib        -> shared libraries
├── mnt        -> temporary mount points
├── opt        -> optional/third-party software
├── proc       -> virtual filesystem for process info
├── root       -> home directory for the root user
├── run        -> runtime data
├── srv        -> data for services (web servers, etc.)
├── sys        -> virtual filesystem for hardware info
├── tmp        -> temporary files (cleared on reboot)
├── usr        -> user system resources (programs, docs)
│   ├── bin
│   ├── lib
│   └── share
└── var        -> variable data (logs, caches, mail)
    ├── log
    └── cache
```

You do not need to memorize all of these right now. Here are the ones that
matter most to you as a beginner:

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `/`       | The root of the entire filesystem. Everything lives under here. |
| `/home`   | Contains a subdirectory for each regular user. Your files live here. |
| `/etc`    | System-wide configuration files. Think "**et cetera**" or "**edit to configure**." |
| `/usr`    | Programs, libraries, and documentation installed by the package manager. |
| `/var`    | Files that change frequently: logs (`/var/log`), package caches (`/var/cache`). |
| `/tmp`    | Temporary files. Anything here may be deleted when you reboot. |
| `/dev`    | Device files representing hardware (disks, terminals, etc.). |
| `/proc`   | A virtual directory showing running process and kernel information. |

**Tip:** On CachyOS (and Arch Linux in general), `/bin`, `/sbin`, and `/lib` are
symlinks to their counterparts inside `/usr`. So `/bin/ls` and `/usr/bin/ls` are
the same file. This simplifies the system and is called the **merged-usr**
layout.

## Your Home Directory

When you open a terminal, you start in your **home directory**. For a user
named `alex`, that directory is:

```
/home/alex
```

This is *your* personal space. Your documents, downloads, configuration files,
and desktop all live here. The tilde shortcut `~` always refers to your home
directory.

On CachyOS you will typically find directories like `Documents`, `Downloads`,
`Pictures`, `Music`, and `Videos` pre-created inside your home.

## The pwd Command

Now that you know the tree exists, how do you figure out where you are inside
it? Use `pwd`:

```bash
pwd
```

`pwd` stands for **print working directory**. It tells you the full (absolute)
path of the directory you are currently in:

```
/home/alex
```

If you have navigated somewhere else, `pwd` updates accordingly:

```
/var/log
```

**Tip:** You can never get truly "lost" in Linux. Just run `pwd` and you will
immediately know where you are.

## Peeking at the Top of the Tree

You can use `ls /` to see the top-level directories:

```bash
ls /
```

```
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
```

This lists the first level of branches under the root `/`. We will learn more
about `ls` in Lesson 4, but for now just know it lists the contents of a
directory.

## Absolute vs. Relative Paths

This is one of the most important concepts in Linux navigation. There are two
ways to describe the location of any file or directory.

### Absolute Paths

An absolute path starts from the root `/` and spells out the entire route:

```
/home/alex/Documents/report.txt
```

No matter where you currently are in the filesystem, this path always points to
the same file. It is like giving a full street address.

### Relative Paths

A relative path describes a location **relative to where you are right now**.
If your working directory is `/home/alex`, then:

```
Documents/report.txt
```

points to the exact same file as the absolute path above. It is like saying
"two doors down on the left" -- it only makes sense if you know the starting
point.

### How to Tell Them Apart

The rule is simple:

- **Starts with `/`** -> absolute path.
- **Does not start with `/`** -> relative path.

```
/etc/pacman.conf        <- absolute
etc/pacman.conf         <- relative (from wherever you are now)
./etc/pacman.conf       <- also relative (the ./ means "current directory")
```

### Why Does It Matter?

When you tell a command to operate on a file, it needs to know *which* file.
If you use a relative path, the command combines it with your working directory
to find the target. Using the wrong type of path is a common source of "file
not found" errors for beginners.

**Warning:** If you get a "No such file or directory" error, the first thing to
check is whether you are in the directory you think you are. Run `pwd` to
verify.

## Special Path Shortcuts

Linux provides a few handy shortcuts you will use constantly:

| Symbol | Meaning |
|--------|---------|
| `/`    | The root of the filesystem |
| `~`    | Your home directory (`/home/yourname`) |
| `.`    | The current directory |
| `..`   | The parent directory (one level up) |
| `-`    | The previous directory you were in (used with `cd`) |

You will put these to work in the next lesson when you learn `cd`.

## CachyOS-Specific Notes

- CachyOS follows the **Filesystem Hierarchy Standard (FHS)** like most Linux
  distributions, but uses the merged-usr layout where `/bin` is a symlink to
  `/usr/bin`.
- The pacman package database lives in `/var/lib/pacman/`.
- CachyOS-specific configuration files can be found in `/etc/` alongside
  standard Arch configuration.
- The CachyOS kernel and its modules are stored under `/boot` and
  `/usr/lib/modules/`.

## Try It Yourself

1. Open your terminal and run `pwd`. What directory are you in?
2. Run `ls /` to see all the top-level directories. How many are there?
3. Run `ls /home` to see which user accounts have home directories.
4. Run `ls /etc` -- notice how many configuration files are here.
5. Run `ls /tmp` -- is anything in the temporary directory?
6. Identify whether each of the following is an absolute or relative path:
   - `/var/log/pacman.log`
   - `Documents/homework.txt`
   - `./notes.txt`
   - `/home/alex/.bashrc`
7. Run `ls /var/log` to see system log files.
8. Run `echo $HOME` and compare the output with `pwd`. Are they the same?

In the next lesson you will learn how to move around the filesystem tree using
the `cd` command. You will finally stop standing in one place and start
exploring.
