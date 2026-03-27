---
id: 7
week: 2
title: "Copying and Moving"
duration_minutes: 15
objectives:
  - "Copy files and directories with cp and cp -r"
  - "Move and rename files and directories with mv"
  - "Understand the difference between copying and moving"
commands: [cp, cp -r, cp -i, mv, mv -i]
prerequisites: []
sandbox_commands: [cp, mv, ls, touch, mkdir]
sandbox_setup: |
  mkdir -p ~/practice/subdir
  echo "Hello from file1" > ~/practice/file1.txt
  echo "Hello from file2" > ~/practice/file2.txt
  cd ~/practice
---

# Copying and Moving

Once you have created files and directories, you will constantly need to
rearrange them -- making backups, reorganising projects, or renaming things.
This lesson covers the two essential commands for that: `cp` (copy) and `mv`
(move/rename).

## Copying Files with `cp`

The `cp` command duplicates a file, leaving the original in place.

### Basic syntax

```bash
cp source destination
```

**Example -- copy a file to a new name:**

```bash
cp file1.txt file1_backup.txt
```

Now you have two independent files with identical contents. Changing one does
not affect the other.

**Example -- copy a file into a directory:**

```bash
cp file1.txt subdir/
```

This places a copy of `file1.txt` inside `subdir/`. The original stays where
it is.

**Example -- copy and rename at the same time:**

```bash
cp file1.txt subdir/renamed.txt
```

The copy lands in `subdir/` with the name `renamed.txt`.

### Copying multiple files

You can copy several files into a directory in one command:

```bash
cp file1.txt file2.txt subdir/
```

When copying multiple sources, the last argument **must** be a directory.

### Preserving attributes with `-a`

By default `cp` may not preserve ownership, permissions, or timestamps. The
`-a` (archive) flag keeps everything intact:

```bash
cp -a file1.txt file1_archive.txt
```

This is especially useful for backups.

### Interactive mode with `-i`

If the destination already exists, `cp` silently overwrites it. To get a
confirmation prompt first, use `-i`:

```bash
cp -i file1.txt file2.txt
# cp: overwrite 'file2.txt'?
```

**Tip:** On CachyOS (and many Arch-based systems) you can alias `cp` to
`cp -i` in your `~/.bashrc` so you always get prompted before overwriting.

### Verbose mode with `-v`

See exactly what is happening:

```bash
cp -v file1.txt subdir/
# 'file1.txt' -> 'subdir/file1.txt'
```

## Copying Directories with `cp -r`

Plain `cp` refuses to copy a directory:

```bash
cp subdir/ backup/
# cp: -r not specified; omitting directory 'subdir/'
```

You need the `-r` (recursive) flag to copy a directory and everything inside
it:

```bash
cp -r subdir/ subdir_backup/
```

This creates `subdir_backup/` as a complete copy of `subdir/`, including all
files and subdirectories within it.

### Combining flags

Flags can be combined:

```bash
cp -rv subdir/ subdir_backup/    # recursive + verbose
cp -ri subdir/ subdir_backup/    # recursive + interactive
cp -ra subdir/ subdir_backup/    # recursive + archive (preserve all attributes)
```

### Watch the trailing slash

Be careful with trailing slashes when copying directories:

```bash
cp -r subdir  backup/      # copies subdir INTO backup/ -> backup/subdir/
cp -r subdir/ backup/      # same result on most systems
```

If `backup/` does not exist, it becomes the copy itself. If it does exist, the
source is placed inside it. Always verify with `ls` after copying.

## Moving and Renaming with `mv`

The `mv` command serves two purposes:

1. **Move** a file or directory to a different location.
2. **Rename** a file or directory (move it to the same location with a new
   name).

### Renaming a file

```bash
mv file1.txt report.txt
```

`file1.txt` no longer exists; it has been renamed to `report.txt`.

### Moving a file into a directory

```bash
mv report.txt subdir/
```

`report.txt` is gone from the current directory and now lives inside `subdir/`.

### Moving and renaming simultaneously

