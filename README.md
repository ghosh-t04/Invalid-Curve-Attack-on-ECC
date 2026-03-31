# Comparative ECC Point Validation Attack & Prevention Study (P-256)

A Python-based educational cybersecurity project that demonstrates how improper validation of elliptic curve points can lead to **private key leakage** in ECC implementations.

This project implements **Elliptic Curve Cryptography (ECC) from scratch** (without cryptographic libraries) using the **real-world NIST P-256 curve**, and compares multiple attack strategies and prevention mechanisms using a **Tkinter GUI**.



## Project Overview

Elliptic Curve Cryptography (ECC) is widely used in:

- TLS / HTTPS
- Digital signatures
- Cryptocurrency systems
- Secure messaging
- Embedded and IoT security

Many ECC implementations assume that received public points are valid.  
If an attacker sends a **malicious or invalid point**, some vulnerable implementations may still perform scalar multiplication:

\[
Q = d \cdot P
\]

where:
- `d` = victim's private key
- `P` = attacker-controlled point

This can leak information about the private key.

This project demonstrates:

- **Invalid Curve Attack**
- **Small Subgroup Attack**
- **Twist-Style Malicious Point Attack**
- Prevention using:
  - Curve Equation Validation
  - Subgroup Validation
  - Combined Validation



## Features

- ECC arithmetic implemented **from scratch**
- Uses **real-world 256-bit curve (NIST P-256 / secp256r1)**
- Tkinter GUI for easy demonstration
- Multiple attack simulations
- Multiple prevention mechanisms
- Automated **25 test cases per attack**
- Attack success comparison
- Graph-based analysis
- Before vs After prevention evaluation



## What This Project Demonstrates

### Attacks
1. **Invalid Curve Attack**
2. **Small Subgroup Attack**
3. **Twist Attack (simulated malicious-point attack)**

### Defenses
1. **Curve Equation Check**
2. **Subgroup Validation**
3. **Combined Validation (recommended)**

### Metrics Visualized
- Attack Success Rate
- Confidentiality Preservation
- Time vs Key Size
- Latency Overhead
- Defense Comparison
- Security Improvement


## Project Structure

