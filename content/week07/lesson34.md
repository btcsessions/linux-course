---
id: 34
week: 7
title: "Networking Basics from the CLI"
duration_minutes: 15
objectives:
  - "Test connectivity with ping and transfer data with curl and wget"
  - "View and understand network configuration with ip addr and ip route"
  - "Diagnose connections with ss, dig, nslookup, and traceroute"
commands: [ping, curl, wget, ip addr, ip route, ss -tlnp, dig, nslookup, traceroute]
prerequisites: []
sandbox_commands: [ip addr, ip route, ss -tlnp, dig, nslookup]
sandbox_setup: |
  # Set up sample files for curl/wget practice
  mkdir -p /tmp/netlab
  echo "Hello from the network lab" > /tmp/netlab/index.html
  echo "sandbox: networking query commands available"
---

# Networking Basics from the CLI

## Why Network Skills Matter

Almost everything a modern computer does involves a network. Whether you are
troubleshooting why a website will not load, checking if a server is reachable,
or configuring a home lab, the command line gives you precise tools that go far
beyond what a browser or settings panel can show you.

In this lesson you will learn the essential networking commands that every Linux
user should know.

## Testing Connectivity with ping

The `ping` command sends a small packet to a remote host and measures the
round-trip time. It is the first tool to reach for when something "is not
working":

```bash
ping -c 4 archlinux.org
```

```
PING archlinux.org (95.217.163.246) 56(84) bytes of data.
64 bytes from 95.217.163.246: icmp_seq=1 ttl=50 time=28.3 ms
64 bytes from 95.217.163.246: icmp_seq=2 ttl=50 time=27.9 ms
64 bytes from 95.217.163.246: icmp_seq=3 ttl=50 time=28.1 ms
64 bytes from 95.217.163.246: icmp_seq=4 ttl=50 time=28.0 ms

--- archlinux.org ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 27.901/28.075/28.304/0.146 ms
```

Key things to look at:

| Field         | Meaning                                     |
|---------------|---------------------------------------------|
| `time`        | Round-trip time in milliseconds             |
| `packet loss` | Percentage of packets that did not return   |
| `ttl`         | Time to live -- how many hops remain        |

**Tip:** On Linux, `ping` runs forever unless you stop it with **Ctrl + C** or
use the `-c` flag to set a count. Always use `-c` in scripts.

### Quick connectivity checks

```bash
ping -c 1 8.8.8.8       # Can I reach the internet at all?
ping -c 1 archlinux.org  # Does DNS resolution work?
```

If the first works but the second does not, your DNS is likely misconfigured.

## Downloading with curl and wget

### curl

`curl` transfers data from (or to) a URL. It is incredibly versatile:

```bash
curl https://example.com
```

This prints the HTML content of the page to your terminal. To save it to a
file:

```bash
curl -o page.html https://example.com
```

To follow redirects (many URLs redirect):

```bash
curl -L -o file.tar.gz https://example.com/download
```

The `-L` flag tells curl to follow HTTP redirects. Without it, you may get an
empty or tiny file instead of the actual download.

### Checking HTTP headers

```bash
curl -I https://archlinux.org
```

The `-I` flag fetches only the headers, which is useful for checking if a
server is responding, what content type it returns, and other metadata.

### wget

`wget` is simpler and purpose-built for downloading files:

```bash
wget https://example.com/file.tar.gz
```

wget automatically saves to the current directory with the remote filename. It
also handles retries and can resume interrupted downloads:

```bash
wget -c https://example.com/largefile.iso
```

The `-c` flag continues a partially downloaded file.

**Tip:** Both `curl` and `wget` are essential tools. `curl` is more flexible
(supports many protocols, can send POST requests, etc.), while `wget` is more
convenient for simple downloads.

## Viewing Network Configuration

### ip addr -- Your network interfaces

```bash
ip addr
```

