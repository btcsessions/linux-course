---
id: 1
week: 1
title: "Welcome to the Terminal"
duration_minutes: 15
objectives:
  - "Understand what a terminal emulator and shell are"
  - "Identify the components of the shell prompt (user@host:dir$)"
  - "Run your first commands: whoami, hostname, date, cal, clear, echo"
commands: [whoami, hostname, date, cal, clear, echo]
prerequisites: []
sandbox_commands: [whoami, hostname, date, cal, clear, echo, ls]
sandbox_setup: |
  echo "Welcome to the CachyCLI sandbox!" > welcome.txt
  echo "This is a sample file." > sample.txt
  mkdir documents pictures
  echo "My notes" > documents/notes.txt
  echo "Photo list" > pictures/photos.txt
---

# Welcome to the Terminal

## What Is a Terminal?

When most people think of using a computer, they picture clicking icons, dragging
windows, and scrolling through menus. That is the **graphical user interface**
(GUI). But underneath every Linux system -- including your CachyOS desktop --
lives a powerful text-based interface called the **terminal**.

A **terminal emulator** is the application that gives you a window into that
text world. On CachyOS you will typically find one of these already installed:

- **Konsole** (if you are running KDE Plasma, the CachyOS default desktop)
- **GNOME Terminal** or **Alacritty** (on other desktop variants)

You can usually open a terminal with the keyboard shortcut **Ctrl + Alt + T**, or
by searching for "Terminal" in your application menu.

## What Is a Shell?

The terminal emulator is just the window. The program that actually reads what
you type and decides what to do with it is called the **shell**.

Think of it this way:

- The **terminal** is the screen and keyboard of an old teletype machine.
- The **shell** is the operator sitting at the machine, interpreting your requests.

CachyOS ships with **fish** (Friendly Interactive Shell) as the default
interactive shell on many of its editions, though **bash** (Bourne Again Shell)
is also available and is the default on most other Linux distributions. You may
also encounter **zsh**. The core commands you learn here work the same in all of
them.

**Tip:** You can check which shell you are running by looking at the output of
`echo $SHELL` or, more reliably, `echo $0`.

## The Prompt

When you open your terminal you will see something like this:

```
alex@cachyos ~ $
```

Each piece tells you something:

| Part        | Meaning                                         |
|-------------|--------------------------------------------------|
| `alex`      | Your username -- the account you are logged in as |
| `@`         | Separator (just punctuation)                     |
| `cachyos`   | The hostname -- the name of your computer        |
| `~`         | Your current directory (`~` means your home dir) |
| `$`         | Prompt symbol -- you are a normal user           |

If you ever see a `#` instead of `$`, that means you are logged in as the
**root** (administrator) user. Be extra careful in that mode.

**Tip:** The prompt format can be customized. What you see depends on your
shell and its configuration, but the information above is the most common
layout.

## Command Syntax

Every command you type in the terminal follows a general pattern:

```
command [options] [arguments]
```

- **command** -- the program you want to run (e.g., `ls`).
- **options** -- modify the behavior of the command. They usually start with
  a dash (`-l`) or double-dash (`--long`).
- **arguments** -- the targets the command acts on (e.g., a filename).

Square brackets mean the part is optional. Some commands need no options or
arguments at all.

## Your First Commands

Let's run some commands. Type each one at your prompt and press **Enter**.

### whoami

```bash
whoami
```

This prints your username. It is the simplest possible command -- no options,
no arguments, just a question: "Who am I?"

```
alex
```

### hostname

```bash
hostname
```

This prints the name of your computer. On a fresh CachyOS install, this might
be something like `cachyos` or whatever you chose during setup.

```
cachyos
```

### date

```bash
date
```

This shows the current date and time:

```
Thu Mar 27 10:42:15 AM EDT 2026
```

You can format the output with options. For example:

```bash
date +"%Y-%m-%d"
```

Gives you just the date in a tidy format:

```
2026-03-27
```

### cal

```bash
cal
```

This prints a small calendar for the current month:

```
     March 2026
Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31
```

Want to see a full year?

```bash
cal 2026
```

Or a specific month and year:

```bash
cal 6 2026
```

### clear

```bash
clear
```

This wipes the screen so you start with a clean slate. You can also press
**Ctrl + L** as a shortcut in most shells.

**Tip:** `clear` does not delete your command history. You can still scroll
up to see previous output in most terminal emulators.

### echo

```bash
echo "Hello, CachyOS!"
```

`echo` prints whatever text you give it back to the screen:

```
Hello, CachyOS!
```

This might seem pointless now, but `echo` is one of the most frequently used
commands in shell scripting. You can also use it to peek at environment
variables:

```bash
echo $HOME
```

```
/home/alex
```

```bash
echo $USER
```

```
alex
```

## Combining What You Know

You can run multiple commands on one line by separating them with a semicolon:

```bash
whoami; hostname; date
```

```
alex
cachyos
Thu Mar 27 10:45:00 AM EDT 2026
```

This is a handy trick when you want quick output from several commands without
typing each one separately.

## A Note About Case Sensitivity

Linux is **case-sensitive**. That means:

- `whoami` works.
- `Whoami` does **not** work.
- `WHOAMI` does **not** work.

Always type commands in the exact case shown. Almost all standard Linux commands
are lowercase.

**Warning:** Case sensitivity also applies to filenames. `Report.txt` and
`report.txt` are two completely different files on Linux.

## CachyOS-Specific Notes

CachyOS is built on Arch Linux, which means:

- Packages are installed with **pacman** (you will learn this later).
- The system is rolling-release, so you always have the latest software.
- If `cal` is not installed, you can install it with `sudo pacman -S util-linux`.
  On a standard CachyOS install it should already be present.
- The default shell may be **fish**. If you want to follow along with bash
  examples exactly, you can type `bash` at any time to switch to a bash session.

## Try It Yourself

Practice makes permanent. Open your terminal and try each of these exercises:

1. Run `whoami` and `hostname`. Do the values match what you set during install?
2. Run `date +"%A"` to see just the day of the week.
3. Run `cal 12 2026` to see December 2026.
4. Use `echo` to print your name: `echo "My name is ___"`
5. Run `echo $SHELL` to find out which shell you are using.
6. Chain three commands together with semicolons on a single line.
7. Try typing `WHOAMI` (all caps). Read the error message -- what does it say?
8. Use `clear` or **Ctrl + L** to clean your screen, then run `cal` again.

Congratulations -- you have just had your first real conversation with your
Linux system. In the next lesson, we will find out *where* you are inside the
filesystem.
