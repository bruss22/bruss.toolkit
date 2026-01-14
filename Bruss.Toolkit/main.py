#!/usr/bin/env python3
import time
from os.path import exists
from typing import Optional
import requests
import urllib3


class tkit:
    @staticmethod
    def fileExists(filename: str) -> bool:
        return exists(filename)

    @staticmethod
    def urlRequest(
        url: str,
        *,
        timeout: int = 6,
        ca_cert: Optional[str] = None,
        insecure: bool = False,
    ) -> dict:
        """
        Makes a GET request to `url`.

        Returns a consistent dict:
          {
            "url": str,
            "ok": bool,
            "status_code": int | None,
            "reason": str | None,
            "elapsed_ms": int,
            "error": str | None
          }

        DPI:
          - pass ca_cert="/path/to/FGT_CA.cer" to validate TLS using your DPI CA
        Lab-only insecure:
          - set insecure=True to skip TLS verification (not recommended)
        """
        if insecure:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        verify_value = True
        if ca_cert:
            verify_value = ca_cert
        elif insecure:
            verify_value = False

        headers = {"User-Agent": "bruss.toolkit/1.0"}

        start = time.time()
        try:
            resp = requests.get(
                url,
                timeout=timeout,
                verify=verify_value,
                headers=headers,
                allow_redirects=True,
            )
            elapsed_ms = int(resp.elapsed.total_seconds() * 1000)
            return {
                "url": url,
                "ok": True,
                "status_code": resp.status_code,
                "reason": getattr(resp, "reason", None),
                "elapsed_ms": elapsed_ms,
                "error": None,
            }

        except requests.exceptions.Timeout:
            elapsed_ms = int((time.time() - start) * 1000)
            return {
                "url": url,
                "ok": False,
                "status_code": None,
                "reason": None,
                "elapsed_ms": elapsed_ms,
                "error": "timeout",
            }

        except requests.exceptions.SSLError as e:
            elapsed_ms = int((time.time() - start) * 1000)
            return {
                "url": url,
                "ok": False,
                "status_code": None,
                "reason": None,
                "elapsed_ms": elapsed_ms,
                "error": f"ssl_error: {e}",
            }

        except requests.exceptions.RequestException as e:
            elapsed_ms = int((time.time() - start) * 1000)
            return {
                "url": url,
                "ok": False,
                "status_code": None,
                "reason": None,
                "elapsed_ms": elapsed_ms,
                "error": f"request_error: {e}",
            }
