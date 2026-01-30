import hashlib
import requests

HIBP_API = "https://api.pwnedpasswords.com/range/"

def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    r = requests.get(HIBP_API + prefix, timeout=5)
    if r.status_code != 200:
        return None
    for line in r.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0

if __name__ == "__main__":
    print ("Testing HIBP Check...")
    print ("Result:", check_breach("password")) 
