def audit_file(path):
    with open(path) as  f:
        passwords = [line.strip() for line in f if line.strip()]

        results = []
        for p in passwords:
            results.append(analyze_password(p))
            return results
