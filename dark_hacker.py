#!/usr/bin/env python3
"""
================================================================
              D A R K   H A C K E R   T O O L K I T
================================================================
Author : Cyber Security Student Project
Purpose: An advanced, menu-driven, real-time Python toolkit
         covering DEFENSIVE / ETHICAL cybersecurity & recon tasks.

  PASSWORD & CRYPTO
   1. Password Strength Checker
   2. Secure Password Generator
   3. Hash Generator (MD5/SHA1/SHA256/SHA512)
   4. Dictionary-Based Hash Cracker (audit your own hashes)
   5. AES Text Encryption / Decryption (Fernet)

  FILE & SYSTEM
   6. File Integrity Checker (tamper detection)
   7. Image Steganography (hide/reveal text)
   8. Log File Analyzer (suspicious activity detection)

  NETWORK & RECON
   9. Local Network Port Scanner (multithreaded + banner grabbing)
  10. Network Information Gatherer (IP + live host discovery)
  11. WHOIS Domain Lookup
  12. DNS Record Lookup (A / MX / NS / TXT / CNAME)
  13. Subdomain Enumeration
  14. SSL/TLS Certificate Inspector
  15. HTTP Security Headers Analyzer
  16. Website Misconfiguration Scanner (exposed files/paths)

  INTELLIGENCE
  17. Email/Password Breach Check (HaveIBeenPwned, k-anonymity)
  18. Email Header / Phishing Analyzer
  19. IP Geolocation Lookup

  BLUE TEAM / DEFENSE (real-time monitoring & hardening)
  20. Real-Time Brute-Force / Intrusion Detector
  21. System Security Hardening Audit
  22. Firewall Status & Rules Checker
  23. Malware Hash Reputation Lookup (CIRCL hashlookup)
  24. File Permission Auditor (world-writable file finder)
  25. Startup Persistence Checker (cron/systemd/registry)

⚠ LEGAL NOTICE:
This toolkit is for LEARNING and AUTHORIZED security testing only.
Only scan/test networks, domains, or devices you OWN or have explicit
written permission to test. Unauthorized scanning or accessing
systems is illegal in most countries (including Pakistan's PECA 2016).
================================================================
"""

import os
import re
import sys
import ssl
import time
import json
import socket
import string
import random
import hashlib
import getpass
import platform
import subprocess
import ipaddress
import itertools
import collections
import concurrent.futures
from datetime import datetime, timedelta

# ---------- Optional third-party libraries (auto-checked) ----------
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


APP_NAME = "DARK HACKER"
LOG_FILE = "dark_hacker_activity.log"


# ==================================================================
# UTILITY / UI HELPERS
# ==================================================================

def banner():
    print(r"""
 ██████╗  █████╗ ██████╗ ██╗  ██╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
 ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
 ██║  ██║███████║██████╔╝█████╔╝     ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
 ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
 ██████╔╝██║  ██║██║  ██║██║  ██╗    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                  Advanced Ethical Hacking & Recon Suite v2.0
""")


def pause():
    input("\nPress ENTER to return to main menu...")


def log_action(action):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {action}\n")


def require(flag, package_name):
    if not flag:
        print(f"❌ Required library '{package_name}' not installed.")
        print(f"   Install it with: pip install {package_name}")
        return False
    return True


# ==================================================================
# 1. PASSWORD STRENGTH CHECKER
# ==================================================================

def password_strength_checker():
    print("\n--- Password Strength Checker ---")
    pwd = getpass.getpass("Enter password to test (hidden input): ")

    score = 0
    feedback = []

    if len(pwd) >= 12:
        score += 2
    elif len(pwd) >= 8:
        score += 1
    else:
        feedback.append("❌ Too short (use at least 12 characters).")

    if re.search(r"[a-z]", pwd):
        score += 1
    else:
        feedback.append("❌ Add lowercase letters.")

    if re.search(r"[A-Z]", pwd):
        score += 1
    else:
        feedback.append("❌ Add uppercase letters.")

    if re.search(r"\d", pwd):
        score += 1
    else:
        feedback.append("❌ Add numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\[\]/\\+=~`]", pwd):
        score += 1
    else:
        feedback.append("❌ Add special characters (!@#$% etc.)")

    common_passwords = {"password", "123456", "12345678", "qwerty",
                         "admin", "letmein", "welcome", "iloveyou"}
    if pwd.lower() in common_passwords:
        score = 0
        feedback.append("❌ This is a very common/leaked password!")

    levels = {0: "Very Weak", 1: "Very Weak", 2: "Weak", 3: "Moderate",
              4: "Strong", 5: "Very Strong", 6: "Excellent"}
    strength = levels.get(min(score, 6), "Excellent")

    print(f"\nStrength Score : {score}/6")
    print(f"Rating         : {strength}")
    if feedback:
        print("Suggestions:")
        for f in feedback:
            print("  ", f)
    else:
        print("✅ Great password!")
    log_action(f"Password strength checked -> Rating: {strength}")


# ==================================================================
# 2. SECURE PASSWORD GENERATOR
# ==================================================================

def password_generator():
    print("\n--- Secure Password Generator ---")
    try:
        length = int(input("Password length (recommended 16): ") or 16)
        count = int(input("How many passwords to generate? ") or 1)
    except ValueError:
        print("Invalid number.")
        return

    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    print("\nGenerated Passwords:")
    for _ in range(count):
        pwd = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        print("  ", pwd)
    log_action(f"Generated {count} password(s) of length {length}")


# ==================================================================
# 3. HASH GENERATOR
# ==================================================================

