---
id: 35
week: 7
title: "systemd Services and Logs on CachyOS"
duration_minutes: 15
objectives:
  - "Start, stop, enable, and check the status of services with systemctl"
  - "Read and filter system logs with journalctl"
  - "Understand CachyOS boot process and common services"
commands: [systemctl status, systemctl start, systemctl enable, systemctl list-units, journalctl, journalctl -u, journalctl -f]
prerequisites: []
sandbox_commands: [cat, ls, grep, echo, head, tail, wc, cd, pwd, find, sort, whoami, date, clear, sed, awk, cut, less]
sandbox_setup: |
  echo "systemd commands must be run in your real terminal." > README.txt
  echo "" >> README.txt
  echo "Key commands to try in CachyOS:" >> README.txt
  echo "  systemctl status sshd" >> README.txt
  echo "  systemctl list-units --type=service" >> README.txt
  echo "  journalctl -u NetworkManager --no-pager -n 20" >> README.txt
  echo "" >> README.txt
  echo "Sample journalctl output:" > sample_journal.txt
  echo "Jan 15 10:00:01 cachyos systemd[1]: Started NetworkManager." >> sample_journal.txt
  echo "Jan 15 10:00:02 cachyos NetworkManager[450]: <info> starting..." >> sample_journal.txt
  echo "Jan 15 10:00:03 cachyos NetworkManager[450]: <info> WiFi enabled" >> sample_journal.txt
  echo "Jan 15 10:00:05 cachyos NetworkManager[450]: <info> connected to MyWiFi" >> sample_journal.txt
---

# systemd Services and Logs on CachyOS

## What Is systemd?

When your CachyOS machine boots, something needs to start the kernel, mount
your filesystems, launch your network, start your display manager, and bring
up dozens of other services in the right order. That something is **systemd**.

systemd is the **init system** and service manager used by CachyOS (and most
modern Linux distributions). It is the very first process that runs (PID 1) and
it manages everything else from that point on.

The two main tools for interacting with systemd are:

- **systemctl** -- manage services (start, stop, enable, status)
- **journalctl** -- read the system journal (logs)

## Understanding Services (Units)

In systemd terminology, a **unit** is anything that systemd manages. The most
common type is a **service** -- a background program (daemon) that runs
continuously. Examples:

| Service                | What It Does                         |
|------------------------|--------------------------------------|
| `sshd.service`         | SSH server for remote login          |
| `NetworkManager.service` | Manages network connections        |
| `bluetooth.service`    | Bluetooth daemon                     |
| `cups.service`         | Print server                         |
| `sddm.service`        | Display manager (CachyOS login screen) |

Other unit types include `.timer` (scheduled tasks), `.mount` (mount points),
`.socket` (network sockets), and `.target` (groups of units).

## Checking Service Status

The first thing to do when troubleshooting a service:

```bash
systemctl status sshd
```

```
● sshd.service - OpenSSH Daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: disabled)
     Active: active (running) since Fri 2026-03-27 08:12:34 EDT; 6h ago
   Main PID: 892 (sshd)
      Tasks: 1 (limit: 19051)
     Memory: 3.2M
        CPU: 42ms
     CGroup: /system.slice/sshd.service
             └─892 "sshd: /usr/sbin/sshd -D"

Mar 27 08:12:34 cachyos systemd[1]: Started OpenSSH Daemon.
```

Key information:

| Field     | Meaning                                          |
|-----------|--------------------------------------------------|
| `Loaded`  | Where the unit file lives and if it is enabled   |
| `Active`  | Current state -- running, stopped, failed        |
| `Main PID`| Process ID of the service                        |
| `Memory`  | Current memory usage                             |

The status also shows the most recent log lines for that service.

### Possible states

| State                | Meaning                                      |
|----------------------|----------------------------------------------|
| `active (running)`   | The service is running normally               |
| `active (exited)`    | The service ran and finished (one-shot)       |
| `inactive (dead)`    | The service is not running                    |
| `failed`             | The service tried to start and crashed        |
| `enabled`            | Will start automatically at boot              |
| `disabled`           | Will not start at boot (manual only)          |

## Starting and Stopping Services

### Start a service now

```bash
sudo systemctl start sshd
```

This starts the service immediately. It will not survive a reboot unless it is
also enabled.

### Stop a service now

```bash
sudo systemctl stop sshd
```

### Restart a service

```bash
sudo systemctl restart sshd
```

Useful after changing a service's configuration file. The service stops and
starts again.

### Reload configuration without restarting

Some services support reloading their config without a full restart:

```bash
sudo systemctl reload nginx
```

Not all services support this. If unsure:

```bash
sudo systemctl reload-or-restart nginx
```

## Enabling and Disabling Services

### Enable -- start at boot

```bash
sudo systemctl enable sshd
```

This creates a symlink so systemd starts the service every time the system
boots. It does **not** start it right now.

### Enable and start immediately

```bash
sudo systemctl enable --now sshd
```

The `--now` flag is a shortcut that enables the service **and** starts it in
one command.

### Disable -- do not start at boot

```bash
sudo systemctl disable sshd
```

This removes the boot-time symlink. The service can still be started manually.

### Disable and stop

```bash
sudo systemctl disable --now sshd
```

## Listing Services

### All loaded units

```bash
systemctl list-units --type=service
```

This shows every service that systemd currently has loaded, along with its
state.

### Only running services

```bash
systemctl list-units --type=service --state=running
```

### Only failed services

```bash
systemctl list-units --type=service --state=failed
```

