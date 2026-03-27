---
id: 12
week: 3
title: "Text Editors -- nano"
duration_minutes: 15
objectives:
  - "Open, edit, save, and exit files using nano"
  - "Use essential nano shortcuts for cutting, pasting, searching, and getting help"
commands: [nano]
prerequisites: []
sandbox_commands: [nano]
sandbox_setup: |
  #!/bin/bash
  cat > ~/practice.txt <<'EOF'
  Welcome to the nano practice file.
  This file has several lines for you to edit.
  Try changing this line.
  Add a new line below this one.
  Delete this line entirely.
  The quick brown fox jumps over the lazy dog.
  CachyOS is a performance-focused Arch-based distribution.
  Practice makes perfect.
  EOF
---
# Text Editors -- nano

Sooner or later you will need to edit a file directly in the terminal. Maybe you are
connected to a remote server over SSH, or you just need to make a quick change to a
config file. `nano` is the friendliest terminal-based text editor and ships with
virtually every Linux distribution, including CachyOS.

## Opening a File

To open an existing file:

```bash
nano practice.txt
```

To create a new file, just give it a name that does not exist yet:

```bash
nano newfile.txt
```

When nano opens, you will see:

- The **file contents** in the main area.
- A **title bar** at the top showing the filename.
- A **shortcut bar** at the bottom listing common key combinations.

> **Key convention:** In nano's shortcut bar, the `^` symbol means **Ctrl**. So
> `^O` means press `Ctrl+O`. The `M-` prefix means **Alt** (Meta).

## Essential Shortcuts

### Saving and Exiting

| Shortcut   | Action                                      |
|------------|---------------------------------------------|
| `Ctrl+O`   | **Write Out** -- save the file              |
| `Ctrl+X`   | **Exit** nano                               |

When you press `Ctrl+O`, nano asks you to confirm (or change) the filename. Press
`Enter` to save. If you press `Ctrl+X` with unsaved changes, nano will ask whether
to save -- press `Y` for yes, `N` for no, or `Ctrl+C` to cancel.

### Navigation

| Shortcut     | Action                          |
|--------------|---------------------------------|
| Arrow keys   | Move cursor                     |
| `Ctrl+A`     | Go to beginning of current line |
| `Ctrl+E`     | Go to end of current line       |
| `Ctrl+Y`     | Scroll up one page              |
| `Ctrl+V`     | Scroll down one page            |
| `Ctrl+_`     | Go to a specific line number    |

### Editing

| Shortcut   | Action                                      |
|------------|---------------------------------------------|
| `Ctrl+K`   | **Cut** the current line (or selected text)  |
| `Ctrl+U`   | **Paste** (uncut) the last cut text          |
| `Alt+6`    | **Copy** the current line (without cutting)  |
| `Ctrl+J`   | **Justify** (reformat) the current paragraph |
| `Ctrl+T`   | Invoke the spell checker (if installed)      |

> **Tip:** You can cut multiple consecutive lines by pressing `Ctrl+K` several
> times in a row. They all accumulate in the paste buffer, so a single `Ctrl+U`
> pastes them all back.

### Searching and Replacing

| Shortcut   | Action                          |
|------------|---------------------------------|
| `Ctrl+W`   | **Search** for text             |
| `Alt+W`    | Repeat last search              |
| `Ctrl+\`   | **Search and replace**          |

When you press `Ctrl+W`, type your search term and press `Enter`. nano jumps to the
first match. Press `Alt+W` to find subsequent matches.

For search-and-replace (`Ctrl+\`):
1. Type the text to find, press `Enter`.
2. Type the replacement, press `Enter`.
3. Choose `Y` to replace this occurrence, `N` to skip, or `A` to replace all.

### Getting Help

Press `Ctrl+G` at any time to open nano's built-in **help screen**. It lists every
shortcut available. Press `Ctrl+X` to close help and return to your file.

## Selecting Text

Nano supports a simple selection mechanism:

1. Move the cursor to the start of the text you want to select.
2. Press `Alt+A` to set the mark (beginning of selection).
3. Move the cursor to extend the selection -- the highlighted region grows.
4. Press `Ctrl+K` to cut or `Alt+6` to copy the selection.

Press `Alt+A` again to cancel the mark without cutting.

## Useful Command-Line Options

```bash
# Open file at a specific line number
nano +25 practice.txt

# Open in read-only mode (view mode)
nano -v practice.txt

# Enable line numbers in the display
nano -l practice.txt

# Open with soft line wrapping
nano -$ practice.txt
```

## Making nano More Comfortable

On CachyOS, nano reads its configuration from `~/.nanorc`. You can enable helpful
features there:

```bash
# Create or edit your nanorc
nano ~/.nanorc
```

Add these commonly desired settings:

```
# Show line numbers
set linenumbers

# Enable mouse support
set mouse

# Use smooth scrolling
set smooth

# Enable syntax highlighting (usually on by default)
include "/usr/share/nano/*.nanorc"
```

Save with `Ctrl+O` and exit with `Ctrl+X`.

## Try It Yourself

1. **Open the practice file:**
   ```bash
   nano practice.txt
   ```

2. **Navigate to line 3** by pressing `Ctrl+_`, typing `3`, and pressing `Enter`.

3. **Edit the line** -- change the text to something of your choice.

4. **Search for a word:** Press `Ctrl+W`, type `fox`, and press `Enter`. The cursor
   jumps to the matching line.

5. **Cut and paste a line:** Move to the line that says "Delete this line entirely."
   Press `Ctrl+K` to cut it. Move to the end of the file and press `Ctrl+U` to
   paste it there.

6. **Save your changes:** Press `Ctrl+O`, confirm the filename, and press `Enter`.

7. **Exit nano:** Press `Ctrl+X`.

8. **Verify your edits:**
   ```bash
   cat practice.txt
   ```

## Quick Reference Card

```
Ctrl+G  Help        Ctrl+O  Save        Ctrl+X  Exit
Ctrl+K  Cut line    Ctrl+U  Paste       Alt+6   Copy line
Ctrl+W  Search      Ctrl+\  Replace     Alt+W   Search again
Ctrl+A  Line start  Ctrl+E  Line end    Ctrl+_  Go to line
Ctrl+Y  Page up     Ctrl+V  Page down
```

## Summary

- `nano` is a beginner-friendly terminal editor available on CachyOS by default.
- `Ctrl+O` saves, `Ctrl+X` exits, `Ctrl+K` cuts, `Ctrl+U` pastes.
- `Ctrl+W` searches, `Ctrl+\` does search-and-replace.
- `Ctrl+G` opens the built-in help at any time.
- Customize nano behavior in `~/.nanorc`.
