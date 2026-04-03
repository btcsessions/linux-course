---
id: 22
week: 5
title: "Regular Expressions for grep"
duration_minutes: 15
objectives:
  - "Use anchors ^ and $ to match line beginnings and endings"
  - "Build character classes with [abc], [0-9], and negation [^...]"
  - "Apply quantifiers with grep -E: +, ?, {n,m}"
  - "Combine regex elements to write precise search patterns"
commands: [grep -E, egrep]
prerequisites: []
sandbox_commands: [grep, cat, ls, cd, pwd, echo, touch, mkdir, cp, head, tail, less, find, wc, sort, uniq, cut, whoami, date, clear, file, egrep]
sandbox_setup: |
  echo "john.doe@email.com" > data.txt
  echo "jane_smith@company.org" >> data.txt
  echo "Phone: 555-123-4567" >> data.txt
  echo "Phone: 555-987-6543" >> data.txt
  echo "IP: 192.168.1.1" >> data.txt
  echo "IP: 10.0.0.255" >> data.txt
  echo "Date: 2024-01-15" >> data.txt
  echo "Date: 2024-12-31" >> data.txt
  echo "Price: \$19.99" >> data.txt
  echo "Price: \$142.50" >> data.txt
  echo "# This is a comment" >> data.txt
  echo "  # Indented comment" >> data.txt
  echo "Normal line of text" >> data.txt
  echo "Another normal line" >> data.txt
  echo "ERROR: file not found" >> data.txt
  echo "warning: low disk space" >> data.txt
  echo "INFO: process started" >> data.txt
  echo "3 apples" >> data.txt
  echo "15 oranges" >> data.txt
  echo "200 bananas" >> data.txt
  echo "Practice regex!" > README.txt
---

# Regular Expressions for grep

## What Are Regular Expressions?

In the previous lesson you used `grep` with simple text patterns. Regular
expressions (regex) take that to the next level -- they let you describe
*patterns* rather than exact strings. Instead of searching for the literal word
"error", you can search for "any line that starts with a date, followed by a
space, followed by ERROR or WARN".

Regular expressions are used not just in `grep`, but in `sed`, `awk`, Python,
JavaScript, and countless other tools. Learning them here pays off everywhere.

## Basic vs Extended Regular Expressions

GNU `grep` supports two flavors of regex:

- **Basic Regular Expressions (BRE)** -- the default. Some special characters
  like `+`, `?`, `{`, `}`, `(`, `)` must be escaped with backslashes.
- **Extended Regular Expressions (ERE)** -- enabled with `grep -E` (or the
  equivalent command `egrep`). These characters work without backslashes.

**Tip:** In practice, most people use `grep -E` because it is less cluttered
and easier to read. This lesson focuses on extended regular expressions.

## Anchors: Pinning Patterns to Positions

Anchors do not match characters -- they match *positions* in a line.

### ^ -- Start of Line

```bash
grep "^error" /tmp/regex-practice/data.txt
```

```
error: file not found
```

Only lines that *begin* with "error" (lowercase) match. Lines like "ERROR:" or
lines with "error" in the middle are excluded.

### $ -- End of Line

```bash
grep "com$" /tmp/regex-practice/data.txt
```

```
alice@example.com
```

This matches lines that *end* with "com".

### Combining Anchors

To match a line that contains *exactly* "abc" and nothing else:

```bash
grep "^abc$" /tmp/regex-practice/data.txt
```

```
abc
```

The `^` and `$` together ensure there is nothing before or after "abc".

## Character Classes

Character classes let you match any *one* character from a set.

### Basic Character Class: [...]

```bash
grep "[Ee]rror" /tmp/regex-practice/data.txt
```

```
error: file not found
Error: permission denied
```

The pattern `[Ee]rror` matches either "Error" or "error". Notice that "ERROR"
does not match because only the first letter is flexible.

### Ranges Inside Character Classes

Instead of listing every character, use a dash to specify a range:

| Pattern    | Matches                          |
|------------|----------------------------------|
| `[0-9]`    | Any single digit                 |
| `[a-z]`    | Any lowercase letter             |
| `[A-Z]`    | Any uppercase letter             |
| `[a-zA-Z]` | Any letter, upper or lower       |
| `[0-9a-f]` | Any hexadecimal digit            |

```bash
grep "[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]" /tmp/regex-practice/data.txt
```

```
123-45-6789
```

This crude pattern matches strings shaped like "NNN-NN-NNNN".

### Negated Character Classes: [^...]

A caret *inside* square brackets means "anything except these characters":

```bash
grep "[^a-z]" /tmp/regex-practice/data.txt
```

This matches any line containing at least one character that is NOT a lowercase
letter. Since almost every line has spaces, digits, or uppercase letters, most
lines match.

A more useful example:

```bash
grep "^[^#]" /etc/pacman.conf
```

This shows all lines in `pacman.conf` that do **not** start with a `#` comment.

## The Dot: Any Character

The `.` (dot) matches any single character except a newline:

```bash
grep "a.c" /tmp/regex-practice/data.txt
```

```
abc
adc
```

This matches "abc", "adc", and anything else with a character between "a" and
"c". It does NOT match "ac" because the dot requires exactly one character.

## Quantifiers with grep -E

Quantifiers control *how many times* the preceding element can repeat. This is
where `grep -E` (extended regex) shines.

### * -- Zero or More

The `*` matches zero or more of the preceding character:

