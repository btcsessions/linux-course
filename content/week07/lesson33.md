---
id: 33
week: 7
title: "Disk and Storage"
duration_minutes: 15
objectives:
  - "Check disk usage and free space with df and du"
  - "Understand mount points, block devices, and how to use lsblk"
  - "Monitor disk health and find large files consuming space"
commands: [df -h, du -sh, du -sh *, lsblk, mount, findmnt]
prerequisites: []
sandbox_commands: [df -h, du -sh, lsblk, findmnt, mount]
sandbox_setup: |
  # Create sample directory structure for du exploration
  mkdir -p /tmp/disklab/logs /tmp/disklab/data /tmp/disklab/cache
  dd if=/dev/zero of=/tmp/disklab/logs/app.log bs=1K count=512 2>/dev/null
  dd if=/dev/zero of=/tmp/disklab/data/records.db bs=1K count=2048 2>/dev/null
  dd if=/dev/zero of=/tmp/disklab/cache/thumb1.jpg bs=1K count=128 2>/dev/null
  dd if=/dev/zero of=/tmp/disklab/cache/thumb2.jpg bs=1K count=256 2>/dev/null
  echo "Disk lab ready in /tmp/disklab"
---

# Disk and Storage

## Why Disk Management Matters

One of the most common problems on any computer is running out of disk space.
On a Linux system this can cause log files to stop writing, package installs to
fail, and in severe cases the system may refuse to boot properly. Knowing how
to check your disk usage, find space hogs, and understand your storage layout
is an essential skill.

## Checking Free Space with df

The `df` (disk free) command shows how much space is available on each mounted
filesystem:

```bash
df -h
```

