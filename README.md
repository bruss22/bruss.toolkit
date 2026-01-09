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

```bash
pip install requests


⸻

Repository Layout

bruss.toolkit/
├── main.py                 # Core request logic (tkit class)
├── toolkit_v3_distro.py    # Traffic generation driver
├── urllist.csv             # URLs used to generate traffic
└── README.md


⸻

URL List Configuration

Populate urllist.csv with the destinations you want to generate traffic toward.

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

From the project directory:

python toolkit_v3_distro.py

When prompted:

Press 1 to generate traffic:

Press 1 to begin generating traffic.

Example Output

Trying https://www.google.com Result: 200 OK (143ms)
Trying https://www.youtube.com Result: 200 OK (231ms)

Stop execution at any time using Ctrl+C.

⸻

Default Runtime Behavior
	•	URLs are selected randomly from urllist.csv
	•	One request is sent every 1 second
	•	Request timeout is 6 seconds
	•	HTTP redirects are followed
	•	TLS certificate verification is enabled by default

⸻

SSL/TLS Deep Packet Inspection (DPI)

To validate DPI behavior, configure the toolkit to trust the same CA certificate used by the firewall performing inspection.

Configuration Steps
	1.	Copy the firewall DPI CA certificate to the system running the toolkit
	2.	Edit toolkit_v3_distro.py and set the certificate path:

ca_cert = "/home/fortinet/toolkit/FGTSPI.cer"

	3.	Ensure TLS verification is enabled:

insecure = False

The toolkit will now establish TLS sessions that are fully inspectable by the firewall while maintaining certificate trust.

⸻

Insecure Mode (Lab Only)

For quick validation where certificate trust is not required:

insecure = True

⚠️ Warning:
This disables TLS certificate validation and should only be used in isolated lab environments.

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

Author

Maintained by bruss22