This is a great first check when something is not working. If a critical
service has failed, you will see it here.

### All installed service files

```bash
systemctl list-unit-files --type=service
```

This shows every service file on disk, whether or not it is loaded, and
whether it is enabled or disabled.

## CachyOS Common Services

CachyOS comes with several services enabled by default:

| Service                    | Purpose                              |
|----------------------------|--------------------------------------|
| `NetworkManager.service`   | Network connection management        |
| `sddm.service`            | Login/display manager (KDE default)  |
| `bluetooth.service`        | Bluetooth support                    |
| `cups.service`             | Printing                             |
| `fstrim.timer`             | Periodic SSD TRIM for performance    |
| `reflector.timer`          | Auto-update pacman mirror list       |
| `systemd-timesyncd.service`| Network time synchronization         |

CachyOS may also have its own helper services for things like kernel parameter
optimization. You can find them with:

```bash
systemctl list-units --type=service | grep -i cachy
```

## Reading Logs with journalctl

systemd collects logs from all services into a single **journal**. The
`journalctl` command is your window into these logs.

### View all logs (newest at bottom)

```bash
journalctl
```

This opens a pager (like `less`). Press **q** to quit, **G** to jump to the
end, **/** to search.

### View logs for a specific service

```bash
journalctl -u sshd
```

The `-u` flag filters by unit name. This is how you troubleshoot a specific
service.

### Follow logs in real time

```bash
journalctl -f
```

This works like `tail -f` -- new log entries appear as they happen. Press
**Ctrl + C** to stop.

To follow only one service:

```bash
journalctl -fu NetworkManager
```

### Logs from this boot only

```bash
journalctl -b
```

To see logs from the previous boot (useful for diagnosing why a reboot
happened):

```bash
journalctl -b -1
```

### Logs from a specific time range

```bash
journalctl --since "2026-03-27 08:00" --until "2026-03-27 12:00"
```

Or using relative times:

```bash
journalctl --since "1 hour ago"
```

### Filter by priority

systemd logs have priority levels from 0 (emergency) to 7 (debug):

| Priority | Level     |
|----------|-----------|
| 0        | emerg     |
| 1        | alert     |
| 2        | crit      |
| 3        | err       |
| 4        | warning   |
| 5        | notice    |
| 6        | info      |
| 7        | debug     |

To see only errors and above:

```bash
journalctl -p err
```

To see only errors from this boot:

```bash
journalctl -b -p err
```

### Check journal disk usage

```bash
journalctl --disk-usage
```

If the journal is consuming too much space, you can limit it:

```bash
sudo journalctl --vacuum-size=500M
```

This removes old entries until the journal is under 500 MB.

## Diagnosing Boot Problems

### See how long the boot took

```bash
systemd-analyze
```

```
Startup finished in 2.345s (firmware) + 1.234s (loader) + 2.567s (kernel) + 4.891s (userspace) = 11.037s
```

### See which services were slowest to start

```bash
systemd-analyze blame | head -10
```

This lists services sorted by how long they took to start. If your boot is
slow, this reveals the culprits.

### Boot timeline plot

```bash
systemd-analyze plot > /tmp/boot.svg
```

Open the SVG file in a browser for a visual timeline of the boot process.

## Creating a Simple Custom Service

You can create your own systemd service. For example, a script that runs at
startup:

Create the script:

```bash
sudo tee /usr/local/bin/hello-boot.sh << 'EOF'
#!/bin/bash
echo "System booted at $(date)" >> /var/log/hello-boot.log
EOF
sudo chmod +x /usr/local/bin/hello-boot.sh
```

Create the service file:

```bash
sudo tee /etc/systemd/system/hello-boot.service << 'EOF'
[Unit]
Description=Hello Boot Logger
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/hello-boot.sh

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hello-boot.service
```

Check that it worked:

```bash
systemctl status hello-boot.service
cat /var/log/hello-boot.log
```

## Quick Reference

| Task                          | Command                                |
|-------------------------------|----------------------------------------|
| Check service status          | `systemctl status sshd`                |
| Start a service               | `sudo systemctl start sshd`            |
| Stop a service                | `sudo systemctl stop sshd`             |
| Restart a service             | `sudo systemctl restart sshd`          |
| Enable at boot                | `sudo systemctl enable sshd`           |
| Enable + start now            | `sudo systemctl enable --now sshd`     |
| List running services         | `systemctl list-units --type=service`  |
| List failed services          | `systemctl list-units --state=failed`  |
| View all logs                 | `journalctl`                           |
| Logs for a service            | `journalctl -u sshd`                   |
| Follow live logs              | `journalctl -f`                        |
| This boot only                | `journalctl -b`                        |
| Errors only                   | `journalctl -p err`                    |
| Boot time analysis            | `systemd-analyze blame`                |

## Try It Yourself

1. Check the status of the NetworkManager service:
   ```bash
   systemctl status NetworkManager
   ```

2. List all currently running services:
   ```bash
   systemctl list-units --type=service --state=running
   ```

3. Check if any services have failed:
   ```bash
   systemctl list-units --type=service --state=failed
   ```

4. View the last 20 log entries for the SSH daemon:
   ```bash
   journalctl -u sshd -n 20
   ```

5. Check errors from this boot:
   ```bash
   journalctl -b -p err
   ```

6. Follow the system log in real time (press Ctrl+C to stop):
   ```bash
   journalctl -f
   ```

7. See how long your system took to boot:
   ```bash
   systemd-analyze
   ```

8. Find the five slowest services during boot:
   ```bash
   systemd-analyze blame | head -5
   ```
