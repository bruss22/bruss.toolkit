#!/usr/bin/env python3
import csv
import random
import time

from main import tkit


def load_urls(path: str) -> list[str]:
    urls: list[str] = []
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if not row:
                continue
            u = (row[0] or "").strip()
            if not u:
                continue
            if u.lower() in {"url", "urls"}:  # optional header skip
                continue
            urls.append(u)
    return urls


def main():
    try:
        scope = int(input("Press 1 to generate traffic: ").strip() or "0")
    except ValueError:
        scope = 0

    if scope != 1:
        print("Exiting.")
        return

    print("Checking for urllist.csv")
    if not tkit.fileExists("urllist.csv"):
        print("urllist.csv not found")
        return

    urls = load_urls("urllist.csv")
    if not urls:
        print("urllist.csv contains no usable URLs")
        return

    print(f"Loaded {len(urls)} URLs. Press Ctrl+C to stop.")

    # Optional knobs (hard-coded like your original; easy to make CLI args later)
    sleep_seconds = 1
    timeout_seconds = 6

    # DPI example w/Cert verify. using site bypasses could result in SSL errors:
    #ca_cert = "./FGTDPI.cer"
    #insecure = False
    
    # Lab-only. Typically used for WF and APP Steering.:
    ca_cert = None
    insecure = True

    while True:
        try:
            url = random.choice(urls)
            result = tkit.urlRequest(
                url,
                timeout=timeout_seconds,
                ca_cert=ca_cert,
                insecure=insecure,
            )

            if result["ok"]:
                print(
                    f'Trying {result["url"]} Result: {result["status_code"]} '
                    f'{result["reason"] or ""} ({result["elapsed_ms"]}ms)'
                )
                time.sleep(sleep_seconds)
            else:
                print(f'error:{result["url"]} - {result["error"]} ({result["elapsed_ms"]}ms)')
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("Cancelled")
            break


if __name__ == "__main__":
    main()
