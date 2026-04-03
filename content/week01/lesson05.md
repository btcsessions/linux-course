---
id: 5
week: 1
title: "Getting Help -- man, --help, and info"
duration_minutes: 15
objectives:
  - "Read and navigate man pages to learn about any command"
  - "Use --help for quick reference and command summaries"
  - "Use type, which, whereis, and apropos to discover and locate commands"
commands: [man, --help, info, type, which, whereis, apropos]
prerequisites: [4]
sandbox_commands: [man, which, type, whereis, apropos, ls, cd, pwd, whoami, hostname, date, cal, clear, echo, cat, help]
sandbox_setup: |
  echo "Practice looking up help for commands!" > README.txt
  mkdir docs
  echo "Use 'man ls' to learn about listing files" > docs/tips.txt
  echo "Use 'which python3' to find where python lives" > docs/exercises.txt
  echo "Remember: --help works on almost every command" > docs/reminder.txt
---

# Getting Help -- man, --help, and info

## You Do Not Need to Memorize Everything

One of the most important lessons in learning Linux is this: **nobody memorizes
every command and every option**. Even experienced system administrators look up
commands regularly. The difference between a beginner and an expert is not what
they have memorized -- it is how quickly they can find the answer.

Linux has a built-in help system that has been part of the operating system for
decades. In this lesson you will learn how to use it.

## man -- The Manual Pages

The primary documentation system on Linux is the **man pages** (short for
manual). Almost every command installed on your system has a man page.

To read the man page for a command, type:

```bash
man ls
```

This opens the manual for `ls` in a pager (usually `less`), which lets you
scroll through it.

### Navigating a Man Page

When you are inside a man page, you can use these keys:

| Key | Action |
|-----|--------|
| `Space` or `Page Down` | Scroll down one screen |
| `b` or `Page Up` | Scroll up one screen |
| `j` or `Down Arrow` | Scroll down one line |
| `k` or `Up Arrow` | Scroll up one line |
| `/pattern` | Search forward for "pattern" |
| `n` | Jump to the next search match |
| `N` | Jump to the previous search match |
| `q` | Quit the man page |
| `h` | Display help for the pager itself |

**Tip:** The search feature is extremely useful. If you open `man ls` and want
to find information about the `-t` option, type `/-t` and press Enter. Then
press `n` to cycle through matches.

### Anatomy of a Man Page

Man pages follow a standard structure:

| Section | Contents |
|---------|----------|
| **NAME** | The command name and a one-line description |
| **SYNOPSIS** | The command syntax showing options and arguments |
| **DESCRIPTION** | Detailed explanation of what the command does |
| **OPTIONS** | A list of all available flags and options |
| **EXAMPLES** | Usage examples (not all man pages include this) |
| **SEE ALSO** | Related commands and man pages |
| **AUTHOR** | Who wrote the command |
| **BUGS** | Known issues |

