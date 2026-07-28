"""
=========================================================
CyberScope
Reconnaissance Engine

Author : Krunal Paliwal

Production Version
=========================================================
"""

from __future__ import annotations

import socket
import time
import ipaddress
import concurrent.futures

from urllib.parse import urlparse

import dns.resolver
import requests
import whois

from bs4 import BeautifulSoup


# ==========================================================
# COMMON HTTP SESSION
# ==========================================================

class HTTPSession:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
            "CyberScope Recon Engine"

        })

        self.timeout = 10

    def get(self, url):

        return self.session.get(

            url,

            timeout=self.timeout,

            allow_redirects=True

        )


# ==========================================================
# URL VALIDATOR
# ==========================================================

class URLValidator:

    @staticmethod
    def normalize(target):

        target = target.strip()

        if not target.startswith("http"):

            target = "https://" + target

        return target

    @staticmethod
    def hostname(target):

        return urlparse(

            URLValidator.normalize(target)

        ).hostname

    @staticmethod
    def validate(target):

        try:

            host = URLValidator.hostname(target)

            socket.gethostbyname(host)

            return True

        except Exception:

            return False


# ==========================================================
# DNS LOOKUP
# ==========================================================

class DNSLookup:

    RECORDS = [

        "A",

        "AAAA",

        "MX",

        "NS",

        "TXT",

        "SOA",

        "CNAME"

    ]

    def lookup(self, domain):

        result = {}

        for record in self.RECORDS:

            try:

                answers = dns.resolver.resolve(

                    domain,

                    record

                )

                result[record] = [

                    str(x)

                    for x in answers

                ]

            except Exception:

                result[record] = []

        return result


# ==========================================================
# REAL IP
# ==========================================================

class IPLookup:

    def lookup(self, domain):

        ip = socket.gethostbyname(domain)

        return {

            "hostname": domain,

            "ip": ip

        }


# ==========================================================
# REVERSE DNS
# ==========================================================

class ReverseDNS:

    def lookup(self, ip):

        try:

            host = socket.gethostbyaddr(ip)

            return {

                "hostname": host[0],

                "aliases": host[1],

                "addresses": host[2]

            }

        except Exception:

            return None


# ==========================================================
# RESPONSE TIME
# ==========================================================

class ResponseTime:

    def measure(self, url):

        session = HTTPSession()

        start = time.time()

        session.get(url)

        end = time.time()

        return round(

            (end-start)*1000,

            2

        )


# ==========================================================
# PERFORMANCE
# ==========================================================

