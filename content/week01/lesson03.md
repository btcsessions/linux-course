---
id: 3
week: 1
title: "Navigating with cd"
duration_minutes: 15
objectives:
  - "Change directories using absolute and relative paths"
  - "Use the shortcuts ~, ., .., and - to navigate efficiently"
  - "Leverage tab completion to save time and avoid typos"
commands: [cd, cd ~, cd .., cd -, cd /absolute/path]
prerequisites: [2]
sandbox_commands: [cd, pwd, ls, whoami, hostname, date, cal, clear, echo, cat]
sandbox_setup: |
  mkdir -p projects/website/css projects/website/js projects/website/images
  mkdir -p projects/app/src projects/app/tests
  mkdir -p documents/work documents/personal
  mkdir -p pictures/vacation pictures/family
  echo "body { color: red; }" > projects/website/css/style.css
  echo "console.log('hello');" > projects/website/js/app.js
  echo "index page" > projects/website/index.html
  echo "main code" > projects/app/src/main.py
  echo "test code" > projects/app/tests/test_main.py
  echo "Work report" > documents/work/report.txt
  echo "Shopping list" > documents/personal/shopping.txt
  echo "Beach photo" > pictures/vacation/beach.jpg
  echo "Family photo" > pictures/family/dinner.jpg
  echo "Welcome to the sandbox!" > README.txt
---

# Navigating with cd

## Moving Around the Filesystem

In the previous lesson you learned how to find out where you are with `pwd`. Now
it is time to learn how to **move**. The command that changes your location in
the filesystem is `cd`, which stands for **change directory**.

`cd` is probably the command you will use more often than any other. Mastering it
will make everything else faster and more comfortable.

## Basic Usage

The simplest form of `cd` takes one argument -- the directory you want to move
to:

```bash
cd /var/log
```

After running that command, your working directory changes. Verify it:

```bash
pwd
```

```
/var/log
```

Your prompt will also update to reflect the new location:

```
alex@cachyos /var/log $
```

## Using Absolute Paths

An absolute path starts from the root `/` and describes the full route to a
directory. You can always use an absolute path with `cd`, no matter where you
currently are:

```bash
cd /home/alex/Documents
cd /etc
cd /usr/share/man
```

Absolute paths are reliable because they never depend on your current location.
They are like giving a full street address -- they work from anywhere.

## Using Relative Paths

A relative path describes where to go starting from your current directory. If
you are in `/home/alex` and want to enter the `Documents` directory inside it,
you do not need to type the full path:

```bash
cd Documents
```

That is equivalent to:

```bash
cd /home/alex/Documents
```

You can chain directories in a relative path:

```bash
cd projects/website/css
```

If you are in `/home/alex`, this takes you to `/home/alex/projects/website/css`.

**Tip:** Use relative paths for nearby directories and absolute paths when you
need to jump to a completely different part of the tree.

## The Parent Directory: ..

Two dots (`..`) represent the **parent directory** -- the directory one level
above your current location.

If you are in `/home/alex/Documents`:

```bash
cd ..
```

Takes you to `/home/alex`.

You can chain `..` to climb multiple levels:

```bash
cd ../..
```

From `/home/alex/Documents`, this takes you to `/home` (up two levels).

You can also combine `..` with directory names:

```bash
cd ../pictures
```

From `/home/alex/Documents`, this goes up to `/home/alex` and then down into
`pictures`, landing you in `/home/alex/pictures`.

This is extremely useful when you need to move between sibling directories
without typing out long absolute paths.

## The Current Directory: .

A single dot (`.`) represents the current directory. By itself with `cd` it does
nothing useful:

```bash
cd .
```

You are still in the same place. However, `.` matters when you run scripts or
reference files:

```bash
./my_script.sh
```

This means "run `my_script.sh` in the current directory." You will encounter
this pattern frequently.

## The Home Directory: ~

The tilde (`~`) is a shortcut for your home directory. These are all equivalent:

```bash
cd ~
cd $HOME
cd /home/alex
cd
```

Yes, that last one -- `cd` with **no arguments at all** -- also takes you home.
It is the fastest way to get back to your home directory from anywhere.

```bash
pwd
```

```
/var/log
```

```bash
cd
pwd
```

```
/home/alex
```

You can also use `~` as part of a longer path:

```bash
cd ~/Documents/school
```

This works from any location because `~` is an absolute reference to your home.

**Tip:** You can reference another user's home directory with `~username`:

```bash
cd ~maria
```

This takes you to `/home/maria` (assuming you have permission to access it).

