---
id: 31
week: 7
title: "pacman -- Installing and Removing Packages"
duration_minutes: 15
objectives:
  - "Search for packages in the repositories with pacman -Ss"
  - "Install and remove packages cleanly with pacman -S and pacman -Rs"
  - "Query installed packages and their files with pacman -Q operations"
  - "Understand dependency handling and CachyOS-specific repositories"
commands: [pacman -S, pacman -Rs, pacman -Ss, pacman -Qi, pacman -Ql, pacman -Syu]
prerequisites: []
sandbox_commands: [cat, ls, grep, echo, head, tail, wc, sort, cd, pwd, find, less, whoami, date, clear, sed, awk, cut]
sandbox_setup: |
  echo "pacman commands must be run in your real terminal (not sandbox)." > README.txt
  echo "" >> README.txt
  echo "Try these commands in your CachyOS terminal:" >> README.txt
  echo "  pacman -Ss firefox    # search for packages" >> README.txt
  echo "  pacman -Qi bash       # info about installed package" >> README.txt
  echo "  pacman -Ql coreutils  # list files in a package" >> README.txt
  echo "" >> README.txt
  echo "Sample pacman -Qi output:" > sample_pacman_output.txt
  echo "Name            : bash" >> sample_pacman_output.txt
  echo "Version         : 5.2.026-2" >> sample_pacman_output.txt
  echo "Description     : The GNU Bourne Again shell" >> sample_pacman_output.txt
  echo "Architecture    : x86_64" >> sample_pacman_output.txt
  echo "Installed Size  : 8.30 MiB" >> sample_pacman_output.txt
  echo "Depends On      : readline  glibc  ncurses" >> sample_pacman_output.txt
---

# pacman -- Installing and Removing Packages

## The Arch Package Manager

CachyOS is built on top of Arch Linux, and it inherits one of the most powerful
and straightforward package managers in the Linux world: **pacman**. Unlike
`apt` on Debian/Ubuntu or `dnf` on Fedora, pacman uses a single short command
with uppercase flag letters to perform every package operation.

If you have never used a command-line package manager before, think of it like
an app store that you control entirely from the terminal -- no mouse clicking
required.

## How pacman Is Organized

pacman operations are grouped by a capital letter flag:

| Flag | Meaning              | Example                     |
|------|----------------------|-----------------------------|
| `-S` | **Sync** (install)   | `pacman -S firefox`         |
| `-R` | **Remove**           | `pacman -R firefox`         |
| `-Q` | **Query** (local)    | `pacman -Q`                 |
| `-U` | **Upgrade** (local)  | `pacman -U package.pkg.tar.zst` |
| `-F` | **Files** (search)   | `pacman -F libssl.so`       |

These capital letters are always the *first* flag after `pacman`. Additional
lowercase letters modify the behavior.

## Searching for Packages

Before you install anything, you will usually want to search for it:

```bash
pacman -Ss firefox
```

This searches the **sync database** -- the remote repositories your system
knows about. The output looks something like:

```
extra/firefox 125.0-1
    Standalone web browser from mozilla.org
cachyos/firefox 125.0-1.1
    Standalone web browser from mozilla.org (CachyOS optimized)
```

Notice that CachyOS often provides its own optimized builds in the `cachyos`
repository, compiled with performance flags specific to modern CPUs.

To search only among packages you have already installed:

```bash
pacman -Qs firefox
```

## Installing Packages

To install a package, use `-S` (sync):

```bash
sudo pacman -S firefox
```

**Why sudo?** Installing software modifies system directories like `/usr/bin`
and `/usr/lib`. Only the root user can do this. `sudo` lets you run a single
command with root privileges.

pacman will show you what it plans to install, including any **dependencies** --
other packages that the one you want needs in order to work:

```
resolving dependencies...
looking for conflicting packages...

Packages (3) dav1d-1.4.1-1  libvpx-1.14.0-1  firefox-125.0-1

Total Installed Size:  238.42 MiB

:: Proceed with installation? [Y/n]
```

Press **Enter** (or type `Y`) to confirm. Type `n` to cancel.

### Installing Multiple Packages at Once

You can list several packages in a single command:

```bash
sudo pacman -S git vim htop
```

This is faster than installing them one at a time because pacman only resolves
dependencies once.

## Removing Packages

The basic removal command is:

```bash
sudo pacman -R firefox
```

