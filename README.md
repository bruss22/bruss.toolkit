# bruss.toolkit

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-lab%20tool-orange)
![Use Case](https://img.shields.io/badge/use%20case-SD--WAN%20%7C%20DPI%20%7C%20WebFilter-green)

`bruss.toolkit` is a lightweight Python utility designed to generate **deterministic HTTP/HTTPS web traffic** for validating:

- Web filtering policies
- Application steering (SD-WAN / SASE)
- SSL/TLS Deep Packet Inspection (DPI)

The toolkit is intentionally simple and predictable, making it well-suited for **FortiGate labs, POCs, demos, and validation testing**.

---

## Key Features

- Randomized URL selection from a CSV file
- Controlled request pacing (default: 1 request/second)
- HTTPS traffic compatible with **SSL/TLS DPI via custom CA certificates**
- Clear request feedback (status, reason, latency)
- Graceful shutdown using `Ctrl+C`

---

## Requirements

- Python **3.9+**
- Required Python package:
	- pip install requests

Fortigate notes:
- set all web filter categories to monitor or block to ensure logging is performed. Allow will not be logged.
- typically the default app control profile is fine for monitor.
- SDWAN App-Cache: `diag sys sdwan internet-service-app-ctrl-list` requires an sdwan rule using an application as destination to populate. 

⸻
```
Repository Layout

bruss.toolkit/
├── main.py                 # Core request logic (tkit class)
├── toolkit.py    			# Traffic generation driver
├── urllist.csv             # URLs used to generate traffic
├── quickstart.md
└── README.md


⸻

URL List Configuration

Populate urllist.csv with the destinations you want to generate traffic toward. I would reccomend seperate Application Steering(SDWAN) and Web FIlter lists.

Example urllist.csv

https://www.google.com
https://www.facebook.com
https://www.youtube.com
https://www.github.com

Parsing Rules
	•	One URL per line
	•	Blank lines are ignored
	•	Optional headers (url, urls) are skipped automatically
	•	HTTP and HTTPS are both supported

⸻

Running the Toolkit

See quickstart.md
⸻

Default Runtime Behavior
	•	insecure = True
	•	ca_cert = None
	•	URLs are selected randomly from urllist.csv
	•	One request is sent every 1 second
	•	Request timeout is 6 seconds
	•	HTTP redirects are followed

⸻

Tuning Request Rate and Timeouts

Within toolkit_v3_distro.py:

sleep_seconds = 1      # Delay between requests
timeout_seconds = 6    # Per-request timeout

Adjust these values to match lab scale, inspection capacity, or demo timing requirements.

⸻

Output Details

Each request reports:
	•	URL
	•	HTTP status code
	•	Response reason (if available)
	•	Request latency (milliseconds)

Error output may include:
	•	Timeout
	•	SSL/TLS validation errors
	•	General request failures

⸻

Intended Use Cases
	•	FortiGate web filtering validation
	•	SD-WAN application steering testing
	•	SSL/TLS DPI inspection verification
	•	SASE / ZTNA demo traffic generation
	•	Lab and POC environments

⸻

Known Limitations
	•	Single-threaded execution
	•	No retry or backoff logic
	•	No persistent logging to disk
	•	No command-line arguments (values set in code)

These limitations are intentional to preserve clarity, predictability, and transparency.

⸻

Roadmap (Optional Enhancements)
	•	Command-line argument support
	•	CSV / JSON request logging
	•	Retry and backoff logic
	•	URL weighting
	•	Optional concurrency
	•	Docker container support

⸻

Disclaimer

This tool is provided for testing and educational purposes only.
Do not use it to generate abusive, excessive, or unauthorized traffic.

⸻

Maintained by bruss22
```