## The Previous Directory: -

The dash (`-`) is one of the most underappreciated shortcuts. It takes you back
to the **previous directory** you were in:

```bash
cd /etc
cd /var/log
cd -
```

After running `cd -`, you are back in `/etc`. Run it again and you return to
`/var/log`. It toggles you between two directories.

This is incredibly useful when you are working in two directories at once --
say, editing a configuration file in `/etc` and checking logs in `/var/log`.

```bash
cd -
```

```
/etc
```

```bash
cd -
```

```
/var/log
```

The shell also prints the directory it switched to, so you always know where
you ended up.

## Tab Completion

This is the feature that will save you the most time. Instead of typing a full
directory name, you can type the first few characters and press **Tab**:

```bash
cd Doc<Tab>
```

The shell completes it to:

```bash
cd Documents/
```

If there are multiple matches, pressing Tab twice shows you the options:

```bash
cd D<Tab><Tab>
```

```
Desktop/    Documents/  Downloads/
```

Then type one or two more characters to narrow it down and press Tab again.

Tab completion works in **bash**, **zsh**, and **fish**. In fact, fish has
particularly excellent tab completion with color-coded suggestions that appear
as you type.

**Tip:** Use Tab religiously. It is faster, prevents typos, and confirms that
the directory actually exists. If Tab does not complete anything, the directory
name you started typing probably does not exist in the current location.

Tab completion also works for commands, filenames, and in many shells even
command options:

```bash
host<Tab>        ->  hostname
```

## Common Mistakes and How to Fix Them

### Mistake 1: Spaces in directory names

If a directory name has spaces, you must quote it or escape the space:

```bash
cd "My Documents"
cd My\ Documents
```

Without quotes or the backslash, the shell thinks you are passing two separate
arguments.

### Mistake 2: Forgetting where you are

You try `cd Documents` but get an error. Run `pwd` -- you might not be where you
think you are. The `Documents` directory only exists relative to your home.

### Mistake 3: Confusing / and ~

`cd /` takes you to the root of the entire filesystem. `cd ~` takes you to your
home directory. They are very different places.

**Warning:** Running commands in `/` (the root directory) as root is dangerous.
A careless `rm -rf *` there would destroy your entire system. Always check where
you are with `pwd` before running destructive commands.

## A Practical Navigation Session

Let us walk through a realistic sequence of commands:

```bash
pwd                          # Where am I?
/home/alex

cd Documents                 # Go into Documents
pwd
/home/alex/Documents

cd school/math               # Go deeper
pwd
/home/alex/Documents/school/math

cd ..                        # Back up one level
pwd
/home/alex/Documents/school

cd ../../projects            # Up two levels, then into projects
pwd
/home/alex/projects

cd ~/Documents               # Jump straight to Documents from anywhere
pwd
/home/alex/Documents

cd -                         # Back to previous (projects)
pwd
/home/alex/projects

cd                           # Go home
pwd
/home/alex
```

Notice how each method has its strengths. Absolute paths for big jumps, relative
paths for nearby moves, `..` for going up, `~` for going home, and `-` for
toggling.

## CachyOS-Specific Notes

- If you are using the **fish** shell on CachyOS, tab completion is even more
  powerful -- fish suggests completions as you type, before you even press Tab.
  You can accept a suggestion by pressing the right arrow key.
- fish also abbreviates long paths in the prompt. For example, it might show
  `~/D/s/math` instead of `~/Documents/school/math`.
- The `cd` command works identically in bash, zsh, and fish, so everything in
  this lesson applies regardless of which shell CachyOS has set as your default.

## Try It Yourself

Use the sandbox to practice navigating. Try these exercises:

1. Run `pwd` to see where you start.
2. Use `cd /tmp/sandbox` to jump to the sandbox directory.
3. Run `ls` to see what directories are available.
4. Navigate into `projects/website/css` using a relative path.
5. Run `pwd` to confirm your location.
6. Use `cd ..` to go back to the `website` directory.
7. Use `cd ../python-app/src` to move to a sibling project's source directory.
8. Use `cd ~` to return home, then `cd -` to jump back to where you were.
9. Navigate to `/tmp/sandbox/documents/school/math` using an absolute path.
10. Use `cd ../../work` to get to the work directory from math.
11. Practice tab completion: type `cd /tmp/sand<Tab>` and watch it complete.
12. Use `cd` (with no arguments) to go home from wherever you are.

You now have all the tools you need to move confidently through the Linux
filesystem. In the next lesson we will explore how to see what is inside each
directory with the `ls` command.
