---
id: 28
week: 6
title: "Environment Variables and the Shell"
duration_minutes: 15
objectives:
  - "View and set environment variables with export, env, and printenv"
  - "Understand the $PATH variable and how the shell finds commands"
  - "Know which shell configuration files are loaded on CachyOS (bash and fish)"
  - "Create and use aliases to shorten repetitive commands"
commands: [env, printenv, export, echo, source, alias]
prerequisites: []
sandbox_commands: [env, printenv, export, echo, source, alias, cat, grep, bash]
sandbox_setup: |
  #!/bin/bash
  mkdir -p ~/demo/bin
  echo '#!/bin/bash' > ~/demo/bin/hello
  echo 'echo "Hello from $USER on $(hostname)!"' >> ~/demo/bin/hello
  chmod +x ~/demo/bin/hello
  # Create a sample .bashrc snippet
  cat > ~/demo/sample_bashrc <<'CONF'
  # ~/.bashrc - executed for interactive non-login shells

  # User-specific aliases
  alias ll='ls -lah --color=auto'
  alias gs='git status'
  alias update='sudo pacman -Syu'

  # Add personal scripts to PATH
  export PATH="$HOME/bin:$PATH"

  # Custom prompt
  export PS1='\u@\h:\w\$ '
  CONF
---
# Environment Variables and the Shell

When you open a terminal on CachyOS, the shell does not start with a blank
slate. It inherits a collection of **environment variables** -- named values
that configure how programs behave, where the shell looks for commands, and what
language your system speaks. Mastering these variables gives you fine-grained
control over your working environment.

## What Is an Environment Variable?

An environment variable is a key-value pair stored in your shell session. Think
of it as a labeled box:

```
KEY=value
```

Programs you launch inherit copies of these variables. For instance, the `LANG`
variable tells applications which language and character set to use, while `HOME`
always points to your home directory.

## Viewing Environment Variables

### List everything with `env` or `printenv`

```bash
env            # prints every exported variable, one per line
printenv       # does the same thing (slightly different heritage)
```

Both produce long lists. Pipe them through `grep` or `sort` to find what you
need:

```bash
env | grep -i lang
printenv | sort | head -20
```

### Print a single variable with `echo` or `printenv`

```bash
echo $HOME           # prints /home/yourname
echo $SHELL          # prints /bin/bash or /usr/bin/fish
printenv HOME        # same result, no $ needed
```

> **Tip:** The `$` prefix is how the shell knows you want the *value* of the
> variable, not the literal word. Without `$`, `echo HOME` just prints the
> letters H-O-M-E.

## Setting Variables

### Shell (local) variables

A plain assignment creates a variable visible only in the current shell:

```bash
greeting="Hello, CachyOS"
echo $greeting          # Hello, CachyOS
bash -c 'echo $greeting'  # (empty -- child process cannot see it)
```

### Exporting to child processes

Use `export` to promote a variable so every program you launch can read it:

```bash
export EDITOR=nano
echo $EDITOR            # nano
bash -c 'echo $EDITOR'  # nano  (child inherits it)
```

You can combine assignment and export in one line:

```bash
export PROJECT_DIR="/home/$USER/projects"
```

### Unsetting a variable

```bash
unset PROJECT_DIR
echo $PROJECT_DIR       # (empty)
```

## The Critical `$PATH` Variable

`$PATH` is the most important environment variable for day-to-day use. It is a
colon-separated list of directories the shell searches -- left to right -- when
you type a command name:

```bash
echo $PATH
# Typical CachyOS output:
# /usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:...
```

### How the shell finds a command

When you type `ls`, the shell checks each directory in `$PATH` in order:

1. `/usr/local/sbin/ls` -- does this file exist and is it executable?
2. `/usr/local/bin/ls` -- what about here?
3. `/usr/bin/ls` -- found it! Run this one.

If no directory contains the command, you get `command not found`.

### Adding a directory to `$PATH`

```bash
export PATH="$HOME/bin:$PATH"     # prepend -- your dir is checked first
export PATH="$PATH:$HOME/bin"     # append -- checked last
```