The `-h` flag means **human-readable** -- sizes are shown in KB, MB, GB instead
of raw bytes. Typical output:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  234G   48G  174G  22% /
/dev/nvme0n1p1  511M   72M  440M  15% /boot
tmpfs           7.8G  156M  7.7G   2% /tmp
```

Key columns:

| Column       | Meaning                                       |
|--------------|-----------------------------------------------|
| `Filesystem` | The device or virtual filesystem              |
| `Size`       | Total capacity                                |
| `Used`       | Space consumed                                |
| `Avail`      | Space remaining                               |
| `Use%`       | Percentage of capacity used                   |
| `Mounted on` | Where in the directory tree it is accessible  |

### Filtering df output

To see only real disk filesystems (ignoring tmpfs, devtmpfs, etc.):

```bash
df -h --type=ext4 --type=btrfs --type=xfs
```

Or check a specific directory:

```bash
df -h /home
```

This shows the filesystem that `/home` lives on.

**Tip:** On CachyOS, the default filesystem is often **btrfs** or **ext4**. If
you are using btrfs, you may also want to use `btrfs filesystem usage /` for
more accurate space reporting, as btrfs handles free space differently.

## Measuring Directory Size with du

While `df` tells you about whole filesystems, `du` (disk usage) measures the
size of specific directories and files.

### Size of a single directory

```bash
du -sh /var/log
```

| Flag | Meaning                                      |
|------|----------------------------------------------|
| `-s` | Summary -- show only the total, not each file |
| `-h` | Human-readable sizes                         |

Output:

```
247M    /var/log
```

### Size of each item in a directory

```bash
du -sh /home/alex/*
```

This shows how much space each file and subdirectory directly inside
`/home/alex/` uses:

```
4.2G    /home/alex/Documents
1.1G    /home/alex/Downloads
892M    /home/alex/.cache
340M    /home/alex/Pictures
 12K    /home/alex/.bashrc
```

### Finding the biggest directories

Combine `du` with `sort` to find the largest subdirectories:

```bash
du -sh /home/alex/* | sort -rh | head -10
```

| Command     | What It Does                           |
|-------------|----------------------------------------|
| `du -sh *`  | Get size of each item                  |
| `sort -rh`  | Sort by human-readable size, reversed (largest first) |
| `head -10`  | Show only the top 10                   |

### Limiting depth

Sometimes you want to see a few levels deep without listing every single file:

```bash
du -h --max-depth=2 /var | sort -rh | head -20
```

The `--max-depth=2` flag shows directories up to two levels below `/var`.

## Understanding Block Devices with lsblk

The `lsblk` (list block devices) command shows your physical and virtual
storage devices in a tree format:

```bash
lsblk
```

```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
nvme0n1     259:0    0 476.9G  0 disk
├─nvme0n1p1 259:1    0   512M  0 part /boot
├─nvme0n1p2 259:2    0 468.4G  0 part /
└─nvme0n1p3 259:3    0     8G  0 part [SWAP]
sda           8:0    1  14.9G  0 disk
└─sda1        8:1    1  14.9G  0 part /run/media/alex/USB
```

This tells you:

- **nvme0n1** is your NVMe SSD (the whole disk).
- It has three **partitions**: a boot partition, a root partition, and swap.
- **sda** is a USB drive with one partition mounted at `/run/media/alex/USB`.

### More detail with lsblk

```bash
lsblk -f
```

The `-f` flag adds filesystem type, label, UUID, and available space:

```
NAME        FSTYPE LABEL   UUID                                 MOUNTPOINTS
nvme0n1p1   vfat   BOOT    ABCD-1234                            /boot
nvme0n1p2   btrfs  cachyos 12345678-abcd-efgh-ijkl-123456789abc /
nvme0n1p3   swap           87654321-dcba-...                     [SWAP]
```

## Mount Points

In Linux, storage devices are not accessed by drive letters like `C:` or `D:`.
Instead, they are **mounted** at specific directories in the filesystem tree.

- `/` is the **root mount point** -- your main filesystem.
- `/boot` typically holds the bootloader and kernel images.
- `/home` may be a separate partition on some setups.
- USB drives are often auto-mounted under `/run/media/username/`.

### Viewing mounts

The `mount` command with no arguments shows all current mounts, but the output
is very long. A cleaner alternative:

```bash
findmnt
```

This displays the same information in a readable tree format:

```
TARGET           SOURCE          FSTYPE  OPTIONS
/                /dev/nvme0n1p2  btrfs   rw,relatime,ssd
├─/boot          /dev/nvme0n1p1  vfat    rw,relatime
├─/tmp           tmpfs           tmpfs   rw,nosuid,nodev
└─/run/media/... /dev/sda1       ext4    rw,nosuid,nodev
```

### Filtering findmnt

Show only a specific mount point:

```bash
findmnt /boot
```

Show only real (non-virtual) filesystems:

```bash
findmnt -t btrfs,ext4,xfs,vfat
```

## Finding Large Files

When disk space is low, you need to find the culprits quickly.

### Using du to scan from root

```bash
sudo du -sh /* 2>/dev/null | sort -rh | head -10
```

Then drill into the largest directories:

```bash
sudo du -sh /var/* 2>/dev/null | sort -rh | head -10
```

### Using find for large files

```bash
find / -type f -size +100M 2>/dev/null | head -20
```

This finds all files larger than 100 MB. Common space hogs include:

- `/var/log/` -- log files that have grown unchecked
- `/var/cache/pacman/pkg/` -- the pacman package cache
- `~/.cache/` -- application caches (browsers, thumbnails)
- `~/Downloads/` -- forgotten downloads

## Monitoring Disk Health

### Check for filesystem errors

If you suspect disk issues on an ext4 filesystem (it must be unmounted first):

```bash
sudo fsck /dev/sda1
```

**Warning:** Never run `fsck` on a mounted filesystem. It can cause data
corruption. Use it from a live USB or on unmounted partitions only.

### SMART monitoring

Modern drives support SMART (Self-Monitoring, Analysis, and Reporting
Technology). Install the `smartmontools` package:

```bash
sudo pacman -S smartmontools
```

Then check drive health:

```bash
sudo smartctl -a /dev/nvme0n1
```

Look for the "SMART overall-health self-assessment test result" line. If it
says anything other than "PASSED," back up your data immediately.

## Btrfs-Specific Commands on CachyOS

If your CachyOS installation uses btrfs (a common default), there are some
additional useful commands:

```bash
sudo btrfs filesystem usage /
```

This gives a more accurate breakdown of space than `df` because btrfs handles
metadata, data, and unallocated space differently.

To list btrfs subvolumes:

```bash
sudo btrfs subvolume list /
```

## Quick Reference

| Task                        | Command                              |
|-----------------------------|--------------------------------------|
| Check free space            | `df -h`                              |
| Size of a directory         | `du -sh /path`                       |
| Size of contents            | `du -sh /path/*`                     |
| Top space users             | `du -sh /* \| sort -rh \| head`      |
| List block devices          | `lsblk`                              |
| Block devices with FS info  | `lsblk -f`                           |
| Show mount tree             | `findmnt`                            |
| Find large files            | `find / -type f -size +100M`         |
| Check drive health          | `sudo smartctl -a /dev/sdX`          |

## Try It Yourself

1. Run `df -h` and identify which filesystem holds your home directory. What
   percentage of it is used?

2. Check the total size of your home directory:
   ```bash
   du -sh ~
   ```

3. Find the five largest items in your home directory:
   ```bash
   du -sh ~/* | sort -rh | head -5
   ```

4. Run `lsblk` and identify how your disk is partitioned. Do you have a
   separate boot partition? Swap?

5. Use `lsblk -f` to find out which filesystem type your root partition uses.

6. Run `findmnt -t btrfs,ext4,xfs` to see only your real disk mounts.

7. Check how much space the pacman cache is using:
   ```bash
   du -sh /var/cache/pacman/pkg/
   ```

8. If you have smartmontools installed, check your drive health with
   `sudo smartctl -a /dev/nvme0n1` (adjust the device name as needed).