def hash_generator():
    print("\n--- Hash Generator ---")
    text = input("Enter text to hash: ").encode()
    algos = {"MD5": hashlib.md5, "SHA1": hashlib.sha1,
              "SHA256": hashlib.sha256, "SHA512": hashlib.sha512}
    print()
    for name, func in algos.items():
        print(f"{name:8}: {func(text).hexdigest()}")
    log_action("Generated hash values for user input text")


# ==================================================================
# 4. DICTIONARY-BASED HASH CRACKER (audit your own password hashes)
# ==================================================================

BUILTIN_WORDLIST = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "baseball",
    "abc123", "football", "monkey", "letmein", "shadow", "master",
    "666666", "qwertyuiop", "123321", "mustang", "1234567890",
    "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212",
    "000000", "iloveyou", "welcome", "admin", "login", "princess",
    "solo", "starwars", "freedom", "whatever", "trustno1", "hello",
    "charlie", "aa123456", "donald", "password1", "qazwsx", "zaq1zaq1"
]


def hash_cracker():
    print("\n--- Dictionary-Based Hash Cracker ---")
    print("Use this to AUDIT the strength of your own password hashes.")
    target_hash = input("Enter the hash to crack: ").strip().lower()
    algo = input("Algorithm (md5/sha1/sha256/sha512) [md5]: ").strip().lower() or "md5"

    if algo not in ("md5", "sha1", "sha256", "sha512"):
        print("❌ Unsupported algorithm.")
        return

    use_custom = input("Use a custom wordlist file? (y/n): ").strip().lower()
    wordlist = BUILTIN_WORDLIST
    if use_custom == "y":
        path = input("Path to wordlist file: ").strip()
        if os.path.isfile(path):
            with open(path, "r", errors="ignore") as f:
                wordlist = [line.strip() for line in f if line.strip()]
        else:
            print("❌ File not found, using built-in wordlist instead.")

    print(f"\nTrying {len(wordlist)} candidate password(s)...\n")
    hasher = getattr(hashlib, algo)
    found = None
    start = time.time()
    for i, word in enumerate(wordlist, 1):
        candidate_hash = hasher(word.encode()).hexdigest()
        if candidate_hash == target_hash:
            found = word
            break
    elapsed = time.time() - start

    if found:
        print(f"✅ MATCH FOUND: '{found}'  (in {elapsed:.3f}s)")
        print("⚠️  This password is WEAK — it exists in common wordlists!")
    else:
        print(f"❌ No match found in {len(wordlist)} words ({elapsed:.3f}s).")
        print("   This suggests the password is not a common/dictionary word.")
    log_action(f"Hash cracker run -> {'FOUND' if found else 'NOT FOUND'}")


# ==================================================================
# 5. AES TEXT ENCRYPTION / DECRYPTION (Fernet)
# ==================================================================

def encryption_tool():
    print("\n--- AES Text Encryption / Decryption ---")
    if not require(CRYPTO_AVAILABLE, "cryptography"):
        return

    print("1. Generate a new key")
    print("2. Encrypt text")
    print("3. Decrypt text")
    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        key = Fernet.generate_key()
        print(f"\n🔑 Your secret key (SAVE THIS SAFELY):\n{key.decode()}")

    elif choice == "2":
        key = input("Enter your key: ").strip().encode()
        try:
            f = Fernet(key)
        except Exception:
            print("❌ Invalid key.")
            return
        text = input("Enter text to encrypt: ").encode()
        token = f.encrypt(text)
        print(f"\n🔒 Encrypted:\n{token.decode()}")

    elif choice == "3":
        key = input("Enter your key: ").strip().encode()
        try:
            f = Fernet(key)
        except Exception:
            print("❌ Invalid key.")
            return
        token = input("Enter encrypted text: ").strip().encode()
        try:
            text = f.decrypt(token)
            print(f"\n🔓 Decrypted:\n{text.decode()}")
        except Exception:
            print("❌ Decryption failed. Wrong key or corrupted data.")
    else:
        print("Invalid choice.")
    log_action("Encryption/Decryption tool used")


# ==================================================================
# 6. FILE INTEGRITY CHECKER
# ==================================================================

