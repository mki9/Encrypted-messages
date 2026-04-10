<div align="center">

# 🔐 G.I.D SECURE MESSENGER
### End-to-End Encrypted Agent Communication System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Encryption](https://img.shields.io/badge/Encryption-RSA--2048%20%2B%20Fernet-green?style=for-the-badge&logo=shield)](https://cryptography.io)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)
[![Author](https://img.shields.io/badge/Developer-mki9-purple?style=for-the-badge&logo=ghost)](https://github.com/mki9)

> *"No plain text ever leaves your device."*

</div>

---

## 📡 Overview

**G.I.D Secure Messenger** is a terminal-based, peer-to-peer encrypted chat system built with a client-server architecture. Every message is protected using a hybrid **RSA-2048 + Fernet (AES-128)** encryption scheme, ensuring full end-to-end encryption (E2EE) — the server **never** sees message content.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔑 **RSA-2048 Key Exchange** | Each client generates a unique keypair on launch |
| 🔒 **Fernet Symmetric Encryption** | Messages encrypted with a per-session AES key |
| 📬 **Offline Mailbox** | Messages buffered server-side and delivered on reconnect |
| 🕵️ **Agent Identity System** | Agents register with custom IDs and public keys |
| 🖥️ **Terminal UI** | Centered, colored interface powered by Colorama |
| 🔔 **Audio Notifications** | Bell sound on incoming message |
| 🧵 **Multi-threaded** | Simultaneous send/receive without blocking |

---

## 🛡️ How Encryption Works

```
SENDER SIDE:
  1. Generate a random Fernet (AES) session key
  2. Encrypt the message with the session key
  3. Encrypt the session key with TARGET's RSA-2048 public key
  4. Send: [ RSA_ENCRYPTED_SESSION_KEY || FERNET_ENCRYPTED_MESSAGE ]

RECEIVER SIDE:
  1. Decrypt session key using own RSA private key
  2. Decrypt message using session key
  3. Original plaintext revealed — only on receiver's device
```

> ⚠️ The server only routes encrypted blobs — it **cannot** read any message.

---

## 📁 Project Structure

```
GID-Secure-Messenger/
│
├── server.py          # Central relay server (key registry + message router)
├── client.py          # Agent client (E2EE send/receive + terminal UI)
└── README.md          # You are here
```

---

## ⚙️ Requirements

```bash
pip install cryptography colorama
```

| Package | Purpose |
|---|---|
| `cryptography` | RSA-2048 key generation, OAEP encryption, Fernet AES |
| `colorama` | Colored terminal output (cross-platform) |

---

## 🚀 Getting Started

### 1. Run the Server

```bash
python server.py
```

The server listens on port `5555` by default and displays registered agents in real time.

### 2. Run the Client

```bash
python client.py
```

On launch, the client will:
- Generate a fresh RSA-2048 keypair
- Ask for your **Agent ID**
- Connect to the server and register your public key
- Ask for the **Target Agent ID** to start a secure session

### 3. Chat

```
[SECURE INPUT] >> Hello, this message is fully encrypted.
[SENT] 2048-BIT ENCRYPTED PACKET.
```

---

## 🌐 Server Configuration

By default, the client connects to a public tunnel. To use your own server, edit in `client.py`:

```python
SERVER_IP = 'your.server.ip'
SERVER_PORT = 5555
```

---

## 🔧 Architecture

```
┌──────────────┐         ┌─────────────────────┐         ┌──────────────┐
│   AGENT A    │         │     G.I.D SERVER     │         │   AGENT B    │
│              │─REGISTER─▶  Key Registry       │         │              │
│  RSA KeyPair │◀─GET KEY──  Public Key Store   │◀─REGISTER  RSA KeyPair │
│              │──MSG─────▶  Message Router     │──MSG────▶│              │
└──────────────┘         └─────────────────────┘         └──────────────┘
       ▲                     (sees only blobs)                    ▲
       └──────────────── E2EE — Server is blind ─────────────────┘
```

---

## ⚠️ Disclaimer

This project is built for **educational purposes** to demonstrate applied cryptography and network programming concepts.  
Use responsibly and in compliance with applicable laws.

---

## 🛠️ Tool

<div align="center">

```
 ███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗███████╗██████╗ 
 ██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
 █████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   █████╗  ██████╔╝
 ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══╝  ██╔══██╗
 ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   ███████╗██║  ██║
 ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝

 ███╗   ███╗███████╗███████╗███████╗ █████╗  ██████╗ ███████╗███████╗
 ████╗ ████║██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔════╝
 ██╔████╔██║█████╗  ███████╗███████╗███████║██║  ███╗█████╗  ███████╗
 ██║╚██╔╝██║██╔══╝  ╚════██║╚════██║██╔══██║██║   ██║██╔══╝  ╚════██║
 ██║ ╚═╝ ██║███████╗███████║███████║██║  ██║╚██████╔╝███████╗███████║
 ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ 
```

**mki9**  
Security Enthusiast · Python Developer · Crypto Systems

[![GitHub](https://img.shields.io/badge/GitHub-mki9-black?style=flat-square&logo=github)](https://github.com/mki9)

</div>

---

<div align="center">

Made with 🔐 by **mki9**  
*"Stay encrypted. Stay invisible."*

</div>