```bash
mv file2.txt subdir/data.txt
```

The file ends up inside `subdir/` with the new name `data.txt`.

### Moving multiple files

Like `cp`, you can move several files at once if the last argument is a
directory:

```bash
mv file1.txt file2.txt file3.txt subdir/
```

### Moving directories

Unlike `cp`, `mv` works on directories without any special flag:

```bash
mv subdir/ archive/
```

This renames (or relocates) the entire directory.

### Interactive mode with `-i`

Just like `cp -i`, this prompts before overwriting:

```bash
mv -i file1.txt file2.txt
# mv: overwrite 'file2.txt'?
```

### Verbose mode with `-v`

```bash
mv -v file1.txt subdir/
# renamed 'file1.txt' -> 'subdir/file1.txt'
```

## Copy vs Move: Key Differences

| Aspect | `cp` | `mv` |
|--------|------|------|
| Original file | Kept | Removed |
| Disk usage | Doubles (new copy) | Same (no new data on same filesystem) |
| Needs `-r` for dirs | Yes | No |
| Speed on same filesystem | Slower (copies bytes) | Instant (updates directory entry) |
| Speed across filesystems | Same | Same (must copy then delete) |

**Important:** When `mv` operates within the same filesystem, it is nearly
instant regardless of file size because it only updates a directory entry. When
moving across filesystems (e.g., from `/home` to `/tmp` if they are separate
partitions), `mv` internally copies the data and then deletes the original.

## Common Patterns

### Making a quick backup

```bash
cp config.conf config.conf.bak
```

### Organising files into directories

```bash
mkdir -p sorted/{images,documents,scripts}
mv *.jpg sorted/images/
mv *.pdf sorted/documents/
mv *.sh sorted/scripts/
```

### Renaming with a pattern (batch rename)

While `mv` handles single renames, for batch operations consider the `rename`
command (available in the Arch repositories). But for basic tasks, a loop
works:

```bash
for f in *.txt; do
    mv "$f" "backup_$f"
done
```

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| `cp dir1 dir2` without `-r` | Error: omitting directory | Use `cp -r dir1 dir2` |
| `mv *.log logs/` when `logs/` doesn't exist | File renamed to `logs` if only one match | Create the target directory first |
| Overwriting without `-i` | Data lost silently | Use `-i` flag or set an alias |
| Forgetting trailing `/` on destination | Ambiguous: rename vs move-into | Be explicit; ensure target dir exists |

## Try It Yourself

1. Copy `file1.txt` to a new file called `file1_copy.txt`:
   ```bash
   cp file1.txt file1_copy.txt
   ls -l
   ```

2. Copy `file2.txt` into `subdir/`:
   ```bash
   cp file2.txt subdir/
   ls subdir/
   ```

3. Copy the entire `subdir/` directory to `subdir_backup/`:
   ```bash
   cp -r subdir/ subdir_backup/
   ls -R subdir_backup/
   ```

4. Rename `file1_copy.txt` to `renamed.txt`:
   ```bash
   mv file1_copy.txt renamed.txt
   ls
   ```

5. Move `renamed.txt` into `subdir/`:
   ```bash
   mv renamed.txt subdir/
   ls subdir/
   ```

6. Move `subdir_backup/` to a new name:
   ```bash
   mv subdir_backup/ archive/
   ls
   ```

7. Try overwriting safely with `-i`:
   ```bash
   cp file1.txt file2.txt     # silent overwrite
   cp -i file1.txt file2.txt  # asks first
   ```

## Summary

| Command | Purpose |
|---------|---------|
| `cp src dest` | Copy a file |
| `cp -r src/ dest/` | Copy a directory recursively |
| `cp -i src dest` | Copy with overwrite confirmation |
| `mv src dest` | Move or rename a file/directory |
| `mv -i src dest` | Move with overwrite confirmation |
| `cp -v` / `mv -v` | Show what is being done (verbose) |

You can now duplicate and rearrange files and directories with confidence. Next
up: removing them safely.
