---
id: 13
week: 3
title: "Introduction to vim (Survival Mode)"
duration_minutes: 15
objectives:
  - "Understand vim's modal editing concept (Normal, Insert, Command-line)"
  - "Open files, enter Insert mode, and type text"
  - "Save and quit using :w, :q, :wq, and the emergency exit :q!"
commands: [vim, i, Esc, ":w", ":q", ":wq", ":q!", h, j, k, l, dd, u]
prerequisites: []
sandbox_commands: [vim, cat, ls]
sandbox_setup: |
  #!/bin/bash
  cat > ~/vim_practice.txt <<'EOF'
  Welcome to vim practice.
  This is line two.
  Edit this line to say something new.
  Here is line four.
  This line should be deleted.
  The quick brown fox jumps over the lazy dog.
  CachyOS ships with vim by default.
  Happy editing!
  EOF
---
# Introduction to vim (Survival Mode)

At some point every Linux user ends up inside vim -- maybe by running `git commit`
without setting an editor, maybe by opening a file on a server where nano is not
installed. The internet is full of jokes about people being unable to exit vim. After
this lesson, you will never be one of them.

This is not a full vim tutorial. It is **survival mode**: enough knowledge to open a
file, make an edit, save, and get out. Once you are comfortable with these basics, vim
becomes an incredibly powerful editor worth learning further on your own.

## Why vim?

- It is installed on virtually every Unix and Linux system, including CachyOS.
- Many command-line tools (like `git`) default to vim.
- It is extremely fast once you know the basics.
- Configuration files on remote servers often must be edited with vim.

## The Key Concept: Modes

Unlike nano, where you just start typing, vim uses **modes**. This is the single most
important thing to understand:

| Mode | Purpose | How to Enter |
|------|---------|-------------|
| **Normal** | Navigate, delete, copy, paste | Press `Esc` (this is the default mode) |
| **Insert** | Type and edit text | Press `i` from Normal mode |
| **Command-line** | Save, quit, search, run commands | Press `:` from Normal mode |
| **Visual** | Select text | Press `v` from Normal mode |

> **Golden rule:** When in doubt, press `Esc`. It always takes you back to Normal
> mode. Press it twice if you are unsure.

## Opening a File

```bash
vim vim_practice.txt
```

To create a new file:

```bash
vim newfile.txt
```

When vim opens, you are in **Normal mode**. You cannot type text yet -- that is the
part that confuses newcomers.

## Entering Insert Mode

To start typing, press one of these keys from Normal mode:

| Key | Insert Where |
|-----|-------------|
| `i` | Before the cursor (most common) |
| `a` | After the cursor |
| `I` | At the beginning of the line |
| `A` | At the end of the line |
| `o` | Open a new line below |
| `O` | Open a new line above |

The bottom of the screen will show `-- INSERT --` to confirm you are in Insert mode.

When you are done typing, press **`Esc`** to return to Normal mode.

## Saving and Quitting

All save/quit commands start with `:` from Normal mode:

| Command | Action |
|---------|--------|
| `:w` | **Write** (save) the file |
| `:q` | **Quit** vim |
| `:wq` | **Write and quit** (save then exit) |
| `:q!` | **Quit without saving** (force quit -- the emergency exit) |
| `ZZ` | Shortcut for `:wq` (capital Z, twice, no colon) |

### The Emergency Exit

If you are stuck, panicking, and just want out:

1. Press **`Esc`** (maybe twice to be safe).
2. Type **`:q!`** and press **Enter**.

That will drop all changes and exit vim. Memorize this sequence.

## Basic Navigation in Normal Mode

You can use the arrow keys, but vim veterans prefer:

| Key | Direction |
|-----|-----------|
| `h` | Left |
| `j` | Down |
| `k` | Up |
| `l` | Right |

Other useful navigation:

| Key | Action |
|-----|--------|
| `0` | Jump to beginning of line |
| `$` | Jump to end of line |
| `gg` | Jump to first line of file |
| `G` | Jump to last line of file |
| `w` | Jump forward one word |
| `b` | Jump backward one word |