> **Warning:** Never set `PATH` to just one directory (e.g., `PATH="/my/dir"`).
> You will lose access to all standard commands until you fix it or open a new
> terminal. Always include `$PATH` in the assignment.

### Verify where a command lives

```bash
which pacman        # /usr/bin/pacman
type ls             # ls is aliased to 'ls --color=auto' (common on CachyOS)
```

## Shell Configuration Files

Every time you open a terminal, the shell reads one or more configuration files.
Which files depends on the shell and whether the session is a *login* shell or
an *interactive* shell.

### Bash (default on many CachyOS installs)

| File | When it runs |
|---|---|
| `/etc/profile` | Login shells (system-wide) |
| `~/.bash_profile` or `~/.bash_login` or `~/.profile` | Login shells (user) |
| `~/.bashrc` | Interactive non-login shells |

On CachyOS, most terminal emulators open a non-login interactive shell, so
`~/.bashrc` is the file you will edit most often.

### Fish shell

CachyOS sometimes ships with **fish** as an alternative shell. Fish uses:

| File | Purpose |
|---|---|
| `~/.config/fish/config.fish` | Main user configuration |
| `~/.config/fish/functions/` | Auto-loaded function files |

Fish does *not* use `export VAR=value`. Instead you write:

```fish
set -gx EDITOR nano
```

> **Tip:** To check which shell you are running, use `echo $SHELL` or
> `echo $0` inside the terminal.

### Applying changes with `source`

After editing a config file, you do not need to close and reopen the terminal.
Use `source` to reload it in the current session:

```bash
source ~/.bashrc       # re-read your bashrc right now
# Fish equivalent:
source ~/.config/fish/config.fish
```

The `.` (dot) command is a shorthand for `source` in bash:

```bash
. ~/.bashrc
```

## Creating Aliases

An **alias** is a shortcut name for a longer command. Define them in your shell
config so they persist across sessions:

```bash
alias ll='ls -lah --color=auto'
alias gs='git status'
alias update='sudo pacman -Syu'
alias ..='cd ..'
```

### Viewing current aliases

```bash
alias            # list all defined aliases
alias ll         # show what 'll' expands to
```

### Removing an alias

```bash
unalias ll
```

### Bypassing an alias temporarily

If `ls` is aliased, you can run the real `ls` by prefixing with a backslash:

```bash
\ls               # runs /usr/bin/ls directly, ignoring the alias
```

## Common Environment Variables Reference

| Variable | Typical value | Purpose |
|---|---|---|
| `HOME` | `/home/yourname` | Your home directory |
| `USER` | `yourname` | Current username |
| `SHELL` | `/bin/bash` | Your default shell |
| `PATH` | (colon-separated dirs) | Command search path |
| `EDITOR` | `nano` or `vim` | Default text editor |
| `LANG` | `en_US.UTF-8` | Locale settings |
| `PWD` | (current directory) | Present working directory |
| `TERM` | `xterm-256color` | Terminal type |

## Try It Yourself

1. **Inspect your environment.** Run `env | wc -l` to see how many variables
   are set. Then use `env | grep -i path` to find all PATH-related entries.

2. **Create and export a variable.** Set `MY_PROJECT=/tmp/sandbox` and export
   it. Verify it is visible in a subshell:
   ```bash
   export MY_PROJECT=/tmp/sandbox
   bash -c 'echo $MY_PROJECT'
   ```

3. **Extend your PATH.** Add `~/demo/bin` to your PATH and run the `hello`
   script without its full path:
   ```bash
   export PATH="$HOME/demo/bin:$PATH"
   hello
   ```

4. **Create an alias.** Make a shortcut called `myip` that prints your local
   IP address:
   ```bash
   alias myip='ip -4 addr show | grep inet'
   myip
   ```

5. **Practice `source`.** Edit `~/demo/sample_bashrc` (add an alias), then
   source it and verify the alias works.

> **Key takeaway:** Environment variables shape every command you run. Learning
> to read, set, and persist them through config files is essential for
> customizing your CachyOS system and writing reliable scripts.
