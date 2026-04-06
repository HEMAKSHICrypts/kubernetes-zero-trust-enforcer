# Zero‑Trust Auto Enforcer for Kubernetes

One‑command demo that deploys a pod, simulates an attacker, and detects the compromise in real time.

## How it works
- Creates an nginx pod (if not exists).
- Spawns a background attacker thread that creates a marker file (`/tmp/compromised`) after 10 seconds.
- Monitors for the marker file every 5 seconds.
- Raises a clear alert when found.

## Why this matters
Runtime detection of indicators of compromise (IoCs) is the foundation of zero‑trust security in cloud native environments.

## Run it yourself
```bash
# Requires kubectl and a Kubernetes cluster (e.g., Docker Desktop with Kubernetes enabled)
python auto_enforcer.py

## 🚀 How to Run (One Terminal, One Command)

1. **Open PowerShell** (or VS Code terminal) as **Administrator**.
2. **Navigate to the folder**:
   ```bash
   cd C:\ZeroTrust-AutoEnforcer

Example Output
🚨🚨🚨 SECURITY ALERT 🚨🚨🚨
Pod web-app-... has been compromised!
Indicator: /tmp/compromised found.
Action: Pod should be isolated immediately.


Author
HEMAKSHI C -CISCO CERTIFIED(Introduction to Cybersecurity)
