#!/usr/bin/env python3
"""
AutoEmailGrabber v2.0 — Fully Autonomous & Self-Starting
For Authorized Penetration Testing Only
Just open/double-click the file. That's it.
"""

# ============================================================
# SELF-START — This makes it run automatically on open
# ============================================================
import subprocess
import sys
import os

# Check if we have dependencies, install if missing
def ensure_dependencies():
    try:
        import requests
        import bs4
    except ImportError:
        print("[*] Installing dependencies automatically...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "lxml", "--quiet"])
        print("[*] Dependencies installed. Continuing...\n")

ensure_dependencies()

# ============================================================
# Now import everything
# ============================================================
import re
import requests
import time
import random
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
OUTPUT_FILE = "emails_found.txt"
MAX_PAGES_PER_SITE = 30
MAX_DOMAINS = 10
CRAWL_DEPTH = 2
REQUEST_DELAY = 1.0
TIMEOUT = 10

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
EXCLUDE_PATTERNS = [
    r'noreply', r'no-reply', r'donotreply', r'do-not-reply',
    r'example\.com', r'example\.org', r'@\[', r'@localhost',
    r'@test', r'@fake', r'@invalid', r'@domain',
    r'@sentry', r'@log', r'@error',
    r'wordpress', r'gravatar',
]

# ============================================================
# BUILT-IN TARGETS
# ============================================================
AUTO_TARGETS = [
    {"name": "Google",      "domain": "google.com",      "url": "https://www.google.com/about/"},
    {"name": "Microsoft",   "domain": "microsoft.com",   "url": "https://www.microsoft.com/en-us/"},
    {"name": "GitHub",      "domain": "github.com",      "url": "https://github.com/about"},
    {"name": "Meta",        "domain": "meta.com",        "url": "https://about.meta.com/"},
    {"name": "Apple",       "domain": "apple.com",       "url": "https://www.apple.com/contact/"},
    {"name": "Amazon",      "domain": "amazon.com",      "url": "https://www.amazon.com/contact/"},
    {"name": "Netflix",     "domain": "netflix.com",     "url": "https://www.netflix.com/"},
    {"name": "Twitter/X",   "domain": "twitter.com",     "url": "https://about.twitter.com/"},
    {"name": "LinkedIn",    "domain": "linkedin.com",    "url": "https://about.linkedin.com/"},
    {"name": "Reddit",      "domain": "reddit.com",      "url": "https://www.reddit.com/about/"},
]

# ============================================================
# CORE FUNCTIONS
# ============================================================

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
    }


def is_valid_email(email):
    email = email.strip().lower()
    if email.count('@') != 1:
        return False
    if len(email) < 6 or len(email) > 254:
        return False
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, email, re.IGNORECASE):
            return False
    parts = email.split('.')
    if len(parts[-1]) < 2:
        return False
    local, domain = email.split('@')
    if not local or not domain:
        return False
    if domain.count('.') < 1:
        return False
    return True


def extract_emails(text):
    found = set()
    for email in EMAIL_REGEX.findall(str(text)):
        if is_valid_email(email):
            found.add(email.lower())
    return found


def scrape_page(url, domain):
    emails = set()
    links = []
    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=get_headers(), timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('mailto:'):
                e = href[7:].split('?')[0].strip()
                if is_valid_email(e):
                    emails.add(e.lower())
            full = urljoin(url, href)
            parsed = urlparse(full)
            if domain in parsed.netloc and parsed.scheme in ('http', 'https'):
                links.append(parsed.scheme + '://' + parsed.netloc + parsed.path)

        emails |= extract_emails(soup.get_text())
        for script in soup.find_all('script'):
            if script.string:
                emails |= extract_emails(script.string)

        return emails, links
    except Exception:
        return emails, links


def crawl_domain(start_url, domain, max_pages=30, max_depth=2):
    found = set()
    to_visit = deque([(start_url, 0)])
    visited = set()

    print(f"\n{'='*60}")
    print(f"  Scanning: {domain}")
    print(f"  Starting: {start_url}")
    print(f"{'='*60}")

    while to_visit and len(visited) < max_pages:
        url, depth = to_visit.popleft()
        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        emails, links = scrape_page(url, domain)
        if emails:
            new_emails = emails - found
            if new_emails:
                found |= new_emails
                for e in sorted(new_emails):
                    print(f"    [+] {e}")
                print(f"    → Page {len(visited)}/{max_pages}: {len(new_emails)} new email(s)")

        if depth < max_depth:
            for link in links:
                if link not in visited and link not in [u for u, _ in to_visit]:
                    to_visit.append((link, depth + 1))

    print(f"  [{len(visited)} pages crawled] → {len(found)} total emails")
    return found