def hash_file(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def file_integrity_checker():
    print("\n--- File Integrity Checker ---")
    print("1. Generate hash for a file (save this for later)")
    print("2. Verify a file against a known hash")
    choice = input("Choose (1/2): ").strip()

    path = input("Enter full file path: ").strip()
    if not os.path.isfile(path):
        print("❌ File not found.")
        return

    if choice == "1":
        digest = hash_file(path)
        print(f"\nSHA256 hash of file:\n{digest}")
        print("👉 Save this hash somewhere safe. Compare later to detect tampering.")
    elif choice == "2":
        known = input("Enter the known/original SHA256 hash: ").strip()
        current = hash_file(path)
        if current.lower() == known.lower():
            print("✅ MATCH — file has NOT been modified.")
        else:
            print("❌ MISMATCH — file integrity compromised (tampered/corrupted)!")
    else:
        print("Invalid choice.")
    log_action(f"File integrity check performed on {path}")


# ==================================================================
# 7. IMAGE STEGANOGRAPHY
# ==================================================================

def steganography_tool():
    print("\n--- Image Steganography (Hide/Reveal Text) ---")
    if not require(PIL_AVAILABLE, "Pillow"):
        return

    print("1. Hide text inside an image")
    print("2. Reveal text from an image")
    choice = input("Choose (1/2): ").strip()

    if choice == "1":
        in_path = input("Path to source image (.png recommended): ").strip()
        if not os.path.isfile(in_path):
            print("❌ File not found.")
            return
        secret = input("Enter secret text to hide: ") + "<<END>>"
        out_path = input("Output image path (e.g. secret.png): ").strip() or "secret.png"

        img = Image.open(in_path).convert("RGB")
        binary_secret = "".join(format(ord(c), "08b") for c in secret)

        pixels = list(img.getdata())
        if len(binary_secret) > len(pixels) * 3:
            print("❌ Image too small to hide this much text.")
            return

        new_pixels = []
        bit_idx = 0
        for pixel in pixels:
            pixel = list(pixel)
            for n in range(3):
                if bit_idx < len(binary_secret):
                    pixel[n] = (pixel[n] & ~1) | int(binary_secret[bit_idx])
                    bit_idx += 1
            new_pixels.append(tuple(pixel))

        img.putdata(new_pixels)
        img.save(out_path)
        print(f"✅ Secret text hidden inside: {out_path}")

    elif choice == "2":
        in_path = input("Path to image containing hidden text: ").strip()
        if not os.path.isfile(in_path):
            print("❌ File not found.")
            return
        img = Image.open(in_path).convert("RGB")
        pixels = list(img.getdata())

        bits = ""
        for pixel in pixels:
            for n in range(3):
                bits += str(pixel[n] & 1)

        chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
        message = "".join(chars)
        if "<<END>>" in message:
            message = message.split("<<END>>")[0]
            print(f"\n🔍 Hidden message found:\n{message}")
        else:
            print("❌ No hidden message marker found (may not contain hidden text).")
    else:
        print("Invalid choice.")
    log_action("Steganography tool used")


# ==================================================================
# 8. LOG FILE ANALYZER
# ==================================================================

SUSPICIOUS_KEYWORDS = [
    "failed password", "authentication failure", "unauthorized",
    "invalid user", "sql injection", "select * from", "union select",
    "<script>", "root login", "permission denied", "brute force",
    "port scan", "denied", "attack"
]


def log_analyzer():
    print("\n--- Log File Analyzer ---")
    path = input("Enter path to log file (.log/.txt): ").strip()
    if not os.path.isfile(path):
        print("❌ File not found.")
        return

    print("\nScanning log file for suspicious activity (real-time)...\n")
    hits = 0
    with open(path, "r", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            low = line.lower()
            for kw in SUSPICIOUS_KEYWORDS:
                if kw in low:
                    print(f"  ⚠️  Line {i}: {line.strip()[:120]}")
                    hits += 1
                    break

    print(f"\nScan complete. {hits} suspicious line(s) found.")
    log_action(f"Log file analyzed: {path} -> {hits} suspicious entries")


# ==================================================================
# 9. LOCAL NETWORK PORT SCANNER (+ banner grabbing)
# ==================================================================

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
}


def grab_banner(ip, port, timeout=1.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        try:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        except Exception:
            pass
        banner_data = s.recv(256)
        s.close()
        return banner_data.decode(errors="ignore").strip().split("\n")[0]
    except Exception:
        return None


def scan_port(ip, port, timeout=0.6):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))
        return port if result == 0 else None
    finally:
        s.close()


def port_scanner():
    print("\n--- Local/Authorized Port Scanner ---")
    print("⚠ Only scan systems you OWN or have written permission to test.")
    target = input("Enter target IP or hostname (e.g. 127.0.0.1): ").strip()

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("❌ Could not resolve hostname.")
        return

    mode = input("Scan (1) Common ports  or (2) Custom range? [1/2]: ").strip()
    if mode == "2":
        try:
            start = int(input("Start port: "))
            end = int(input("End port: "))
            ports = range(start, end + 1)
        except ValueError:
            print("Invalid range.")
            return
    else:
        ports = COMMON_PORTS.keys()

    grab = input("Attempt banner grabbing on open ports? (y/n): ").strip().lower() == "y"

    print(f"\nScanning {ip} ... please wait (real-time results below)\n")
    open_ports = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                service = COMMON_PORTS.get(port, "Unknown")
                line = f"  ✅ OPEN  -> Port {port:<6} ({service})"
                if grab:
                    b = grab_banner(ip, port)
                    if b:
                        line += f"  | Banner: {b[:60]}"
                print(line)
                open_ports.append(port)

    elapsed = time.time() - start_time
    print(f"\nScan complete in {elapsed:.2f}s. {len(open_ports)} open port(s) found.")
    log_action(f"Port scan on {ip} -> {sorted(open_ports)}")


# ==================================================================
# 10. NETWORK INFORMATION GATHERER
# ==================================================================

def network_info():
    print("\n--- Network Information Gatherer ---")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        local_ip = "Unavailable"

    print(f"Hostname   : {hostname}")
    print(f"Local IP   : {local_ip}")

    if REQUESTS_AVAILABLE:
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=5).text
            print(f"Public IP  : {public_ip}")
        except Exception:
            print("Public IP  : Could not fetch (no internet or blocked)")
    else:
        print("Public IP  : install 'requests' library to fetch this")

    scan_lan = input("\nScan local subnet for live hosts? (y/n): ").strip().lower()
    if scan_lan == "y":
        discover_live_hosts(local_ip)

    log_action("Network info gathered")


def ping_host(ip):
    param = "-n" if os.name == "nt" else "-c"
    cmd = f"ping {param} 1 -W 1 {ip} > {'NUL' if os.name=='nt' else '/dev/null'} 2>&1"
    response = os.system(cmd)
    return ip if response == 0 else None


