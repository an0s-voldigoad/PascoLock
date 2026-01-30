#!/usr/bin/env python3
import re, math, json, time, sys, os, getpass, secrets, string, hashlib, requests
from datetime import datetime

# ================= COLORS =================
RED = "\033[91m"
BLUE = "\033[94m"
BLACK = "\033[90m"
WHITE = "\033[97m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ================= UTILITY FUNCTIONS ==================
def clear_screen():
    os.system("clear")

def beep():
    print("\a", end="", flush=True)

# ================= STARTUP ANIMATION ====================
def startup_animation():
    clear_screen()
    print(f"{BLUE}[*] Initializing PascoLock Engine...{RESET}")
    time.sleep(0.5)

    tasks = [
        "Loading cryptographic modules",
        "Initializing entropy analyzer",
        "Connecting breach intelligence (HIBP)",
        "Applying offline security policy",
        "Finalizing secure environment"
    ]

    for task in tasks:
        print(f"{BLACK}[+] {task}...{RESET}")
        for i in range(0, 101, 20):
            bar = "█" * (i // 10) + "░" * (10 - i // 10)
            print(f"\r{RED}    [{bar}] {i}%{RESET}", end="")
            time.sleep(0.1)
        print()

    print(f"\n{GREEN}[✓] PascoLock Ready.{RESET}")
    beep()
    time.sleep(0.3)
    beep()
    time.sleep(1)
    clear_screen()

# ================ BANNER =================
def banner():
    print(f"{RED} ====================== {RESET}")
    print (f"{BLUE}       PascoLock  Password Checker {{RESET}}")
    print (f"{BLACK}    Offline-First |  HIBP_Aware |  Kali Linux {RESET}")
    print(f"{RED} ====================== {RESET}\n")

# ================= DATA =================
COMMON_PASSWORDS = {
    "password","123456","123456789","qwerty","abc123",
    "password123","admin","letmein","welcome","india123"
}

LEET_MAP = {'@':'a','4':'a','3':'e','1':'l','!':'i','0':'o','$':'s'}
HIBP_API = "https://api.pwnedpasswords.com/range/"

# ================= UI =================
def banner():
    print(f"""{RED}{BOLD}
██████╗  █████╗ ███████╗ ██████╗  ██████╗ ██╗      ██████╗  ██████╗ ██╗  ██╗
██╔══██╗██╔══██╗██╔════╝██╔═══   ██╔═══██╗██║     ██╔═══██╗██╔════╝ ██║ ██╔╝
██████╔╝███████║███████╗██║      ██║   ██║██║     ██║   ██║██║      █████╔╝
██╔═══╝ ██╔══██║╚════██║██║     ║██║   ██║██║     ██║   ██║██║     ║██╔═██╗
██║     ██║  ██║███████║╚██████╔╝╚██████╔╝███████╗╚██████╔╝╚██████╔╝██║  ██╗
╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
{BLUE}            PascoLock – Advanced Password Security Toolkit
{BLACK}          [ Offline-First | Breach-Aware | Kali Linux ]
{RESET}
""")

# ================= CORE LOGIC =================
def entropy(password):
    pool = 0
    if re.search("[a-z]", password): pool += 26
    if re.search("[A-Z]", password): pool += 26
    if re.search("[0-9]", password): pool += 10
    if re.search("[^\\w]", password): pool += 32
    return round(len(password) * math.log2(pool), 2) if pool else 0

def crack_time(ent):
    sec = (2 ** ent) / 1e9
    if sec < 60: return f"{int(sec)} seconds"
    if sec < 3600: return f"{int(sec/60)} minutes"
    if sec < 86400: return f"{int(sec/3600)} hours"
    if sec < 31536000: return f"{int(sec/86400)} days"
    return f"{int(sec/31536000)} years"

def normalize_leet(p):
    for k, v in LEET_MAP.items():
        p = p.replace(k, v)
    return p.lower()

def detect_issues(p):
    issues = []
    if re.search(r"(.)\1{2,}", p):
        issues.append("Repeated characters detected")
    if re.search("(123|abc|qwerty)", p.lower()):
        issues.append("Sequential pattern detected")
    if p.lower() in COMMON_PASSWORDS:
        issues.append("Common password detected")
    if normalize_leet(p) in COMMON_PASSWORDS:
        issues.append("Leetspeak-based common password detected")
    return issues

def score(p):
    s = 0
    if len(p) >= 12: s += 20
    if re.search("[A-Z]", p): s += 15
    if re.search("[a-z]", p): s += 15
    if re.search("[0-9]", p): s += 15
    if re.search("[^\\w]", p): s += 15
    if not detect_issues(p): s += 20
    return min(s, 100)

def strength_bar(s):
    bar = "█" * (s // 10) + "░" * (10 - s // 10)
    color = RED if s < 40 else YELLOW if s < 70 else GREEN
    return f"{color}{bar}{RESET}"

# ================= HIBP BREACH CHECK =================
def hibp_check(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    try:
        r = requests.get(HIBP_API + prefix, timeout=5)
        for line in r.text.splitlines():
            h, count = line.split(":")
            if h == suffix:
                return int(count)
    except:
        return None
    return 0

# ================= POLICY =================
def load_policy(path):
    with open(path) as f:
        return json.load(f)

def check_policy(p, policy):
    errors = []
    if len(p) < policy.get("min_length", 0):
        errors.append("Minimum length violation")
    if policy.get("uppercase") and not re.search("[A-Z]", p):
        errors.append("Uppercase required")
    if policy.get("numbers") and not re.search("[0-9]", p):
        errors.append("Number required")
    if policy.get("symbols") and not re.search("[^\\w]", p):
        errors.append("Symbol required")
    return errors

# ================= GENERATORS =================
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# ================= REPORTS =================
def export_json(results):
    with open("pascolock_report.json", "w") as f:
        json.dump(results, f, indent=4)

def export_html(results):
    rows = ""
    for r in results:
        rows += f"<tr><td>{r['password']}</td><td>{r['score']}</td><td>{r['breach']}</td></tr>"

    html = f"""
    <html><body>
    <h1>PascoLock Password Audit Report</h1>
    <table border="1">
    <tr><th>Password</th><th>Score</th><th>Breach Count</th></tr>
    {rows}
    </table>
    </body></html>
    """
    open("pascolock_report.html", "w").write(html)

# ================= FILE AUDIT =================
def audit_file(path):
    results = []
    with open(path) as f:
        for line in f:
            p = line.strip()
            if not p: continue
            results.append(analyze(p, silent=True))
    export_json(results)
    export_html(results)
    print(f"{G}Reports generated: pascolock_report.json & pascolock_report.html{N}")

# ================= ANALYZE =================
def analyze(p, silent=False):
    ent = entropy(p)
    sc = score(p)
    breach = hibp_check(p)
    result = {
        "password": p,
        "entropy": ent,
        "score": sc,
        "crack_time": crack_time(ent),
        "breach": breach
    }

    if silent:
        return result

    print(f"\nEntropy        : {ent} bits")
    print(f"Crack time     : {crack_time(ent)}")
    print(f"Score          : {sc}/100")
    print(f"Strength bar   : {strength_bar(sc)}")

    issues = detect_issues(p)
    if issues:
        print(f"{RED}Issues:{RESET}")
        for i in issues:
            print(" -", i)

    if breach and breach > 0:
        print(f"{RED}⚠️ Found in {breach} breaches (HIBP){RESET}")
    else:
        print(f"{GREEN}No known breaches found{RESET}")

    return result

# ================= MAIN =================
def main():
    startup_animation()  # clear screen + progress bar + beep
    banner()             # show colored banner

    print("1) Check password")
    print("2) Generate strong password")
    choice = input("\nSelect option: ")

    if choice == "2":
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(chars) for _ in range(16))
        print(f"{GREEN}Generated password: {RESET}{password}")
        return

    password = getpass.getpass("\nEnter password (hidden): ")
    analyze(password)

    print("\nMode: OFFLINE-FIRST 🔒")
    print("PascoLock never stores or logs passwords.")

if __name__ == "__main__":
    main()