```text
Invalid-Curve-ECC/
│
├── ecc_core.py        # ECC math, attacks, validations, prevention logic
├── gui.py             # Tkinter GUI + logs + graph generation
├── README.md          # Project documentation
````

---

## Technologies Used

* **Python 3**
* **Tkinter** (GUI)
* **Matplotlib** (Graphs)

No external cryptographic library is used for ECC core operations.



## ECC Curve Used

This project uses the **NIST P-256** elliptic curve (also called **secp256r1**), which is a real-world curve used in:

* browsers
* operating systems
* SSL/TLS stacks
* enterprise PKI systems

### Curve Equation

[
y^2 \equiv x^3 + ax + b \pmod p
]

This project implements:

* modular inverse
* point addition
* point doubling
* scalar multiplication
* curve validation

from scratch using standard Python arithmetic.



## How to Run This Project Locally

## 1) Prerequisites

Make sure you have:

* **Python 3.9+** installed
* Windows / Linux / macOS
* `pip` available

Check Python version:

```bash
python --version
```

or on some systems:

```bash
python3 --version
```



## 2) Clone or Download the Project

If using Git:

```bash
git clone <your-repo-url>
cd Invalid-Curve-ECC
```

Or simply download the ZIP and extract it.



## 3) (Recommended) Create a Virtual Environment

### On Windows (PowerShell)

```bash
python -m venv venv
venv\Scripts\activate
```

### On Windows (Command Prompt)

```bash
python -m venv venv
venv\Scripts\activate.bat
```

### On Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4) Install Required Packages

Install matplotlib:

```bash
pip install matplotlib
```
 
## 5) Run the GUI

From the project folder:

```bash
python gui.py
```

A GUI window should open.

---

# GUI Usage Guide

The application contains **exactly four main buttons**:

---

## 1. **Generate Keys / Parameters**

This will:

* generate a **256-bit ECC private key**
* generate the corresponding **public key**
* initialize the ECC environment
* reset all previous results
* set the system to **VULNERABLE** mode

### Status:

**Red** → Vulnerable

---

## 2. **Run Attack**

This runs the full attack suite automatically:

* Invalid Curve Attack
* Small Subgroup Attack
* Twist Attack

Each attack runs **25 automated test cases**.

### Output includes:

* whether malicious points are accepted
* whether leakage occurs
* what information is leaked (e.g. `d mod m`)
* attack success rate

Before prevention, the success rate should be **high**.

---

## 3. **Apply Prevention**

This enables **Combined Validation**, which includes:

* Curve Equation Check
* Subgroup Validation

### Status:

**Green** → Secure

After this, malicious points should be rejected.

---

## 4. **Show Graphs**

Displays multiple graphs including:

* Before vs After Attack Success Rate
* Time vs Key / Parameter Size
* Confidentiality Before vs After Prevention
* Attack vs Prevention Latency Overhead
* Defense Performance Comparison
* Security Improvement

---

# Recommended Demo Flow

Use this order when running the project:

### Step 1

Click:

```text
Generate Keys / Parameters
```

### Step 2

Click:

```text
Run Attack
```

Observe:

* red vulnerable logs
* leakage messages
* high success rate

### Step 3

Click:

```text
Apply Prevention
```

Observe:

* system changes to secure mode
* green secure logs

### Step 4

Click:

```text
Run Attack
```

Observe:

* malicious points rejected
* attack success becomes **0%**

### Step 5

Click:

```text
Show Graphs
```

Observe all comparative visual analysis.

---

# Expected Results

## Before Prevention

* High attack success
* Malicious points accepted
* Private key residues leaked
* Low confidentiality

## After Prevention

* Malicious points rejected
* 0% attack success
* High confidentiality
* Small latency overhead

---

# Mathematical Background

ECC scalar multiplication computes:

[
Q = d \cdot P
]

where:

* `d` = private key
* `P` = point on the elliptic curve

If an attacker supplies a **malicious point** of small order `m`, then:

[
mP = \mathcal{O}
]

So:

[
dP = (d \bmod m)P
]

This means the attacker can learn:

[
d \bmod m
]

Repeating this with different points can reveal increasing information about the private key.

---

## Prevention Logic

A secure ECC implementation should validate any received point before using it.

### 1. Curve Equation Check

Verify:

[
y^2 \equiv x^3 + ax + b \pmod p
]

### 2. Subgroup Check

Verify:

[
nP = \mathcal{O}
]

where `n` is the order of the correct subgroup.

### 3. Combined Validation

Use **both checks** before scalar multiplication.

---

# Main Files Explained

## `ecc_core.py`

Contains:

* ECC parameters (P-256)
* modular inverse
* point addition
* scalar multiplication
* key generation
* malicious point generation
* attack simulation logic
* prevention logic

---

## `gui.py`

Contains:

* Tkinter interface
* buttons and event handlers
* text logs
* red / green security indicators
* graph generation
* before/after comparison

---

# Important Academic Note

This project is intended for:

* cybersecurity education
* ECC vulnerability analysis
* academic demonstration
* secure implementation awareness

This project does **not** claim to break production-grade P-256 deployments in real-world hardened cryptographic libraries.

Instead, it demonstrates how **missing point validation** can create serious vulnerabilities in ECC-based systems.

---

# Troubleshooting

## 1) `ModuleNotFoundError: No module named 'matplotlib'`

Install matplotlib:

```bash
pip install matplotlib
```

---

## 2) Tkinter not found

### Windows

Tkinter is usually included with standard Python installation.

Reinstall Python from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

Make sure **"tcl/tk and IDLE"** is selected during installation.

### Ubuntu / Debian

Install Tkinter:

```bash
sudo apt-get install python3-tk
```

### macOS

If using Homebrew Python:

```bash
brew install python-tk
```

---

## 3) GUI does not open

Make sure you are running:

```bash
python gui.py
```

from the correct project folder.

---

## 4) Attack success seems low

Make sure you:

1. Click **Generate Keys / Parameters**
2. Run attacks **before** applying prevention

If you enable prevention first, attacks will be blocked.

---


# Quick Start (Short Version)

```bash
python -m venv venv
venv\Scripts\activate
pip install matplotlib
python gui.py
```

Then in GUI:

1. Generate Keys / Parameters
2. Run Attack
3. Apply Prevention
4. Run Attack again
5. Show Graphs

---

# End Result

This project helps demonstrate:

* why ECC point validation matters
* how malicious ECC inputs can leak secrets
* how secure validation blocks these attacks
* how security and performance can be compared visually