This shows all network interfaces and their IP addresses:

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    inet 127.0.0.1/8 scope host lo
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet 192.168.1.105/24 brd 192.168.1.255 scope global dynamic enp3s0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    inet 192.168.1.110/24 brd 192.168.1.255 scope global dynamic wlan0
```

| Interface  | What It Is                                   |
|------------|----------------------------------------------|
| `lo`       | Loopback -- the machine talking to itself     |
| `enp3s0`   | Wired Ethernet (name varies by hardware)      |
| `wlan0`    | Wireless interface                            |

The `inet` line shows the IPv4 address and subnet mask in CIDR notation
(e.g., `/24` means a 255.255.255.0 subnet).

### Shorter form

```bash
ip -br addr
```

The `-br` (brief) flag gives a compact one-line-per-interface view:

```
lo               UNKNOWN        127.0.0.1/8
enp3s0           UP             192.168.1.105/24
wlan0            UP             192.168.1.110/24
```

### ip route -- How traffic flows

```bash
ip route
```

```
default via 192.168.1.1 dev enp3s0 proto dhcp metric 100
192.168.1.0/24 dev enp3s0 proto kernel scope link src 192.168.1.105
```

The `default via 192.168.1.1` line tells you your **gateway** -- the router
that sends your traffic to the rest of the internet.

## Examining Open Ports with ss

The `ss` (socket statistics) command replaces the older `netstat`. It shows
which network connections and listening ports exist on your machine:

```bash
ss -tlnp
```

| Flag | Meaning                                      |
|------|----------------------------------------------|
| `-t` | Show TCP sockets only                        |
| `-l` | Show only listening (server) sockets         |
| `-n` | Show numbers instead of resolving names       |
| `-p` | Show the process using each socket            |

```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN  0       128     0.0.0.0:22          0.0.0.0:*          users:(("sshd",pid=892))
LISTEN  0       128     127.0.0.1:631       0.0.0.0:*          users:(("cupsd",pid=1024))
```

This tells you that SSH is listening on port 22 (accessible from anywhere) and
CUPS (the print service) is listening on port 631 (localhost only).

### Checking all connections (not just listening)

```bash
ss -tn
```

This shows active TCP connections -- useful for seeing what your machine is
currently talking to.

## DNS Lookups with dig and nslookup

When you type a domain name like `archlinux.org`, your system needs to
translate it to an IP address. This is DNS (Domain Name System).

### dig

```bash
dig archlinux.org
```

The output includes a lot of detail. The key section is the ANSWER:

```
;; ANSWER SECTION:
archlinux.org.    300    IN    A    95.217.163.246
```

This tells you the domain resolves to IP address `95.217.163.246`.

For a cleaner output:

```bash
dig +short archlinux.org
```

```
95.217.163.246
```

### nslookup

```bash
nslookup archlinux.org
```

```
Server:     127.0.0.53
Address:    127.0.0.53#53

Non-authoritative answer:
Name:   archlinux.org
Address: 95.217.163.246
```

`nslookup` is simpler than `dig` and shows which DNS server answered your
query. Both tools work; `dig` gives more detail, `nslookup` is quicker for
basic lookups.

### Checking which DNS servers you use

```bash
resolvectl status
```

Or look at the classic configuration:

```bash
cat /etc/resolv.conf
```

## Tracing the Route with traceroute

`traceroute` shows every hop your packets take between your machine and a
destination:

```bash
traceroute archlinux.org
```

```
 1  router.local (192.168.1.1)      1.234 ms
 2  isp-gateway (10.0.0.1)         12.456 ms
 3  core-router.isp.net (203.0.113.1) 15.789 ms
 ...
12  archlinux.org (95.217.163.246)  28.123 ms
```

Each line is a router (hop) along the path. This is invaluable for diagnosing
where exactly a connection is failing or slowing down.

**Tip:** Some routers are configured to not respond to traceroute, showing
`* * *` instead. This does not necessarily mean a problem.

If `traceroute` is not installed:

```bash
sudo pacman -S traceroute
```

## A Diagnostic Workflow

When something network-related is not working, follow this sequence:

1. **Can I reach my router?**
   ```bash
   ping -c 2 192.168.1.1
   ```

2. **Can I reach the internet by IP?**
   ```bash
   ping -c 2 8.8.8.8
   ```

3. **Can I resolve DNS names?**
   ```bash
   dig +short archlinux.org
   ```

4. **Can I reach a website?**
   ```bash
   curl -I https://archlinux.org
   ```

If step 1 fails, your local network or interface is down. If step 2 fails but
1 works, there is a routing or ISP issue. If step 3 fails but 2 works, DNS is
the problem. This systematic approach saves you hours of guessing.

## Quick Reference

| Task                          | Command                            |
|-------------------------------|------------------------------------|
| Test if a host is reachable   | `ping -c 4 host`                  |
| Download a file               | `wget URL` or `curl -o file URL`  |
| Fetch HTTP headers            | `curl -I URL`                      |
| Show IP addresses             | `ip addr` or `ip -br addr`        |
| Show routing table            | `ip route`                         |
| Show listening ports          | `ss -tlnp`                         |
| DNS lookup                    | `dig +short domain`                |
| DNS lookup (simple)           | `nslookup domain`                  |
| Trace network path            | `traceroute host`                  |

## Try It Yourself

1. Ping `archlinux.org` four times and note the average round-trip time:
   ```bash
   ping -c 4 archlinux.org
   ```

2. Look up your machine's IP address:
   ```bash
   ip -br addr
   ```

3. Find your default gateway:
   ```bash
   ip route | grep default
   ```

4. Check which ports are currently listening on your system:
   ```bash
   sudo ss -tlnp
   ```

5. Do a DNS lookup for `cachyos.org`:
   ```bash
   dig +short cachyos.org
   ```

6. Fetch only the HTTP headers from a website:
   ```bash
   curl -I https://cachyos.org
   ```

7. Download a small file with wget:
   ```bash
   wget -O /tmp/test.html https://example.com
   ```

8. Trace the route to a remote server and count the hops:
   ```bash
   traceroute archlinux.org
   ```
