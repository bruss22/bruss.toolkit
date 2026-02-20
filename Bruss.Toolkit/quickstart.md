## Quick Start

This toolkit generates web traffic for testing **web filtering**, **application control**, and **SSL inspection** behavior on a FortiGate.

By default, the toolkit is configured for **quick testing** and **ease of use**.

---

### Default Behavior (Out of the Box)

The toolkit ships with the following defaults:

```
ca_cert = None
insecure = True
```
This means:
	•	TLS certificate verification is disabled
	•	HTTPS requests will succeed regardless of SSL inspection or certificate trust
	•	No FortiGate CA is required initially

✅ This mode is ideal for:<br>
	•	quick web filtering tests:<br>
	•	application steering validation:<br>
	•	initial connectivity checks:<br>
	•	lab environments:<br>

⸻

Basic Usage
	1.	Clone the repository:

- `git clone https://github.com/bruss22/bruss.toolkit.git`
	
- `cd bruss.toolkit/Bruss.Toolkit`

Populate urllist.csv with the URLs you want to test:

```csv
https://www.google.com
https://www.yahoo.com
https://example.com
```
Run the toolkit:
```
python3 toolkit.py
Press 1 to generate traffic: 1
Checking for urllist.csv
Loaded 31 URLs. Press Ctrl+C to stop.
Trying https://x.com Result: 200 OK (169ms)
Trying https://yahoo.com Result: 200 OK (628ms)
```
Traffic will be generated using HTTPS requests with certificate validation disabled.

⸻

Enabling Deep Inspection (DPI) Validation

If you want to validate Deep Inspection behavior (recommended for security testing), you must explicitly enable TLS verification.

Step 1 — Export the FortiGate Deep-Inspection CA

    From the FortiGate:
	•	System → Certificates
	•	Export the Deep-Inspection CA
	•	Format: PEM / Base64
	•	Replace or paste contents into filename: FGTDPI.cer
⸻

Step 2 — Choose a Trust Mode

Option A — No DPI Exceptions (Strict DPI-Only Mode)
Use this only if all HTTPS traffic is deep-inspected.
```
ca_cert = "./FGTDPI.cer"
insecure = False
```
Behavior:<br>
	•	✅ DPI-inspected traffic succeeds<br>
	•	❌ Any non-DPI or bypassed traffic fails TLS validation<br>

⸻

Option B — DPI Exceptions Present (Recommended)
If any DPI exceptions or bypass rules exist, install the FortiGate CA into the OS trust store.

Ubuntu 22.04 / 24.04:
```
sudo cp FGTDPI.cer /usr/local/share/ca-certificates/FGTDPI.crt
sudo update-ca-certificates
```
Then configure:
- do not reference cert
```
ca_cert = None
insecure = False
```
Behavior:<br>
	•	✅ DPI traffic succeeds<br>
	•	✅ Non-DPI / exception traffic succeeds<br>
	•	✅ OpenSSL, curl, Python, and browsers behave consistently<br>

⸻

Verifying DPI

Fortigate DPI Security Profile:<br>
- set ssl-exemption-log enable<br>
- set ssl-server-cert-log enable<br>
- set ssl-handshake-log enable(SSL Security Log example below) <br>

- <img width="411" height="530" alt="image" src="https://github.com/user-attachments/assets/78f4ec9b-c5ce-461b-8359-719dfc9cd348" />



To confirm whether traffic is being deep-inspected, run:
```
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
| openssl x509 -noout -issuer
```
- Fortinet / FG… issuer → DPI active
- Public CA issuer → DPI bypass or exception

No Exception in Profile or strict DPI:
```bash
 openssl s_client -connect cnn.com:443 -servername cnn.com </dev/null 2>/dev/null | openssl x509 -noout -issuer
```
- issuer=C = US, ST = California, L = Sunnyvale, O = Fortinet, OU = Certificate Authority, CN = FG121GTK23000612, emailAddress = support@fortinet.com

Exception
```bash
openssl s_client -connect yahoo.com:443 -servername yaoo.com </dev/null 2>/dev/null | openssl x509 -noout -issuer
```
- issuer=C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert SHA2 High Assurance Server CA

⸻

Note:
SSL verification failures are expected when TLS verification is enabled but the FortiGate CA is not trusted. This indicates inspection coverage issues, not a toolkit error.