```bash
grep -E "ab*c" /tmp/regex-practice/data.txt
```

```
abc
abbc
abbbc
ac
```

The pattern `ab*c` means "a", then zero or more "b"s, then "c". So it matches
"ac", "abc", "abbc", "abbbc", and so on.

### + -- One or More

The `+` matches one or more of the preceding character:

```bash
grep -E "ab+c" /tmp/regex-practice/data.txt
```

```
abc
abbc
abbbc
```

Notice "ac" is gone -- the `+` requires at least one "b".

### ? -- Zero or One

The `?` makes the preceding character optional:

```bash
grep -E "colou?r" /tmp/regex-practice/data.txt
```

This would match both "color" and "colour" -- the "u" is optional.

### {n,m} -- Specific Repetition

Curly braces let you specify exact counts:

| Pattern    | Meaning                                  |
|------------|------------------------------------------|
| `{3}`      | Exactly 3 times                          |
| `{2,4}`    | Between 2 and 4 times                    |
| `{2,}`     | 2 or more times                          |

```bash
grep -E "[0-9]{3}-[0-9]{2}-[0-9]{4}" /tmp/regex-practice/data.txt
```

```
123-45-6789
```

This is a cleaner version of the earlier pattern. It reads naturally: "three
digits, dash, two digits, dash, four digits."

## Alternation: OR Patterns

The pipe `|` in extended regex means "or":

```bash
grep -E "ERROR|WARN" /tmp/regex-practice/data.txt
```

This matches lines containing either "ERROR" or "WARN".

You can group alternatives with parentheses:

```bash
grep -E "(ERROR|WARN|error)" /tmp/regex-practice/data.txt
```

```
error: file not found
ERROR: connection refused
```

## Putting It Together: Real Examples

### Find Lines That Look Like Email Addresses

```bash
grep -E "[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-z]{2,}" /tmp/regex-practice/data.txt
```

```
alice@example.com
bob.smith@company.org
charlie123@domain.net
```

This pattern means: one or more alphanumeric characters (or dots), then `@`,
then one or more alphanumeric characters, then a literal dot, then two or more
lowercase letters.

### Find IP-Address-Like Strings

```bash
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" /tmp/regex-practice/data.txt
```

```
IP: 192.168.1.1
IP: 10.0.0.255
IP: 999.999.999.999
```

**Warning:** This finds strings that *look* like IP addresses but does not
validate them. 999.999.999.999 matched because the pattern only checks the
format, not the values. True IP validation requires more complex logic.

### Find Version Numbers

```bash
grep -E "[0-9]+\.[0-9]+\.[0-9]+" /tmp/regex-practice/data.txt
```

```
version 1.0.0
version 2.11.3
version 10.0.1-beta
```

### Find Lines Starting with a Date

```bash
grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}" /tmp/regex-practice/data.txt
```

```
2026-03-15 server started
2026-13-45 invalid date
```

## Common Mistakes

1. **Forgetting to use -E for extended regex.** Without `-E`, characters like
   `+`, `?`, `{`, and `|` are treated as literals.

2. **Not escaping literal dots.** The pattern `192.168.1.1` actually matches
   `192X168Y1Z1` because unescaped dots match any character. Use `192\.168\.1\.1`.

3. **Confusing `^` outside and inside brackets.** Outside `[]`, the caret means
   "start of line." Inside `[^...]`, it means "not these characters."

4. **Greedy matching surprises.** Quantifiers like `*` and `+` are greedy -- they
   match as much as possible. This usually does not matter with `grep` (which
   prints entire lines) but becomes important in `sed` and `awk`.

## CachyOS-Specific Notes

CachyOS ships with GNU grep, which supports both BRE and ERE. The `egrep`
command is available as a shortcut for `grep -E`, though it is considered
deprecated in favor of `grep -E`. Both work identically on CachyOS.

A practical CachyOS example -- find all enabled repositories in pacman.conf:

```bash
grep -E "^\[" /etc/pacman.conf | grep -v "options"
```

## Try It Yourself

Practice these exercises using the sandbox files:

1. Find all lines in `data.txt` that start with "phone":
   ```bash
   grep "^phone" /tmp/regex-practice/data.txt
   ```

2. Find all email addresses (lines containing `@`):
   ```bash
   grep "@" /tmp/regex-practice/data.txt
   ```

3. Find lines that end with a three-letter TLD (.com, .org, .net):
   ```bash
   grep -E "\.[a-z]{3}$" /tmp/regex-practice/data.txt
   ```

4. Use a character class to match both "Error" and "error":
   ```bash
   grep "[Ee]rror" /tmp/regex-practice/data.txt
   ```

5. Find all lines containing "ab" followed by one or more "b"s:
   ```bash
   grep -E "ab{2,}" /tmp/regex-practice/data.txt
   ```

6. Use alternation to find lines with either "ERROR" or "error":
   ```bash
   grep -E "ERROR|error" /tmp/regex-practice/data.txt
   ```

7. Find version numbers in the format X.Y.Z:
   ```bash
   grep -E "[0-9]+\.[0-9]+\.[0-9]+" /tmp/regex-practice/data.txt
   ```

8. Challenge: Write a pattern that matches phone numbers in any of the formats
   shown in the file (555-1234, (555) 867-5309).

In the next lesson, you will learn `sed`, which uses these same regular
expressions to not just *find* text, but *transform* it.
