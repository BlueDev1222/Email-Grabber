<div align="center">

# 🕵️ AutoEmailGrabber

### *Fully Autonomous OSINT Email Harvester for Authorized Penetration Testing*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.1.1bugfix-orange.svg)](https://github.com/BlueDev1222/Email-Grabber/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/BlueDev1222/Email-Grabber/pulls)




__ _       _          ____                 _     _
/ \ | | | ___ / | __ __ _ _ __ | | () __ _ \ | | | | | / _ \ | | _| '/  | '_ \| '_ \| |/ _ | \ \ | || | || () || || | | | (| | |) | | | | | (| | _/|_,|__/ _|| _,| ./|| |||_, | || |/





**Just open the file. That's it. No commands. No setup. No input required.**

---

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Output Format](#-output-format)
- [Customization](#-customization)
- [Data Sources](#-data-sources)
- [Anti-Detection](#-anti-detection)
- [Dependencies](#-dependencies)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Legal & Ethics](#-legal--ethics)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**AutoEmailGrabber** is a fully autonomous, self-starting OSINT (Open Source Intelligence) tool designed for **authorized penetration testers, security researchers, and bug bounty hunters**. It automatically discovers and extracts email addresses from public sources with zero user input.

Unlike traditional email harvesters that require you to manually specify URLs, run terminal commands, or configure complex settings — **AutoEmailGrabber just works**. You open it, it scans, and you get results.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🤖 Fully Autonomous** | No input required. No URLs to type. No commands to run. |
| **🚀 Self-Starting** | Double-click the file and it runs. Auto-installs dependencies. |
| **🌐 Multi-Source Scanning** | Crawls websites, checks CT logs, searches PGP keyservers, probes common paths. |
| **📄 Clean Output** | Saves all results to `emails_found.txt` — organized, deduplicated, and ready to open in VS Code. |
| **🧹 Smart Filtering** | Automatically removes system emails (noreply, donotreply), duplicates, and invalid addresses. |
| **🛡️ Anti-Detection** | Randomized user agents, polite delays, and respectful crawling to avoid blocking. |
| **📦 Auto-Install** | If dependencies are missing, it installs them automatically. No pip commands needed. |
| **🎨 ASCII Banner** | Displays a professional version banner with tool name, version, and GitHub repo on startup. |
| **🔧 Fully Customizable** | Add your own targets, adjust crawl depth, change delays — all in one config section. |

---

## ⚙️ How It Works

AutoEmailGrabber performs a multi-phase reconnaissance scan:

### Phase 1: Website Crawling
- Crawls the target organization's website using BFS (Breadth-First Search)
- Extracts emails from HTML content, `mailto:` links, JavaScript, and obfuscated text
- Follows internal links up to configurable depth

### Phase 2: Common Path Probing
- Checks predictable endpoints known to leak emails:
  - `/contact`, `/about`, `/team`, `/people`, `/staff`
  - `/.well-known/security.txt`, `/humans.txt`
  - `/wp-json/wp/v2/users/` (WordPress user enumeration)

### Phase 3: Certificate Transparency Logs
- Queries [crt.sh](https://crt.sh) for SSL/TLS certificates issued to the target domain
- Certificates often contain email addresses in SAN (Subject Alternative Name) fields

### Phase 4: PGP Keyserver Lookup
- Searches public PGP keyservers for email addresses associated with the target domain

### Phase 5: Results Processing
- Deduplicates and validates all collected emails
- Filters out system addresses (`noreply@`, `donotreply@`, etc.)
- Groups results by domain
- Writes clean, formatted output to file

---

## 🚀 Quick Start

### The 10-Second Guide

```
# 1. Download the script
wget https://raw.githubusercontent.com/BlueDev1222/Email-Grabber/main/auto_email_grabber.py

# 2. Run it
python auto_email_grabber.py
OR just double-click the file.

That's it. The script handles everything else.
```

📦 Installation
Option 1: Clone the Repository




git clone https://github.com/YOUR_USERNAME/AutoEmailGrabber.git
cd AutoEmailGrabber
python auto_email_grabber.py
Option 2: Download the Single File




wget https://raw.githubusercontent.com/YOUR_USERNAME/AutoEmailGrabber/main/auto_email_grabber.py
python auto_email_grabber.py
Option 3: Just Double-Click (Windows/Mac/Linux)
Save auto_email_grabber.py to your desktop
Double-click it
Watch it work
🎮 Usage



# Run with default settings (scans 10 built-in targets)
python auto_email_grabber.py
There are no command-line arguments. The tool is intentionally designed to require zero configuration. All settings are configured in-script (see Customization).

What Happens When You Run



1. ASCII banner displays with version info
2. Dependencies are checked and auto-installed if missing
3. Scan begins across all targets (10 websites by default)
4. Each target is crawled, paths are checked, CT logs & PGP queried
5. Progress is shown in real-time
6. Results are saved to emails_found.txt
7. Summary is printed to console
8. Script pauses until you press Enter (so you can read output)
📄 Output Format
The results file (emails_found.txt) is formatted for immediate readability:




======================================================================
  AutoEmailGrabber — Scan Results
  Version: 2.1.0
  Date: 2026-06-25 14:30:22
  Total Unique Emails: 47
======================================================================

  ── github.com (12 emails) ──

    admin@github.com
    support@github.com
    security@github.com
    press@github.com
    ...

  ── google.com (8 emails) ──

    press@google.com
    adsense@google.com
    ...

  ── microsoft.com (6 emails) ──

    mshelp@microsoft.com
    ...

======================================================================
  END OF REPORT
======================================================================
Open it in VS Code:

bash



code emails_found.txt
🔧 Customization
All configuration is at the top of the script in the clearly marked section:

python



# ============================================================
# CONFIGURATION
# ============================================================
OUTPUT_FILE = "emails_found.txt"        # Output file name
MAX_PAGES_PER_SITE = 30                 # Pages to crawl per domain
MAX_DOMAINS = 10                        # How many domains to scan
CRAWL_DEPTH = 2                         # Link depth to follow
REQUEST_DELAY = 1.0                     # Seconds between requests
TIMEOUT = 10                            # Request timeout in seconds
Adding Your Own Targets
Replace the AUTO_TARGETS list with your own:

python



AUTO_TARGETS = [
    {"name": "Your Company",      "domain": "yourcompany.com",      "url": "https://www.yourcompany.com"},
    {"name": "Client Project",    "domain": "clientdomain.com",     "url": "https://www.clientdomain.com"},
]
Adjusting Scan Depth
MAX_PAGES_PER_SITE: Higher = more thorough, slower. Lower = faster, less coverage.
CRAWL_DEPTH: 1 = only the starting page. 2 = starting page + linked pages. 3 = deeper.
REQUEST_DELAY: Increase if you're getting rate-limited. Decrease for faster scans.
📡 Data Sources


Source	Method	Coverage
Target Website	BFS Crawl + HTML Parsing	All pages within domain up to max depth
Common Paths	HTTP GET to known endpoints	/contact, /team, /about, /.well-known/security.txt, /wp-json/wp/v2/users/
Certificate Transparency	crt.sh API	All SSL/TLS certificates ever issued for the domain
PGP Keyservers	Ubuntu keyserver search	Public PGP keys containing the domain
🛡️ Anti-Detection
AutoEmailGrabber includes several features to minimize detection and blocking:

Randomized User Agents — Each request uses a random browser signature from a pool of modern browsers
Polite Delays — Configurable delay between requests (default: 1 second)
Respectful Crawling — Limits depth and total pages to avoid overwhelming servers
Session Handling — Uses persistent sessions for consistent crawling
📚 Dependencies
AutoEmailGrabber automatically installs these if missing:



Library	Version	Purpose
requests	Latest	HTTP requests and web scraping
beautifulsoup4	Latest	HTML parsing and DOM navigation
lxml	Latest	Fast HTML/XML parser for BeautifulSoup
pyfiglet	Latest	ASCII art banner generation
No manual installation required. The script handles it.

🗺️ Roadmap
Future planned features:

 SOCKS5/Proxy Support — Route traffic through proxies for anonymity
 Tor Integration — Optional routing through Tor network
 Multi-threaded Crawling — Faster scans with parallel requests
 Export Formats — JSON, CSV, HTML report generation
 Built-in Domain List — 100+ common bug bounty targets
 Wayback Machine Integration — Historical email extraction
 Shodan/Hunter.io API Support — Optional paid API integrations
 Docker Support — Containerized deployment
 Web UI — Simple local web interface for results
 
❓ FAQ
Is this legal?
This tool is designed for authorized penetration testing only. You must have explicit permission before scanning any target. See the Legal & Ethics section.

Do I need to install Python?
Yes, Python 3.7+ is required. Most systems have it pre-installed. If not, download it from python.org.

Will I get blocked?
The tool uses polite delays and randomized user agents. However, aggressive scanning may trigger rate limiting. Adjust REQUEST_DELAY if needed.

Can I scan my own targets?
Yes! Edit the AUTO_TARGETS list in the script to add any domains you're authorized to test.

Why does it come with built-in targets?
The built-in targets (Google, Microsoft, GitHub, etc.) are well-known companies with public bug bounty programs and are used for demonstration and testing purposes only. Replace them with your own authorized targets.

How do I open the results in VS Code?
bash



code emails_found.txt
Or just double-click the file.

Does it work on Windows?
Yes. Python runs on all platforms. Double-clicking .py files works on Windows if Python is installed.

⚖️ Legal & Ethics
⚠️ IMPORTANT — READ THIS FIRST

AutoEmailGrabber is an OSINT tool for authorized security professionals only.

Acceptable Use
✅ Testing your own infrastructure
✅ Authorized penetration tests with written permission
✅ Bug bounty programs where you are registered
✅ Security research on systems you own
Unacceptable Use
❌ Scanning systems without authorization
❌ Harvesting emails for spam or phishing
❌ Violating any applicable laws (CFAA, GDPR, Computer Misuse Act, etc.)
❌ Any use that could harm individuals or organizations
Disclaimer
The author assumes no liability for misuse of this tool. Users are solely responsible for complying with all local, state, and federal laws. By using this software, you agree to use it only for lawful, authorized purposes.

🤝 Contributing
Contributions are welcome! Here's how:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
Development Guidelines
Keep it simple — zero configuration philosophy
Maintain Python 3.7+ compatibility
Add comments for all major functions
Update the version number in the script
Test on all platforms if possible