However, this leaves behind any dependencies that were installed *only* for
that package. A cleaner approach:

```bash
sudo pacman -Rs firefox
```

The lowercase `s` tells pacman to also remove dependencies that are no longer
needed by any other installed package.

**Warning:** Never use `pacman -Rdd` unless you truly know what you are doing.
The `-dd` flag skips dependency checks entirely and can break your system by
removing packages that other software relies on.

### Removing Configuration Files Too

Some packages leave behind configuration files after removal. To remove
everything:

```bash
sudo pacman -Rns firefox
```

The `n` flag removes backup configuration files that pacman would otherwise
keep.

## Querying Installed Packages

The `-Q` family lets you inspect what is on your system.

### List All Installed Packages

```bash
pacman -Q
```

This can be a long list. Pipe it to `less` or `wc -l` for a count:

```bash
pacman -Q | wc -l
```

### Get Detailed Info About a Package

```bash
pacman -Qi firefox
```

This displays the package name, version, description, architecture, URL,
licenses, install size, dependencies, and more.

### List Files Owned by a Package

```bash
pacman -Ql firefox
```

This prints every file that the `firefox` package installed on your system.
Useful when you want to know where a config file or binary ended up.

### Find Which Package Owns a File

```bash
pacman -Qo /usr/bin/git
```

Output: `/usr/bin/git is owned by git 2.45.0-1`

### List Explicitly Installed Packages

```bash
pacman -Qe
```

These are packages you (or the system installer) chose to install, as opposed
to packages pulled in automatically as dependencies.

### List Orphan Packages

```bash
pacman -Qdt
```

Orphans are packages that were installed as dependencies but are no longer
required by anything. You can clean them up:

```bash
sudo pacman -Rns $(pacman -Qdtq)
```

## Remote Package Info

To get details about a package in the repos (not yet installed):

```bash
pacman -Si firefox
```

This is the remote equivalent of `-Qi`.

## CachyOS Repositories

CachyOS extends the standard Arch repositories with its own:

- **cachyos** -- optimized packages built with x86-64-v3 or x86-64-v4
  instruction sets for better performance on modern CPUs.
- **cachyos-extra** -- additional CachyOS-specific tools and themes.

These repos are configured in `/etc/pacman.conf`. The CachyOS keyring
(`cachyos-keyring`) and mirrorlist (`cachyos-mirrorlist`) packages ensure your
system trusts and can reach these repositories.

You can see which repos are enabled:

```bash
grep -E '^\[' /etc/pacman.conf
```

**Tip:** Never remove `cachyos-keyring` or `cachyos-mirrorlist`. Without them,
pacman cannot verify or download CachyOS packages.

## Refreshing the Package Database

Before installing or searching, it is good practice to refresh the database so
you have the latest package lists:

```bash
sudo pacman -Sy
```

However, **never install packages after only `-Sy`** without also upgrading.
This can cause partial upgrade problems on a rolling release. The correct
approach is:

```bash
sudo pacman -Syu
```

This refreshes the database (`-y`) and upgrades all packages (`-u`) in one
step. We cover this in more detail in the next lesson.

## Try It Yourself

1. Search for the `htop` package in the repositories:
   ```bash
   pacman -Ss htop
   ```

2. Check if `htop` is already installed on your system:
   ```bash
   pacman -Qs htop
   ```

3. Get detailed information about an installed package (try `bash`):
   ```bash
   pacman -Qi bash
   ```

4. List all files installed by the `coreutils` package:
   ```bash
   pacman -Ql coreutils | head -20
   ```

5. Count how many packages are installed on your system:
   ```bash
   pacman -Q | wc -l
   ```

6. Find which package owns the `ls` command:
   ```bash
   pacman -Qo /usr/bin/ls
   ```

## Summary

| Task                          | Command                        |
|-------------------------------|--------------------------------|
| Search repos                  | `pacman -Ss <term>`            |
| Install a package             | `sudo pacman -S <pkg>`         |
| Remove + unused deps          | `sudo pacman -Rs <pkg>`        |
| Query installed               | `pacman -Q`                    |
| Package info (installed)      | `pacman -Qi <pkg>`             |
| Package info (remote)         | `pacman -Si <pkg>`             |
| List package files            | `pacman -Ql <pkg>`             |
| Find file owner               | `pacman -Qo <path>`            |
| Remove orphans                | `sudo pacman -Rns $(pacman -Qdtq)` |
