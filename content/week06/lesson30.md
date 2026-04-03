---
id: 30
week: 6
title: "Shell History and Efficiency"
duration_minutes: 15
objectives:
  - "Navigate and search command history with history, Ctrl+R, !!, and !$"
  - "Use command substitution with $() to embed command output"
  - "Chain commands with &&, ||, and ; for conditional and sequential execution"
commands: [history, "Ctrl+R", "!!", "!$", "!n", "$()", "$(( ))", "&&", "||"]
prerequisites: []
sandbox_commands: [history, echo, cat, ls, grep, date, wc, mkdir, touch, basename, cd, pwd, sort, head, tail, find, whoami, clear, sed, awk]
sandbox_setup: |
  mkdir -p project/src project/docs
  echo "main code" > project/src/main.py
  echo "utils code" > project/src/utils.py
  echo "readme" > project/docs/README.md
  touch file1.txt file2.txt file3.txt
  echo "Practice history and efficiency!" > README.txt
---
# Shell History and Efficiency

A fast Linux user is not someone who types faster -- it is someone who types
*less*. The bash shell remembers every command you run and provides powerful
shortcuts to recall, edit, and reuse them. Combine that with command
substitution and conditional chaining, and you can accomplish in one line what
used to take five.

## Command History

### The `history` command

Bash saves every command you type to an in-memory list and, when the session
ends, writes it to `~/.bash_history`. To see your recent commands:

```bash
history          # show all remembered commands (numbered)
history 20       # show only the last 20 entries
```

Each line has a number on the left:

```
  501  ls -la
  502  cd /var/log
  503  grep error syslog
  504  cat /etc/hostname
```

You can control how many commands are saved:

```bash
echo $HISTSIZE       # max entries in memory (often 1000)
echo $HISTFILESIZE   # max entries in ~/.bash_history (often 2000)
```

> **Tip:** Add these lines to your `~/.bashrc` if you want a longer history:
> ```bash
> export HISTSIZE=10000
> export HISTFILESIZE=20000
> ```

### Searching history with Ctrl+R

Press **Ctrl+R** to start a **reverse incremental search**. As you type, bash
finds the most recent command matching your input:

```
(reverse-i-search)`grep': grep error syslog
```

- **Ctrl+R** again: jump to the next older match.
- **Enter**: execute the displayed command.
- **Ctrl+G** or **Esc**: cancel and return to an empty prompt.
- **Arrow keys**: edit the displayed command before running it.

This is one of the most time-saving features in the shell. Practice it until
it becomes muscle memory.

### Searching with `grep`

For a more targeted search:

```bash
history | grep ssh          # find all commands that mention ssh
history | grep -i pacman    # case-insensitive search for pacman commands
```

## History Expansion Shortcuts

Bash provides bang (`!`) shortcuts to reuse parts of previous commands without
retyping them.

### `!!` -- repeat the entire last command

```bash
pacman -Syu
# "error: you cannot perform this operation unless you are root."
sudo !!
# expands to: sudo pacman -Syu
```

This is the classic "oops, I forgot sudo" trick.

### `!$` -- the last argument of the previous command

```bash
mkdir -p /tmp/my_project/src
cd !$
# expands to: cd /tmp/my_project/src
```

This avoids retyping long paths.

### `!n` -- run command number n from history

```bash
history | tail -5
#  501  ls -la
#  502  cd /var/log
#  503  grep error syslog

!503
# re-runs: grep error syslog
```

### `!string` -- run the most recent command starting with *string*

```bash
!grep           # re-runs the last command that started with "grep"
!cat            # re-runs the last command that started with "cat"
```

> **Warning:** `!string` runs the command immediately without confirmation. If
> you are not sure which command it will match, use `!string:p` to print it
> first without executing.

### `!*` -- all arguments of the previous command

```bash
echo one two three
cat !*
# expands to: cat one two three
```

### Quick substitution with `^old^new`

```bash
cat /etc/hostnme
# Oops, typo!
^hostnme^hostname
# re-runs: cat /etc/hostname
```

## Command Substitution with `$()`

Command substitution lets you embed the output of one command inside another.
The shell runs the inner command first, captures its stdout, and pastes the
result into the outer command.

```bash
echo "Today is $(date +%A)"
# Today is Thursday
```

```bash
echo "There are $(ls /etc | wc -l) items in /etc"
# There are 247 items in /etc
```

### Practical uses

**Create a timestamped backup:**

```bash
cp important.conf important.conf.$(date +%Y%m%d)
# creates important.conf.20260327
```

**Loop over command output:**

```bash
for host in $(cat ~/demo/hosts.txt); do
  echo "Pinging $host..."