def try_crtsh(domain):
    emails = set()
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, headers=get_headers(), timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data[:100]:
                name = entry.get('name_value', '')
                emails |= extract_emails(name)
    except:
        pass
    return emails


def try_pgp(domain):
    emails = set()
    try:
        url = "https://keyserver.ubuntu.com/pks/lookup"
        params = {"search": domain, "op": "index", "fingerprint": "on"}
        resp = requests.get(url, params=params, headers=get_headers(), timeout=TIMEOUT)
        if resp.status_code == 200:
            emails |= extract_emails(resp.text)
    except:
        pass
    return emails


def check_common_paths(url, domain):
    paths = [
        "/contact", "/contact-us", "/about", "/about-us", "/team", "/people",
        "/staff", "/company", "/support", "/help",
        "/.well-known/security.txt", "/humans.txt",
        "/wp-json/wp/v2/users/",
    ]
    emails = set()
    base = url.rstrip('/')
    for path in paths:
        try:
            time.sleep(0.3)
            full = base + path
            resp = requests.get(full, headers=get_headers(), timeout=TIMEOUT)
            if resp.status_code == 200:
                found = extract_emails(resp.text)
                if found:
                    emails |= found
                    print(f"    [*] {path}: {len(found)} email(s)")
        except:
            continue
    return emails


def write_results(all_emails, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("  AutoEmailGrabber — Scan Results\n")
        f.write(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"  Total Unique Emails: {len(all_emails)}\n")
        f.write("=" * 70 + "\n\n")

        if not all_emails:
            f.write("  No emails found.\n")
            return

        by_domain = {}
        for email in sorted(all_emails):
            domain = email.split('@')[1]
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(email)

        for domain in sorted(by_domain.keys()):
            f.write(f"\n  ── {domain} ({len(by_domain[domain])} emails) ──\n\n")
            for email in by_domain[domain]:
                f.write(f"    {email}\n")
            f.write("\n")

        f.write("=" * 70 + "\n")
        f.write("  END OF REPORT\n")
        f.write("=" * 70 + "\n")

    print(f"\n  ✓ Results saved to: {output_file}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║              AutoEmailGrabber v2.0                  ║
║         Fully Autonomous — Self-Starting            ║
║   Just open the file. No commands needed.           ║
║   Authorized Penetration Testing Only               ║
╚══════════════════════════════════════════════════════╝
    """)

    all_emails = set()
    count = min(MAX_DOMAINS, len(AUTO_TARGETS))

    print(f"  Targets: {count} websites")
    print(f"  Pages per site: {MAX_PAGES_PER_SITE}")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"{'='*60}\n")

    for i, target in enumerate(AUTO_TARGETS[:count], 1):
        print(f"\n[{i}/{count}] {target['name']} ({target['domain']})")

        site_emails = crawl_domain(
            target['url'],
            target['domain'],
            max_pages=MAX_PAGES_PER_SITE,
            max_depth=CRAWL_DEPTH
        )
        all_emails |= site_emails

        print(f"  Checking common paths...")
        path_emails = check_common_paths(target['url'], target['domain'])
        if path_emails:
            print(f"    → {len(path_emails)} from common paths")
        all_emails |= path_emails

        print(f"  Querying CT logs...")
        ct_emails = try_crtsh(target['domain'])
        if ct_emails:
            print(f"    → {len(ct_emails)} from CT logs")
        all_emails |= ct_emails

        print(f"  Querying PGP keyservers...")
        pgp_emails = try_pgp(target['domain'])
        if pgp_emails:
            print(f"    → {len(pgp_emails)} from PGP keyservers")
        all_emails |= pgp_emails

        print(f"\n  ── Running total: {len(all_emails)} unique emails ──")

    print(f"\n{'='*60}")
    print(f"  SCAN COMPLETE")
    print(f"  Total unique emails found: {len(all_emails)}")
    print(f"{'='*60}")

    write_results(all_emails, OUTPUT_FILE)

    if all_emails:
        by_domain = {}
        for email in sorted(all_emails):
            d = email.split('@')[1]
            by_domain.setdefault(d, []).append(email)

        print(f"\n  Summary by domain:")
        for d in sorted(by_domain.keys()):
            print(f"    {d}: {len(by_domain[d])} emails")

        print(f"\n  Sample emails:")
        for email in list(sorted(all_emails))[:10]:
            print(f"    {email}")
        if len(all_emails) > 10:
            print(f"    ... and {len(all_emails) - 10} more")

    print(f"\n  ✓ Open the results file in VS Code:")
    print(f"    code {OUTPUT_FILE}")
    print(f"  ✓ Or just find '{OUTPUT_FILE}' in this folder\n")

    # Pause so the window stays open when double-clicked
    input("\n  [Press Enter to exit...] ")


# ============================================================
# THIS IS THE SELF-START TRIGGER
# ============================================================
if __name__ == "__main__":
    main()