## Essential Editing in Normal Mode

You do not need to be in Insert mode for every edit. Normal mode has powerful
commands:

| Command | Action |
|---------|--------|
| `dd` | **Delete** (cut) the entire current line |
| `yy` | **Yank** (copy) the current line |
| `p` | **Paste** after the cursor |
| `u` | **Undo** the last change |
| `Ctrl+r` | **Redo** (undo the undo) |
| `x` | Delete the character under the cursor |
| `dw` | Delete from cursor to end of word |

### Deleting Multiple Lines

Type a number before `dd` to delete multiple lines:

```
3dd    -- deletes 3 lines starting from the cursor
```

## Searching

From Normal mode:

| Command | Action |
|---------|--------|
| `/pattern` | Search forward for *pattern* |
| `?pattern` | Search backward |
| `n` | Jump to next match |
| `N` | Jump to previous match |

Example: type `/fox` and press Enter to find the word "fox" in the practice file.

## The Typical vim Workflow

Here is the step-by-step pattern you will use most often:

1. **Open the file:** `vim filename`
2. **Navigate** to where you want to edit (arrow keys or `h/j/k/l`).
3. **Press `i`** to enter Insert mode.
4. **Type your changes.**
5. **Press `Esc`** to return to Normal mode.
6. **Type `:wq`** and press Enter to save and quit.

## Common Mistakes and How to Fix Them

| Problem | Solution |
|---------|----------|
| Typing produces strange behavior | You are in Normal mode. Press `i` first. |
| Cannot quit | Press `Esc`, then type `:q!` and Enter. |
| Accidentally deleted text | Press `u` to undo. |
| Screen looks garbled | Press `Esc`, then type `:redraw!` and Enter. |
| Opened vim by accident from git | `:q!` to abort the commit. |

## vim vs nano: When to Use Which

| Situation | Recommended Editor |
|-----------|-------------------|
| Quick one-line config change | `nano` |
| Server with only vi/vim available | `vim` |
| Git commit messages (default editor) | Set your preference (see below) |
| Heavy text editing or programming | `vim` (once proficient) |

### Setting Your Default Editor

If you prefer nano over vim for git and other tools:

```bash
echo 'export EDITOR=nano' >> ~/.bashrc
source ~/.bashrc
```

Or if you want vim:

```bash
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc
```

## Try It Yourself

1. **Open the practice file:**
   ```bash
   vim vim_practice.txt
   ```

2. **Navigate** to line 3 using the `j` key.

3. **Enter Insert mode** by pressing `i`. Change the text on that line. Press `Esc`
   when done.

4. **Delete a line:** Navigate to "This line should be deleted." and press `dd`.

5. **Undo the deletion** by pressing `u`.

6. **Search** for the word "fox" by typing `/fox` and pressing Enter.

7. **Save and exit:** Press `Esc`, type `:wq`, and press Enter.

8. **Verify your changes:**
   ```bash
   cat vim_practice.txt
   ```

9. **Practice the emergency exit:** Open the file again with `vim vim_practice.txt`,
   make some random edits, then press `Esc` and type `:q!` to quit without saving.

## Quick Reference Card

```
NORMAL MODE (default -- press Esc to return here)
  h/j/k/l   Move left/down/up/right
  i          Enter Insert mode
  dd         Delete line          yy   Copy line
  p          Paste                u    Undo
  /pattern   Search               n    Next match
  :w         Save                 :q   Quit
  :wq        Save and quit        :q!  Quit without saving
  ZZ         Save and quit (shortcut)

INSERT MODE (press i to enter, Esc to leave)
  Type normally -- everything you type is inserted.
```

## Summary

- vim uses **modes** -- Normal mode for commands, Insert mode for typing.
- Press **`i`** to enter Insert mode, **`Esc`** to return to Normal mode.
- Save with **`:w`**, quit with **`:q`**, do both with **`:wq`**.
- The emergency exit is **`Esc` then `:q!`** -- this quits without saving.
- **`dd`** deletes a line, **`u`** undoes, **`/pattern`** searches.
- When in doubt, press **`Esc`**.