class Performance:

    def analyze(self, url):

        session = HTTPSession()

        response = session.get(url)

        return {

            "status":

                response.status_code,

            "server":

                response.headers.get(

                    "Server",

                    "Unknown"

                ),

            "content_type":

                response.headers.get(

                    "Content-Type",

                    ""

                ),

            "content_length":

                response.headers.get(

                    "Content-Length",

                    "Unknown"

                )
          import json

# ==========================================================
# WHOIS LOOKUP
# ==========================================================

class WhoisLookup:

    def lookup(self, domain):

        try:

            info = whois.whois(domain)

            return {

                "domain": info.domain_name,

                "registrar": info.registrar,

                "creation_date": str(info.creation_date),

                "expiration_date": str(info.expiration_date),

                "updated_date": str(info.updated_date),

                "name_servers": info.name_servers,

                "emails": info.emails,

                "country": info.country,

                "status": info.status

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# GEO IP LOOKUP
# ==========================================================

class GeoIP:

    API = "https://ipapi.co/{}/json/"

    def lookup(self, ip):

        try:

            response = requests.get(

                self.API.format(ip),

                timeout=10

            )

            data = response.json()

            return {

                "ip": data.get("ip"),

                "city": data.get("city"),

                "region": data.get("region"),

                "country": data.get("country_name"),

                "postal": data.get("postal"),

                "timezone": data.get("timezone"),

                "latitude": data.get("latitude"),

                "longitude": data.get("longitude"),

                "org": data.get("org")

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# ASN LOOKUP
# ==========================================================

class ASNLookup:

    API = "https://ipapi.co/{}/json/"

    def lookup(self, ip):

        try:

            response = requests.get(

                self.API.format(ip),

                timeout=10

            )

            data = response.json()

            return {

                "asn": data.get("asn"),

                "network": data.get("network"),

                "org": data.get("org"),

                "country": data.get("country_name")

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# HOST INFORMATION
# ==========================================================

class HostInformation:

    def collect(self, domain):

        result = {}

        try:

            result["fqdn"] = socket.getfqdn(domain)

        except Exception:

            result["fqdn"] = None

        try:

            result["ipv4"] = socket.gethostbyname(domain)

        except Exception:

            result["ipv4"] = None

        try:

            result["ipv6"] = socket.getaddrinfo(

                domain,

                None,

                socket.AF_INET6

            )[0][4][0]

        except Exception:

            result["ipv6"] = None

        return result


# ==========================================================
# PORT CHECK
# ==========================================================

class PortCheck:

    COMMON_PORTS = {

        80: "HTTP",

        443: "HTTPS",

        21: "FTP",

        22: "SSH",

        25: "SMTP",

        53: "DNS",

        110: "POP3",

        143: "IMAP"

    }

    def scan(self, host):

        result = {}

        for port, service in self.COMMON_PORTS.items():

            sock = socket.socket()

            sock.settimeout(1)

            try:

                status = sock.connect_ex(

                    (host, port)

                )

                result[port] = {

                    "service": service,

                    "open": status == 0

                }

            except Exception:

                result[port] = {

                    "service": service,

                    "open": False

                }

            finally:

                sock.close()

        return result


# ==========================================================
# DOMAIN INFORMATION
# ==========================================================

class DomainInformation:

    def collect(self, target):

        url = URLValidator.normalize(target)

        host = URLValidator.hostname(target)

        return {

            "url": url,

            "hostname": host,

            "valid": URLValidator.validate(target)

        }


# ==========================================================
# JSON EXPORT
# ==========================================================

class ReconResult:

    @staticmethod
    def to_json(data):

        return json.dumps(

            data,

            indent=4,

            default=str

        )
      # ==========================================================
# RECONNAISSANCE ENGINE
# ==========================================================

class ReconnaissanceEngine:

    def __init__(self):

        self.validator = URLValidator()

        self.dns = DNSLookup()

        self.ip = IPLookup()

        self.reverse = ReverseDNS()

        self.geo = GeoIP()

        self.asn = ASNLookup()

        self.whois = WhoisLookup()

        self.performance = Performance()

        self.response = ResponseTime()

        self.host = HostInformation()

        self.port = PortCheck()

        self.domain = DomainInformation()

    # ==================================================

    def run(self, target):

        result = {

            "target": target,

            "success": False,

            "data": {},

            "errors": []

        }

        info = self.domain.collect(target)

        result["data"]["domain"] = info

        if not info["valid"]:

            result["errors"].append(

                "Invalid or unreachable target."

            )

            return result

        hostname = info["hostname"]

        url = info["url"]

        # --------------------------------------------

        # Parallel Tasks

        # --------------------------------------------

        with concurrent.futures.ThreadPoolExecutor(

            max_workers=8

        ) as executor:

            futures = {

                "dns":

                    executor.submit(

                        self.dns.lookup,

                        hostname

                    ),

                "ip":

                    executor.submit(

                        self.ip.lookup,

                        hostname

                    ),

                "whois":

                    executor.submit(

                        self.whois.lookup,

                        hostname

                    ),

                "performance":

                    executor.submit(

                        self.performance.analyze,

                        url

                    ),

                "response":

                    executor.submit(

                        self.response.measure,

                        url

                    ),

                "host":

                    executor.submit(

                        self.host.collect,

                        hostname

                    )

            }

            for key, future in futures.items():

                try:

                    result["data"][key] = future.result()

                except Exception as error:

                    result["errors"].append(

                        f"{key}: {error}"

                    )

        # --------------------------------------------

        # IP Related

        # --------------------------------------------

        ip = None

        try:

            ip = result["data"]["ip"]["ip"]

        except Exception:

            pass

        if ip:

            try:

                result["data"]["reverse_dns"] = (

                    self.reverse.lookup(ip)

                )

            except Exception:

                result["data"]["reverse_dns"] = None

            try:

                result["data"]["geoip"] = (

                    self.geo.lookup(ip)

                )

            except Exception:

                result["data"]["geoip"] = None

            try:

                result["data"]["asn"] = (

                    self.asn.lookup(ip)

                )

            except Exception:

                result["data"]["asn"] = None

            try:

                result["data"]["ports"] = (

                    self.port.scan(ip)

                )

            except Exception:

                result["data"]["ports"] = {}

        result["success"] = True

        return result


# ==========================================================
# SIMPLE API
# ==========================================================

def scan_target(target):

    engine = ReconnaissanceEngine()

    return engine.run(target)

        }
# ==========================================================
# RETRY HELPER
# ==========================================================

class Retry:

    @staticmethod
    def execute(function, *args, retries=3, delay=1):

        last_error = None

        for _ in range(retries):

            try:

                return function(*args)

            except Exception as error:

                last_error = error

                time.sleep(delay)

        raise last_error


# ==========================================================
# NETWORK HEALTH
# ==========================================================

class NetworkHealth:

    @staticmethod
    def internet():

        try:

            requests.get(

                "https://www.google.com",

                timeout=5

            )

            return True

        except Exception:

            return False


# ==========================================================
# RESULT FORMATTER
# ==========================================================

class ResultFormatter:

    @staticmethod
    def pretty(result):

        lines = []

        lines.append("=" * 60)

        lines.append("CyberScope Reconnaissance Report")

        lines.append("=" * 60)

        lines.append("")

        for key, value in result["data"].items():

            lines.append(f"[{key.upper()}]")

            lines.append(str(value))

            lines.append("")

        if result["errors"]:

            lines.append("Errors")

            lines.append("-" * 60)

            for error in result["errors"]:

                lines.append(error)

                lines.append("")

        return "\n".join(lines)


# ==========================================================
# VERSION
# ==========================================================

ENGINE_NAME = "CyberScope Reconnaissance"

ENGINE_VERSION = "2.0"


# ==========================================================
# SELF TEST
# ==========================================================

def self_test():

    print("=" * 50)

    print(ENGINE_NAME)

    print(ENGINE_VERSION)

    print("=" * 50)

    if NetworkHealth.internet():

        print("[OK] Internet Connection")

    else:

        print("[FAILED] No Internet")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    self_test()

    target = input(

        "\nTarget : "

    ).strip()

    if not target:

        print("No target supplied.")

        raise SystemExit(0)

    engine = ReconnaissanceEngine()

    result = engine.run(target)

    print(

        ResultFormatter.pretty(

            result

        )

    )