The most useful sections for day-to-day work are **SYNOPSIS** (to see the
command's syntax), **OPTIONS** (to find the flag you need), and **EXAMPLES**
(when available).

### Reading the SYNOPSIS

The SYNOPSIS section uses conventions you should learn to read:

```
ls [OPTION]... [FILE]...
```

- **Bold** or plain text means type it literally.
- Items in `[brackets]` are optional.
- `...` means the item can be repeated (e.g., multiple files).
- Items separated by `|` are alternatives (choose one).

So `ls [OPTION]... [FILE]...` means: type `ls`, optionally followed by one or
more options, optionally followed by one or more file names.

### Man Page Sections (Numbered)

Man pages are organized into numbered sections:

| Section | Content |
|---------|---------|
| 1 | User commands (what you type at the prompt) |
| 2 | System calls (programming) |
| 3 | Library functions (programming) |
| 4 | Special files (/dev) |
| 5 | File formats and conventions |
| 6 | Games |
| 7 | Miscellaneous |
| 8 | System administration commands |

Most of the time you want section 1 (user commands), which is the default. But
sometimes a name appears in multiple sections. For example, `passwd` is both a
command (section 1) and a file format (section 5):

```bash
man passwd       # Opens section 1 (the command)
man 5 passwd     # Opens section 5 (the /etc/passwd file format)
```

## --help -- Quick Reference

Most commands support a `--help` flag that prints a short summary directly in
your terminal:

```bash
ls --help
```

This gives you a condensed version of the man page -- usually a list of options
with brief descriptions. It is faster than opening a full man page when you
just need to jog your memory about a specific flag.

Some commands use `-h` instead of `--help`, and a few use `-?`. If one does not
work, try another:

```bash
ls --help
cal -h
```

**Tip:** The `--help` output prints directly to your terminal, so you can scroll
up to review it. If it is too long and scrolls off screen, pipe it to `less`:

```bash
ls --help | less
```

You have not learned about pipes (`|`) yet -- they are coming later in the
course. For now, just know that `| less` lets you scroll through long output.

## info -- GNU Info Pages

Some commands (especially GNU tools) have more detailed documentation in the
**info** format:

```bash
info coreutils
```

Info pages are organized as a hyperlinked document, similar to a simple website.
Navigation keys are different from man pages:

| Key | Action |
|-----|--------|
| `Space` | Scroll down |
| `Backspace` | Scroll up |
| `n` | Next node (section) |
| `p` | Previous node |
| `u` | Up one level |
| `Enter` | Follow a hyperlink (on a menu item) |
| `q` | Quit |

In practice, most people prefer man pages or online documentation over info
pages. But it is good to know they exist.

## type -- What Kind of Command Is This?

The `type` command tells you what a command name actually is:

```bash
type ls
```

```
ls is aliased to 'ls --color=auto'
```

```bash
type cd
```

```
cd is a shell builtin
```

```bash
type python
```

```
python is /usr/bin/python
```

This is useful because commands can be several things:

- **An alias** -- a shortcut defined in your shell configuration
- **A shell builtin** -- a command built directly into the shell itself
- **An external program** -- a binary file somewhere on your disk
- **A shell function** -- a function defined in your shell startup files

Knowing the type helps you understand where to look for documentation. Shell
builtins are documented in the shell's own man page (`man bash`), while external
programs have their own man pages.

## which -- Where Is the Program?

If a command is an external program, `which` tells you its location:

```bash
which ls
```

```
/usr/bin/ls
```

```bash
which pacman
```

```
/usr/bin/pacman
```

This is helpful when you want to know which version of a program is being used,
or when you have multiple versions installed and want to verify which one runs
by default.

**Tip:** `which` only finds external programs. It will not find shell builtins or
aliases. Use `type` for a more complete answer.

## whereis -- Find Binary, Source, and Man Page

The `whereis` command is broader than `which`. It searches for the binary, the
source code, and the man page:

```bash
whereis ls
```

```
ls: /usr/bin/ls /usr/share/man/man1/ls.1.gz
```

This tells you that the `ls` binary is at `/usr/bin/ls` and its man page is at
`/usr/share/man/man1/ls.1.gz`.

## apropos -- Search for Commands by Keyword

What if you do not know the name of the command you need? You know *what* you
want to do, but not *which* command does it. This is where `apropos` comes in:

```bash
apropos "list directory"
```

```
dir (1)              - list directory contents
ls (1)               - list directory contents
vdir (1)             - list directory contents
```

`apropos` searches the short descriptions in all man pages and shows matches.
It is essentially a keyword search of the manual system.

Other examples:

```bash
apropos calendar
apropos "copy files"
apropos password
```

**Tip:** If `apropos` returns "nothing appropriate," you may need to build the
man page database first:

```bash
sudo mandb
```

On CachyOS this is usually done automatically, but it is good to know the
command.

## help -- For Shell Builtins

Shell builtins (like `cd`, `echo`, `type`, `export`) do not have standalone man
pages because they are part of the shell itself. In bash, you can get help for
them using:

```bash
help cd
```

```
cd: cd [-L|[-P [-e]] [-@]] [dir]
    Change the shell working directory...
```

This works only in bash. In fish, you would use:

```bash
cd --help
```

## Building a Help Strategy

Here is a practical workflow for when you need help:

1. **Try `--help` first** -- quick and stays in your terminal.
2. **Read the man page** -- comprehensive reference with `man command`.
3. **Use `apropos`** -- when you do not know the command name.
4. **Use `type` and `which`** -- when you want to know what a command really is.
5. **Search online** -- the Arch Wiki (wiki.archlinux.org) is one of the best
   Linux documentation resources, and since CachyOS is Arch-based, everything
   there applies to your system.

## CachyOS-Specific Notes

- The **Arch Wiki** at https://wiki.archlinux.org is your best friend. It is
  widely regarded as the most comprehensive and well-maintained Linux wiki. Since
  CachyOS is built on Arch, almost all Arch Wiki articles apply directly.
- CachyOS also has its own wiki at https://wiki.cachyos.org for CachyOS-specific
  topics like kernel selection and performance tuning.
- If a man page is missing, the package providing it might not be installed.
  You can install man pages for most packages with:
  ```bash
  sudo pacman -S man-pages
  ```
- If you are using fish, `man` works the same way, but `help cd` will open
  documentation in your web browser instead of the terminal.

## Try It Yourself

1. Run `man ls` and practice navigating: scroll down, scroll up, search for
   `-l`, then quit with `q`.
2. Run `ls --help` and compare it with the man page. Notice how the `--help`
   output is shorter.
3. Run `man man` -- yes, the man command has its own man page. Read the
   DESCRIPTION to learn more about man page sections.
4. Run `type ls` to see if `ls` is aliased on your system.
5. Run `type cd` to confirm that `cd` is a shell builtin.
6. Run `which pacman` to find where the package manager binary lives.
7. Run `whereis ls` to see the binary location and man page location.
8. Run `apropos "file manager"` or `apropos calendar` to discover related
   commands.
9. Run `man 5 passwd` and compare it with `man passwd`. Notice they are
   completely different pages.
10. Run `help cd` (in bash) to see the builtin help for the cd command.

You now have all the tools you need to teach yourself any Linux command. The
rest of this course will introduce you to many new commands, but you will always
be able to fall back on `man`, `--help`, and `apropos` to fill in the gaps on
your own.

Congratulations on completing Week 1! You can open a terminal, identify your
prompt, run basic commands, navigate the filesystem, list directory contents,
and look up help for anything. That is a solid foundation for everything that
comes next.