def discover_live_hosts(local_ip):
    try:
        network = ipaddress.ip_network(local_ip + "/24", strict=False)
    except ValueError:
        print("Could not determine subnet.")
        return

    print(f"\nScanning subnet {network} for live hosts (real-time)...\n")
    live_hosts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_host, str(ip)): ip for ip in network.hosts()}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                print(f"  🟢 LIVE -> {res}")
                live_hosts.append(res)
    print(f"\n{len(live_hosts)} live host(s) found on the network.")


# ==================================================================
# 11. WHOIS DOMAIN LOOKUP
# ==================================================================

WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com", "net": "whois.verisign-grs.com",
    "org": "whois.pir.org", "io": "whois.nic.io", "co": "whois.nic.co",
    "info": "whois.afilias.net", "biz": "whois.biz",
    "dev": "whois.nic.google", "app": "whois.nic.google",
    "pk": "whois.pknic.net.pk", "xyz": "whois.nic.xyz",
}


def whois_lookup():
    print("\n--- WHOIS Domain Lookup ---")
    domain = input("Enter domain (e.g. example.com): ").strip().lower()
    tld = domain.split(".")[-1]
    server = WHOIS_SERVERS.get(tld, "whois.iana.org")

    try:
        with socket.create_connection((server, 43), timeout=8) as s:
            s.send((domain + "\r\n").encode())
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        text = response.decode(errors="ignore")
        print(f"\n📋 WHOIS data for {domain} (via {server}):\n")
        print(text[:2500])
        if len(text) > 2500:
            print("\n...(truncated)")
    except Exception as e:
        print(f"❌ WHOIS lookup failed: {e}")
    log_action(f"WHOIS lookup performed on {domain}")


# ==================================================================
# 12. DNS RECORD LOOKUP
# ==================================================================

def dns_lookup():
    print("\n--- DNS Record Lookup ---")
    domain = input("Enter domain (e.g. example.com): ").strip()

    print(f"\nResolving records for {domain} ...\n")
    try:
        result = socket.getaddrinfo(domain, None)
        ips = sorted(set(r[4][0] for r in result))
        print("A/AAAA Records:")
        for ip in ips:
            print(f"   {ip}")
    except socket.gaierror:
        print("   ❌ Could not resolve A/AAAA records.")

    try:
        hostname, aliases, addresses = socket.gethostbyname_ex(domain)
        if aliases:
            print("\nCNAME Aliases:")
            for a in aliases:
                print(f"   {a}")
    except Exception:
        pass

    print("\nℹ️  For full MX/TXT/NS record lookups, install 'dnspython':")
    print("   pip install dnspython")
    log_action(f"DNS lookup performed on {domain}")


# ==================================================================
# 13. SUBDOMAIN ENUMERATION
# ==================================================================

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "dev", "api", "staging", "test", "admin",
    "blog", "shop", "portal", "vpn", "ns1", "ns2", "smtp", "webmail",
    "cpanel", "m", "mobile", "secure", "cdn", "app", "beta", "support",
    "status", "docs", "git", "dashboard", "cloud", "images", "static"
]


def resolve_sub(sub, domain):
    fqdn = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(fqdn)
        return (fqdn, ip)
    except socket.gaierror:
        return None


def subdomain_enum():
    print("\n--- Subdomain Enumeration ---")
    print("⚠ Only run against domains you own or are authorized to test.")
    domain = input("Enter root domain (e.g. example.com): ").strip()

    print(f"\nEnumerating common subdomains of {domain} (real-time)...\n")
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(resolve_sub, s, domain): s for s in COMMON_SUBDOMAINS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                print(f"  🟢 FOUND -> {res[0]}  ({res[1]})")
                found.append(res)

    print(f"\n{len(found)} subdomain(s) discovered out of {len(COMMON_SUBDOMAINS)} tested.")
    log_action(f"Subdomain enumeration on {domain} -> {len(found)} found")


# ==================================================================
# 14. SSL/TLS CERTIFICATE INSPECTOR
# ==================================================================

def ssl_inspector():
    print("\n--- SSL/TLS Certificate Inspector ---")
    host = input("Enter domain (e.g. example.com): ").strip()
    port = 443

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=8) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        print(f"\n🔒 Certificate details for {host}:\n")
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer = dict(x[0] for x in cert.get("issuer", []))
        print(f"  Subject     : {subject.get('commonName', 'N/A')}")
        print(f"  Issuer      : {issuer.get('commonName', 'N/A')}")
        print(f"  Valid From  : {cert.get('notBefore')}")
        print(f"  Valid Until : {cert.get('notAfter')}")

        expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry - datetime.utcnow()).days
        if days_left < 0:
            print(f"  ❌ Certificate EXPIRED {abs(days_left)} days ago!")
        elif days_left < 30:
            print(f"  ⚠️  Certificate expires soon: {days_left} days left")
        else:
            print(f"  ✅ Certificate valid for {days_left} more days")

        sans = cert.get("subjectAltName", [])
        if sans:
            print(f"  SANs        : {', '.join(s[1] for s in sans[:8])}")
    except Exception as e:
        print(f"❌ Could not retrieve certificate: {e}")
    log_action(f"SSL certificate inspected for {host}")


# ==================================================================
# 15. HTTP SECURITY HEADERS ANALYZER
# ==================================================================

SECURITY_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy",
    "X-Frame-Options", "X-Content-Type-Options",
    "Referrer-Policy", "Permissions-Policy", "X-XSS-Protection",
]