done
```

**Nested substitution:**

```bash
echo "Kernel: $(uname -r) on $(hostname)"
```

### The older backtick syntax

You may see backticks used for the same purpose:

```bash
echo "User: `whoami`"
```

The `$()` form is preferred because it nests cleanly and is easier to read.
Avoid backticks in new scripts.

## Arithmetic Expansion with `$(( ))`

For integer math, use double parentheses:

```bash
echo $(( 5 + 3 ))        # 8
echo $(( 100 / 4 ))      # 25
echo $(( 2 ** 10 ))      # 1024

files=$(ls ~/demo | wc -l)
echo "Double: $(( files * 2 ))"
```

Supported operators: `+`, `-`, `*`, `/`, `%` (modulo), `**` (exponent).

## Chaining Commands: `&&`, `||`, and `;`

### Sequential execution with `;`

The semicolon runs commands one after another, regardless of success or failure:

```bash
echo "Starting" ; sleep 1 ; echo "Done"
```

Even if the middle command fails, the third one still runs.

### Conditional AND with `&&`

The `&&` operator runs the next command **only if the previous one succeeded**
(exit code 0):

```bash
mkdir /tmp/build && cd /tmp/build && echo "Ready to build"
```

If `mkdir` fails (directory already exists with wrong permissions), `cd` and
`echo` are skipped. This is safer than `;` because it stops at the first error.

### Conditional OR with `||`

The `||` operator runs the next command **only if the previous one failed**
(non-zero exit code):

```bash
cd /nonexistent || echo "Directory does not exist!"
```

### Combining `&&` and `||`

A common pattern for simple if/else logic on one line:

```bash
ping -c 1 8.8.8.8 > /dev/null 2>&1 && echo "Online" || echo "Offline"
```

> **Warning:** This is not a perfect replacement for `if/else`. If the
> `&&` command itself fails, the `||` part also runs. Use real `if` statements
> in scripts for complex logic.

### Grouping commands

Use braces to group commands that share the same condition:

```bash
mkdir /tmp/test && { echo "Created"; cd /tmp/test; echo "Moved in"; }
```

> **Note:** The closing brace must be preceded by `;` or a newline, and there
> must be a space after `{`.

## Putting It All Together

Here is a one-liner that combines several techniques from this lesson:

```bash
# Find large log files, back them up with a timestamp, then report
find /var/log -name "*.log" -size +1M 2>/dev/null \
  && echo "Backup at $(date +%H:%M)" \
  || echo "No large logs found"
```

And a practical CachyOS update workflow:

```bash
sudo pacman -Syu && echo "Update complete at $(date)" || echo "Update failed!"
```

## Fish Shell Notes

If you are using fish on CachyOS, some syntax differs:

- History search: Use **Ctrl+R** or the built-in up-arrow search.
- `!!` and `!$` do not work in fish by default. Install the `bang-bang` plugin
  via `fisher` for this functionality.
- Command substitution uses parentheses: `(date +%A)` instead of `$(date +%A)`.
- `&&` and `||` work in fish 3.0+.

## Try It Yourself

1. **Explore your history.** Run `history | tail -20` to see your recent
   commands. Then use `Ctrl+R` and type `echo` to find a previous echo command.

2. **Practice `!!`.** Run `cat /etc/hostname`, then immediately run `echo "!!"` to
   see how the expansion works.

3. **Use `!$` for paths.** Create a directory and cd into it in two steps:
   ```bash
   mkdir -p /tmp/test_history
   cd !$
   ```

4. **Command substitution.** Create a file named with today's date:
   ```bash
   touch ~/demo/backup_$(date +%Y%m%d).txt
   ls ~/demo/backup_*.txt
   ```

5. **Chain commands.** Write a one-liner that tries to create a directory and
   reports success or failure:
   ```bash
   mkdir /tmp/chain_test && echo "Success" || echo "Failed"
   ```

6. **Arithmetic.** Calculate how many total lines are in all the log files:
   ```bash
   echo "Total lines: $(cat ~/demo/log_*.txt | wc -l)"
   ```

> **Key takeaway:** The shell rewards the lazy -- in a good way. History
> shortcuts, command substitution, and smart chaining let you do more with
> fewer keystrokes. Invest a little time learning these tricks and they will
> pay dividends every day.
