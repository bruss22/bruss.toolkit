### bruss.toolkit Overview

bruss.toolkit can be used to generate web traffic for both **web filtering** and **application steering**.

---

### URL Configuration

Populate `urllist.csv` with the desired URLs to be used for traffic generation.

---

### Deep Packet Inspection (DPI)

If Deep Packet Inspection is required:

- Place the CA certificate in the toolkit folder.
- Update the `main.py` file to reference the certificate.

Example:
```python
# First line is for DPI with cert referenced in folder used by FGT for DPI
response = requests.get(
    url[0],
    verify='/path/to/toolkit/certname.cer',
    timeout=12
)