def security_headers_analyzer():
    print("\n--- HTTP Security Headers Analyzer ---")
    if not require(REQUESTS_AVAILABLE, "requests"):
        return

    url = input("Enter website URL (e.g. https://example.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
    except Exception as e:
        print(f"❌ Could not reach site: {e}")
        return

    print(f"\n📄 Headers report for {url} (HTTP {resp.status_code}):\n")
    missing = []
    for h in SECURITY_HEADERS:
        if h in resp.headers:
            print(f"  ✅ {h}: {resp.headers[h][:70]}")
        else:
            print(f"  ❌ {h}: MISSING")
            missing.append(h)

    print(f"\nSummary: {len(SECURITY_HEADERS) - len(missing)}/{len(SECURITY_HEADERS)} security headers present.")
    if missing:
        print("⚠️  Consider adding the missing headers to improve security posture.")
    log_action(f"Security headers analyzed for {url} -> {len(missing)} missing")


# ==================================================================
# 16. WEBSITE MISCONFIGURATION SCANNER
# ==================================================================

COMMON_EXPOSED_PATHS = [
    "robots.txt", ".env", ".git/config", "backup.zip", "config.php.bak",
    "wp-config.php.bak", ".htaccess", "phpinfo.php", "admin/",
    "server-status", ".DS_Store", "database.sql", "id_rsa",
]


def check_path(base_url, path):
    try:
        r = requests.get(base_url.rstrip("/") + "/" + path, timeout=6, allow_redirects=False)
        if r.status_code == 200:
            return (path, r.status_code)
    except Exception:
        pass
    return None


def misconfig_scanner():
    print("\n--- Website Misconfiguration Scanner ---")
    print("⚠ Only run against sites you OWN or are authorized to test.")
    if not require(REQUESTS_AVAILABLE, "requests"):
        return

    url = input("Enter website URL (e.g. https://example.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\nChecking {url} for common exposed files/paths (real-time)...\n")
    findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_path, url, p): p for p in COMMON_EXPOSED_PATHS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                print(f"  ⚠️  EXPOSED -> /{res[0]}  (HTTP {res[1]})")
                findings.append(res)

    print(f"\nScan complete. {len(findings)} potentially exposed path(s) found.")
    if not findings:
        print("✅ No common misconfigurations detected.")
    log_action(f"Misconfig scan on {url} -> {len(findings)} found")


# ==================================================================
# 17. EMAIL/PASSWORD BREACH CHECK (HaveIBeenPwned k-anonymity)
# ==================================================================

