import requests
from urllib.parse import urljoin

ORIGINS = [
    "https://your-domain.com",
    "null",
    "https://sub.your-domain.com",
    "https://another.sub.your-domain.com"
]

DANGEROUS = []

def test_cors(base_url):
    print(f"\n🔍 Testing CORS for {base_url}")
    for origin in ORIGINS:
        cookies = {
            "session": "FxtE2wTYuE2iKTLUFi9slJZWsPVFu4g2"
        }

        headers = {
            "Origin": origin,
            "Referer": "https://0acd00f7031a533480a8cb3800b9008e.web-security-academy.net/my-account?id=wiener",
            "Accept": "*/*"
        }

        try:
            resp = requests.get(base_url, headers=headers, cookies=cookies, timeout=5)
        except Exception as e:
            print(f"  ⚠️ Error with origin={origin}: {e}")
            continue

        acao = resp.headers.get("Access-Control-Allow-Origin")
        acc = resp.headers.get("Access-Control-Allow-Credentials")
        print(f"  Origin={origin:40} → ACAO={acao}, ACC={acc}")

        if acc == "true":
            print("    🚨 RED ALERT: Access-Control-Allow-Credentials: true")
            DANGEROUS.append((base_url, origin, acao, acc))
        elif acao == "*":
            print("    ⚠️ WARNING: wildcard '*' allowed")
            DANGEROUS.append((base_url, origin, acao, acc))

def main():
    endpoints = [
        "https://0acd00f7031a533480a8cb3800b9008e.web-security-academy.net/accountDetails"
    ]

    for ep in endpoints:
        test_cors(ep)

    if DANGEROUS:
        print("\n\n=== SUMMARY OF POTENTIALLY DANGEROUS CONFIGURATIONS ===")
        for url, origin, acao, acc in DANGEROUS:
            print(f"{url}  Origin={origin}  ACAO={acao}  ACC={acc}")
    else:
        print("\n✅ No risky CORS policies detected.")

if __name__ == "__main__":
    main()
