---
id: 32
week: 7
title: "System Updates and the AUR"
duration_minutes: 15
objectives:
  - "Perform a full system update with pacman -Syu and understand rolling releases"
  - "Understand the AUR and use AUR helpers like paru to search and install AUR packages"
  - "Clean the package cache with paccache and pacman -Sc"
commands: [pacman -Syu, paru -S, paru -Ss, paccache -r, pacman -Sc]
prerequisites: []
sandbox_commands: [pacman -Syu, paru -Ss, paccache -h]
sandbox_setup: |
  # Sandbox for safe exploration of update commands
  echo "sandbox: update commands are available in read-only mode"
---

# System Updates and the AUR

## Rolling Release: What It Means

CachyOS follows the Arch Linux **rolling release** model. This means there are
no version numbers and no big upgrade events like "Ubuntu 24.04 to 26.04."
Instead, every package is updated individually as new versions become
available. Your system is always on the latest version of everything.

This has two important consequences:

1. **You get new software quickly.** When Firefox releases a new version, it
   appears in the repos within days (or hours), not months.
2. **You need to update regularly.** Letting a rolling release system go months
   without updates can make the next update painful, because hundreds of
   packages may need to upgrade at once with interrelated changes.

A good habit is to update at least once a week.

## The Full System Update

The single most important command on any Arch-based system:

```bash
sudo pacman -Syu
```

Let's break down what each flag does:

| Flag | Meaning                                    |
|------|--------------------------------------------|
| `-S` | Sync -- work with the remote repositories  |
| `-y` | Refresh the local copy of the package database |
| `-u` | Upgrade all packages that have newer versions  |

When you run this, pacman will:

1. Download the latest package lists from each repository.
2. Compare every installed package against the latest available version.
3. Show you a summary of what will be upgraded, with download sizes.
4. Ask for confirmation before proceeding.

```
:: Synchronizing package databases...
 cachyos is up to date
 core is up to date
 extra is up to date
:: Starting full system upgrade...
resolving dependencies...

Packages (14) base-24-1  linux-cachyos-6.9.1-2  mesa-24.1.0-1 ...

Total Download Size:   142.36 MiB
Total Installed Size:  487.12 MiB
Net Upgrade Size:        8.44 MiB

:: Proceed with installation? [Y/n]
```

**Tip:** Read the output before pressing Y. Occasionally pacman will warn you
about package replacements or conflicts that need your attention.

## Partial Upgrades: The Cardinal Sin

On a rolling release system, **never** do this:

```bash
# WRONG -- do not do this
sudo pacman -Sy
sudo pacman -S firefox
```

Syncing the database (`-Sy`) without upgrading (`-u`) means your database knows
about newer versions, but your installed libraries are still old. Installing a
new package built against those newer libraries can fail or cause crashes.

The safe pattern is always:

```bash
sudo pacman -Syu          # upgrade everything first
sudo pacman -S firefox    # then install new packages
```

Or combine them:

```bash
sudo pacman -Syu firefox
```

This syncs, upgrades, and installs `firefox` all in one step.

## Handling Update Issues

### Keyring errors

If you see messages about unknown trust or invalid signatures:

```bash
sudo pacman -S archlinux-keyring cachyos-keyring
sudo pacman -Syu
```

Updating the keyrings first ensures pacman trusts all current package signers.

### File conflicts

Sometimes an update fails because two packages try to install the same file.
Read the error message carefully -- it usually names the conflicting packages.
A common fix:

```bash
sudo pacman -Syu --overwrite '/path/to/conflicting/file'
```

**Warning:** Only use `--overwrite` when you understand the conflict. Blindly
overwriting files can break things.

### Pacnew files

When a package updates a configuration file that you have modified, pacman
saves the new version with a `.pacnew` extension instead of overwriting yours.
After an update, check for these:

```bash
find /etc -name "*.pacnew" 2>/dev/null
```

Compare your current file with the `.pacnew` version and merge changes:

```bash
diff /etc/some.conf /etc/some.conf.pacnew
```

## The AUR: Arch User Repository

The official repositories contain thousands of packages, but there is far more
software in the world. The **Arch User Repository** (AUR) fills the gap.

The AUR is a community-driven collection of **build scripts** (called
PKGBUILDs) for software that is not in the official repos. These are not
precompiled packages -- they are instructions for building the software on your
machine.

Key facts about the AUR:

- Anyone with an Arch account can submit a PKGBUILD.
- Packages are **not** officially supported or vetted by Arch developers.
- You should **read the PKGBUILD** before installing an AUR package to make
  sure it is not doing anything malicious.
- AUR packages are built from source on your machine (some download prebuilt
  binaries, but most compile).

## AUR Helpers: paru