def breach_check():
    print("\n--- Password Breach Check (k-anonymity, safe) ---")
    if not require(REQUESTS_AVAILABLE, "requests"):
        return

    print("This checks if a PASSWORD has appeared in known data breaches.")
    print("Your full password/hash is never sent to the server.")
    pwd = getpass.getpass("Enter password to check: ")

    sha1 = hashlib.sha1(pwd.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    try:
        resp = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Could not reach breach database: {e}")
        return

    found = False
    for line in resp.text.splitlines():
        h_suffix, count = line.split(":")
        if h_suffix == suffix:
            print(f"⚠️  This password was found in {count} known data breaches!")
            print("   You should change it immediately if you're using it anywhere.")
            found = True
            break

    if not found:
        print("✅ Good news — this password was NOT found in known breaches.")
    log_action("Password breach check performed")


# ==================================================================
# 18. EMAIL HEADER / PHISHING ANALYZER
# ==================================================================

def email_header_analyzer():
    print("\n--- Email Header / Phishing Analyzer ---")
    print("Paste the raw email header text below.")
    print("(Type END on its own line when finished)\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)

    header_text = "\n".join(lines)
    if not header_text.strip():
        print("❌ No header text provided.")
        return

    print("\n🔍 Analysis Results:\n")

    received_count = len(re.findall(r"^Received:", header_text, re.MULTILINE | re.IGNORECASE))
    print(f"  Hops (Received headers): {received_count}")
    if received_count > 8:
        print("    ⚠️  Unusually high hop count — possible relay abuse.")

    spf = re.search(r"spf=(\w+)", header_text, re.IGNORECASE)
    dkim = re.search(r"dkim=(\w+)", header_text, re.IGNORECASE)
    dmarc = re.search(r"dmarc=(\w+)", header_text, re.IGNORECASE)

    for name, match in [("SPF", spf), ("DKIM", dkim), ("DMARC", dmarc)]:
        if match:
            status = match.group(1).lower()
            icon = "✅" if status == "pass" else "❌"
            print(f"  {icon} {name}: {status}")
        else:
            print(f"  ❓ {name}: not found in headers")

    from_match = re.search(r"^From:\s*(.+)$", header_text, re.MULTILINE | re.IGNORECASE)
    reply_to = re.search(r"^Reply-To:\s*(.+)$", header_text, re.MULTILINE | re.IGNORECASE)
    if from_match and reply_to:
        from_domain = re.search(r"@([\w.-]+)", from_match.group(1))
        reply_domain = re.search(r"@([\w.-]+)", reply_to.group(1))
        if from_domain and reply_domain and from_domain.group(1) != reply_domain.group(1):
            print(f"  ⚠️  Mismatch: From domain ({from_domain.group(1)}) != "
                  f"Reply-To domain ({reply_domain.group(1)}) — common phishing sign!")

    print("\nℹ️  This is a heuristic analysis. Always verify with full context.")
    log_action("Email header analyzed for phishing indicators")


# ==================================================================
# 19. IP GEOLOCATION LOOKUP
# ==================================================================

def ip_geolocation():
    print("\n--- IP Geolocation Lookup ---")
    if not require(REQUESTS_AVAILABLE, "requests"):
        return

    ip = input("Enter IP address (leave blank for your own public IP): ").strip()
    url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"

    try:
        resp = requests.get(url, timeout=8)
        data = resp.json()
    except Exception as e:
        print(f"❌ Lookup failed: {e}")
        return

    if data.get("error"):
        print(f"❌ {data.get('reason', 'Lookup failed')}")
        return

    print(f"\n🌍 Geolocation for {data.get('ip', ip)}:\n")
    print(f"  City      : {data.get('city')}")
    print(f"  Region    : {data.get('region')}")
    print(f"  Country   : {data.get('country_name')}")
    print(f"  ISP/Org   : {data.get('org')}")
    print(f"  Timezone  : {data.get('timezone')}")
    print(f"  Lat/Long  : {data.get('latitude')}, {data.get('longitude')}")
    log_action(f"IP geolocation lookup performed for {ip or 'own IP'}")


# ==================================================================
# 20. REAL-TIME BRUTE-FORCE / INTRUSION DETECTOR
# ==================================================================

IP_REGEX = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
BRUTE_FORCE_KEYWORDS = ["failed password", "authentication failure",
                          "invalid user", "failed login", "login failed"]


def _tail_follow(path):
    """Generator that yields new lines appended to a file, like `tail -f`."""
    with open(path, "r", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line


def intrusion_detector():
    print("\n--- Real-Time Brute-Force / Intrusion Detector ---")
    path = input("Enter path to log file to monitor (e.g. auth.log): ").strip()
    if not os.path.isfile(path):
        print("❌ File not found.")
        return

    try:
        threshold = int(input("Alert threshold (failed attempts per IP) [5]: ") or 5)
        window = int(input("Time window in seconds [60]: ") or 60)
    except ValueError:
        print("Invalid number, using defaults (5 attempts / 60s).")
        threshold, window = 5, 60

    print(f"\n🛡️  Monitoring '{path}' in real-time... Press Ctrl+C to stop.\n")
    attempts = collections.defaultdict(list)  # ip -> [timestamps]
    alerted = set()

    try:
        for line in _tail_follow(path):
            low = line.lower()
            if any(kw in low for kw in BRUTE_FORCE_KEYWORDS):
                match = IP_REGEX.search(line)
                if not match:
                    continue
                ip = match.group(1)
                now = time.time()
                attempts[ip].append(now)
                # Keep only attempts within the time window
                attempts[ip] = [t for t in attempts[ip] if now - t <= window]

                count = len(attempts[ip])
                print(f"  ⚠️  Failed attempt from {ip}  (count in window: {count})")

                if count >= threshold and ip not in alerted:
                    print(f"\n  🚨 ALERT: Possible brute-force attack from {ip} "
                          f"— {count} failed attempts in {window}s!\n")
                    log_action(f"BRUTE-FORCE ALERT: {ip} - {count} attempts")
                    alerted.add(ip)
                elif count < threshold and ip in alerted:
                    alerted.discard(ip)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    log_action(f"Intrusion detection session ended for {path}")


# ==================================================================
# 21. SYSTEM SECURITY HARDENING AUDIT
# ==================================================================

RISKY_LOCAL_PORTS = {
    21: "FTP (unencrypted)", 23: "Telnet (unencrypted)",
    69: "TFTP (no auth)", 161: "SNMP (default community strings)",
    445: "SMB (ransomware target)", 3389: "RDP (brute-force target)",
    5900: "VNC (often unauthenticated)",
}


def security_hardening_audit():
    print("\n--- System Security Hardening Audit ---")
    print(f"OS Detected: {platform.system()} {platform.release()}\n")

    findings = []

    # 1. Check risky ports open on localhost
    print("🔍 Checking for risky open services on localhost...")
    for port, desc in RISKY_LOCAL_PORTS.items():
        result = scan_port("127.0.0.1", port, timeout=0.3)
        if result:
            print(f"  ⚠️  Port {port} OPEN -> {desc}")
            findings.append(f"Risky port {port} open ({desc})")
    if not any(scan_port("127.0.0.1", p, timeout=0.3) for p in RISKY_LOCAL_PORTS):
        print("  ✅ No commonly risky ports open on localhost.")

    # 2. Check world-writable files in common sensitive dirs (Linux/Mac)
    if platform.system() in ("Linux", "Darwin"):
        print("\n🔍 Checking for world-writable files in /etc (sample scan)...")
        ww_count = 0
        try:
            for root, dirs, files in os.walk("/etc"):
                for fname in files[:200]:
                    fpath = os.path.join(root, fname)
                    try:
                        mode = os.stat(fpath).st_mode
                        if mode & 0o002:
                            ww_count += 1
                            if ww_count <= 5:
                                print(f"  ⚠️  World-writable: {fpath}")
                    except (PermissionError, FileNotFoundError, OSError):
                        continue
                break  # only scan top-level /etc for speed/safety
        except PermissionError:
            print("  ❓ Insufficient permission to scan /etc")
        if ww_count == 0:
            print("  ✅ No world-writable files found in top-level /etc.")
        elif ww_count > 5:
            print(f"  ...and {ww_count - 5} more.")
        if ww_count:
            findings.append(f"{ww_count} world-writable file(s) in /etc")

    # 3. Check password policy hints (Linux)
    if platform.system() == "Linux" and os.path.isfile("/etc/login.defs"):
        print("\n🔍 Checking password aging policy (/etc/login.defs)...")
        try:
            with open("/etc/login.defs", errors="ignore") as f:
                content = f.read()
            max_days = re.search(r"PASS_MAX_DAYS\s+(\d+)", content)
            if max_days and int(max_days.group(1)) > 90:
                print(f"  ⚠️  PASS_MAX_DAYS is {max_days.group(1)} (recommended ≤ 90)")
                findings.append("Weak password aging policy")
            else:
                print("  ✅ Password aging policy looks reasonable.")
        except PermissionError:
            print("  ❓ Insufficient permission to read /etc/login.defs")

    print(f"\n📊 Audit complete. {len(findings)} finding(s) flagged.")
    log_action(f"Security hardening audit -> {len(findings)} findings")


# ==================================================================
# 22. FIREWALL STATUS & RULES CHECKER
# ==================================================================

def firewall_checker():
    print("\n--- Firewall Status & Rules Checker ---")
    system = platform.system()

    try:
        if system == "Linux":
            # Try ufw first, then iptables
            ufw = subprocess.run(["ufw", "status", "verbose"],
                                  capture_output=True, text=True, timeout=8)
            if ufw.returncode == 0 and ufw.stdout.strip():
                print("📋 UFW Status:\n")
                print(ufw.stdout)
            else:
                ipt = subprocess.run(["iptables", "-L", "-n"],
                                      capture_output=True, text=True, timeout=8)
                print("📋 iptables Rules:\n")
                print(ipt.stdout if ipt.stdout else ipt.stderr)

        elif system == "Darwin":
            result = subprocess.run(
                ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"],
                capture_output=True, text=True, timeout=8)
            print("📋 macOS Application Firewall:\n")
            print(result.stdout if result.stdout else result.stderr)

        elif system == "Windows":
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles", "state"],
                capture_output=True, text=True, timeout=8)
            print("📋 Windows Firewall Status:\n")
            print(result.stdout if result.stdout else result.stderr)

        else:
            print(f"❌ Unsupported OS for automated firewall check: {system}")
            return

    except FileNotFoundError:
        print("❌ Firewall command not found. It may not be installed, or you "
              "may need administrator/root privileges to query it.")
    except subprocess.TimeoutExpired:
        print("❌ Firewall check timed out.")
    except PermissionError:
        print("❌ Permission denied. Try running with administrator/sudo privileges.")
    except Exception as e:
        print(f"❌ Could not check firewall status: {e}")

    log_action("Firewall status checked")


# ==================================================================
# 23. MALWARE HASH REPUTATION LOOKUP (CIRCL hashlookup, no API key)
# ==================================================================

def malware_hash_lookup():
    print("\n--- Malware Hash Reputation Lookup ---")
    print("Checks a file hash against the CIRCL hashlookup database")
    print("(a public catalogue of known-good and known files, no API key needed).\n")
    if not require(REQUESTS_AVAILABLE, "requests"):
        return

    choice = input("Do you want to (1) enter a hash directly or (2) hash a local file? [1/2]: ").strip()
    if choice == "2":
        path = input("Enter file path: ").strip()
        if not os.path.isfile(path):
            print("❌ File not found.")
            return
        file_hash = hash_file(path, "sha256")
        print(f"Computed SHA256: {file_hash}")
    else:
        file_hash = input("Enter SHA256 hash: ").strip()

    algo = "sha256" if len(file_hash) == 64 else "sha1" if len(file_hash) == 40 else "md5"

    try:
        resp = requests.get(f"https://hashlookup.circl.lu/lookup/{algo}/{file_hash}", timeout=10)
    except Exception as e:
        print(f"❌ Could not reach hashlookup database: {e}")
        return

    if resp.status_code == 200:
        data = resp.json()
        print("\n✅ Hash FOUND in known-file database:")
        print(f"  File name : {data.get('FileName', 'N/A')}")
        print(f"  Product   : {data.get('ProductName', 'N/A')}")
        print(f"  Source    : {data.get('source', 'N/A')}")
        print("  ℹ️  This suggests the file is a KNOWN file (commonly benign),")
        print("     but always verify with an up-to-date antivirus engine too.")
    elif resp.status_code == 404:
        print("\n❓ Hash NOT FOUND in the known-file database.")
        print("   This does not confirm malware — it just means the file isn't")
        print("   in this catalogue. Scan it with an antivirus/VirusTotal for certainty.")
    else:
        print(f"❌ Unexpected response: HTTP {resp.status_code}")

    log_action(f"Malware hash lookup performed -> {file_hash[:16]}...")


# ==================================================================
# 24. FILE PERMISSION AUDITOR
# ==================================================================

def file_permission_auditor():
    print("\n--- File Permission Auditor ---")
    print("Scans a directory for world-writable or overly permissive files.\n")
    target_dir = input("Enter directory to scan (e.g. /home/user/project): ").strip()
    if not os.path.isdir(target_dir):
        print("❌ Directory not found.")
        return

    try:
        max_files = int(input("Max files to scan [500]: ") or 500)
    except ValueError:
        max_files = 500

    print(f"\nScanning '{target_dir}' (up to {max_files} files)...\n")
    risky = []
    scanned = 0

    for root, dirs, files in os.walk(target_dir):
        for fname in files:
            if scanned >= max_files:
                break
            fpath = os.path.join(root, fname)
            try:
                mode = os.stat(fpath).st_mode
                perms = oct(mode)[-3:]
                world_writable = bool(mode & 0o002)
                world_executable_sensitive = fname.endswith((".key", ".pem", ".env")) and bool(mode & 0o044)

                if world_writable:
                    print(f"  ⚠️  World-writable ({perms}): {fpath}")
                    risky.append(fpath)
                elif world_executable_sensitive:
                    print(f"  ⚠️  Sensitive file readable by others ({perms}): {fpath}")
                    risky.append(fpath)
            except (PermissionError, FileNotFoundError, OSError):
                continue
            scanned += 1
        if scanned >= max_files:
            break

    print(f"\n📊 Scanned {scanned} file(s). {len(risky)} risky permission issue(s) found.")
    if not risky:
        print("✅ No risky file permissions detected.")
    log_action(f"File permission audit on {target_dir} -> {len(risky)} issues")


# ==================================================================
# 25. STARTUP / PERSISTENCE MECHANISM CHECKER
# ==================================================================

def persistence_checker():
    print("\n--- Startup / Persistence Mechanism Checker ---")
    print("Lists common auto-start locations malware often abuses for persistence.\n")
    system = platform.system()
    findings = []

    if system == "Linux":
        print("🔍 Checking crontab...")
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
            if result.stdout.strip():
                print(result.stdout)
                findings.append("User crontab has entries")
            else:
                print("  ✅ No user crontab entries.")
        except Exception:
            print("  ❓ Could not read crontab.")

        for cron_dir in ["/etc/cron.d", "/etc/cron.daily"]:
            if os.path.isdir(cron_dir):
                entries = os.listdir(cron_dir)
                print(f"\n🔍 {cron_dir}: {len(entries)} entr(y/ies)")
                for e in entries[:10]:
                    print(f"   - {e}")

        autostart_dir = os.path.expanduser("~/.config/autostart")
        if os.path.isdir(autostart_dir):
            entries = os.listdir(autostart_dir)
            print(f"\n🔍 ~/.config/autostart: {len(entries)} entr(y/ies)")
            for e in entries:
                print(f"   - {e}")

    elif system == "Windows":
        print("🔍 Checking Windows Registry Run keys...")
        try:
            import winreg
            for hive, path in [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            ]:
                try:
                    key = winreg.OpenKey(hive, path)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            print(f"   - {name}: {value}")
                            findings.append(name)
                            i += 1
                        except OSError:
                            break
                except FileNotFoundError:
                    continue
        except ImportError:
            print("  ❓ winreg module unavailable.")

    elif system == "Darwin":
        launch_dirs = ["~/Library/LaunchAgents", "/Library/LaunchAgents", "/Library/LaunchDaemons"]
        for d in launch_dirs:
            expanded = os.path.expanduser(d)
            if os.path.isdir(expanded):
                entries = os.listdir(expanded)
                print(f"\n🔍 {d}: {len(entries)} entr(y/ies)")
                for e in entries[:10]:
                    print(f"   - {e}")

    else:
        print(f"❌ Unsupported OS: {system}")
        return

    print(f"\n📊 Review complete. Manually verify any unfamiliar entries above.")
    log_action("Persistence/startup mechanism check performed")


# ==================================================================
# MAIN MENU
# ==================================================================

MENU = {
    "1": ("Password Strength Checker", password_strength_checker),
    "2": ("Secure Password Generator", password_generator),
    "3": ("Hash Generator", hash_generator),
    "4": ("Dictionary-Based Hash Cracker", hash_cracker),
    "5": ("AES Text Encryption/Decryption", encryption_tool),
    "6": ("File Integrity Checker", file_integrity_checker),
    "7": ("Image Steganography", steganography_tool),
    "8": ("Log File Analyzer", log_analyzer),
    "9": ("Local Network Port Scanner", port_scanner),
    "10": ("Network Information Gatherer", network_info),
    "11": ("WHOIS Domain Lookup", whois_lookup),
    "12": ("DNS Record Lookup", dns_lookup),
    "13": ("Subdomain Enumeration", subdomain_enum),
    "14": ("SSL/TLS Certificate Inspector", ssl_inspector),
    "15": ("HTTP Security Headers Analyzer", security_headers_analyzer),
    "16": ("Website Misconfiguration Scanner", misconfig_scanner),
    "17": ("Email/Password Breach Check", breach_check),
    "18": ("Email Header / Phishing Analyzer", email_header_analyzer),
    "19": ("IP Geolocation Lookup", ip_geolocation),
    "20": ("Real-Time Brute-Force / Intrusion Detector", intrusion_detector),
    "21": ("System Security Hardening Audit", security_hardening_audit),
    "22": ("Firewall Status & Rules Checker", firewall_checker),
    "23": ("Malware Hash Reputation Lookup", malware_hash_lookup),
    "24": ("File Permission Auditor", file_permission_auditor),
    "25": ("Startup Persistence Checker", persistence_checker),
    "0": ("Exit", None),
}


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        print("Select a tool:\n")
        for key, (name, _) in MENU.items():
            print(f"  [{key:>2}] {name}")
        print()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print(f"\nExiting {APP_NAME} Toolkit. Stay ethical! 🛡️")
            sys.exit(0)

        entry = MENU.get(choice)
        if entry:
            _, func = entry
            try:
                func()
            except KeyboardInterrupt:
                print("\n\nCancelled by user.")
            except Exception as e:
                print(f"\n❌ Error: {e}")
            pause()
        else:
            print("Invalid choice.")
            time.sleep(1)


if __name__ == "__main__":
    main()