You *can* build AUR packages manually with `makepkg`, but AUR helpers automate
the process. CachyOS ships with **paru** as its recommended AUR helper.

paru wraps pacman, so it can do everything pacman does *plus* handle AUR
packages. Its flags mirror pacman's:

### Searching the AUR

```bash
paru -Ss spotify
```

This searches **both** the official repos and the AUR. AUR results appear with
an `aur/` prefix:

```
aur/spotify 1.2.36.1060-1 (+3254 2.87)
    A proprietary music streaming service
```

The numbers in parentheses are the vote count and popularity score -- higher
is generally better.

### Installing from the AUR

```bash
paru -S spotify
```

paru will:

1. Download the PKGBUILD and related files from the AUR.
2. Show you the PKGBUILD for review (press **q** to close the viewer).
3. Resolve dependencies (installing official repo deps with pacman).
4. Compile the software on your machine.
5. Install the resulting package.

**Tip:** The first time you run paru, it may ask you to review the PKGBUILD.
Always take a quick look -- check for any `curl` or `wget` commands downloading
from suspicious URLs.

### Updating AUR packages

```bash
paru -Syu
```

When run through paru, `-Syu` updates both official repo packages **and** AUR
packages. This is one of the main advantages of using an AUR helper.

### Searching installed AUR packages

```bash
paru -Qm
```

The `-Qm` flag lists packages not found in any sync database -- these are
typically AUR packages (or packages you built manually).

## Cleaning the Package Cache

Every time pacman downloads a package, it saves the file in
`/var/cache/pacman/pkg/`. Over time, this cache can grow to many gigabytes.

### Check cache size

```bash
du -sh /var/cache/pacman/pkg/
```

### Clean with paccache

The `paccache` tool (from the `pacman-contrib` package) gives you fine-grained
control. By default it keeps the three most recent versions of each package:

```bash
sudo paccache -r
```

To keep only one version:

```bash
sudo paccache -rk1
```

To do a dry run (see what *would* be deleted):

```bash
paccache -d
```

### Clean with pacman

pacman's built-in cache cleaning removes packages that are no longer installed:

```bash
sudo pacman -Sc
```

To remove *all* cached packages (use with caution):

```bash
sudo pacman -Scc
```

**Warning:** After running `pacman -Scc`, you cannot downgrade packages without
re-downloading them. Keep at least one or two versions with `paccache` instead.

## Downgrading Packages

If an update breaks something, you can downgrade to a previous version from the
cache:

```bash
sudo pacman -U /var/cache/pacman/pkg/firefox-124.0-1-x86_64.pkg.tar.zst
```

The `-U` flag installs a local package file. Tab completion works here to help
you find the right file.

## Setting Up Automatic Cache Cleaning

You can create a pacman hook to run paccache after every upgrade. CachyOS may
already include this, but if not:

```bash
sudo mkdir -p /etc/pacman.d/hooks
```

Create `/etc/pacman.d/hooks/clean_cache.hook`:

```ini
[Trigger]
Operation = Upgrade
Operation = Install
Operation = Remove
Type = Package
Target = *

[Action]
Description = Cleaning pacman cache...
When = PostTransaction
Exec = /usr/bin/paccache -r
```

## Quick Reference

| Task                            | Command                          |
|---------------------------------|----------------------------------|
| Full system update              | `sudo pacman -Syu`               |
| Update + install a package      | `sudo pacman -Syu pkg`           |
| Search AUR and repos            | `paru -Ss term`                  |
| Install from AUR                | `paru -S pkg`                    |
| Update everything (incl. AUR)   | `paru -Syu`                      |
| List AUR/foreign packages       | `paru -Qm`                       |
| Clean cache (keep 3 versions)   | `sudo paccache -r`               |
| Clean cache (keep 1 version)    | `sudo paccache -rk1`             |
| Remove uninstalled from cache   | `sudo pacman -Sc`                |
| Downgrade from cache            | `sudo pacman -U /var/cache/...`  |

## Try It Yourself

1. Check how many packages on your system are due for an upgrade:
   ```bash
   pacman -Qu
   ```
   (This queries upgradeable packages without actually upgrading.)

2. Run a full system update:
   ```bash
   sudo pacman -Syu
   ```

3. Check the size of your package cache:
   ```bash
   du -sh /var/cache/pacman/pkg/
   ```

4. Do a dry run of paccache to see what would be cleaned:
   ```bash
   paccache -d
   ```

5. Search for an AUR package you are curious about:
   ```bash
   paru -Ss visual-studio-code-bin
   ```

6. List all foreign (AUR) packages on your system:
   ```bash
   paru -Qm
   ```

7. Check for any `.pacnew` files that need attention:
   ```bash
   find /etc -name "*.pacnew" 2>/dev/null
   ```
