"""
=========================================================
CyberScope
Security Engine

Author : Krunal Paliwal

Production Version
=========================================================
"""

from __future__ import annotations

import ssl
import socket
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup


# ==========================================================
# HTTP SESSION
# ==========================================================

class HTTPSession:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
            "CyberScope Security Engine"

        })

        self.timeout = 10

    def get(self, url):

        return self.session.get(

            url,

            timeout=self.timeout,

            allow_redirects=True

        )


# ==========================================================
# SSL CERTIFICATE
# ==========================================================

class SSLCertificate:

    def lookup(self, hostname):

        try:

            context = ssl.create_default_context()

            with context.wrap_socket(

                socket.socket(),

                server_hostname=hostname

            ) as sock:

                sock.settimeout(10)

                sock.connect((hostname,443))

                cert = sock.getpeercert()

            return {

                "subject": cert.get("subject"),

                "issuer": cert.get("issuer"),

                "serial_number": cert.get("serialNumber"),

                "version": cert.get("version"),

                "not_before": cert.get("notBefore"),

                "not_after": cert.get("notAfter"),

                "subject_alt_names": cert.get("subjectAltName")

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# HTTP HEADERS
# ==========================================================

class HTTPHeaders:

    def lookup(self,url):

        try:

            response = HTTPSession().get(url)

            return dict(

                response.headers

            )

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# SECURITY HEADERS
# ==========================================================

class SecurityHeaders:

    HEADERS = [

        "Strict-Transport-Security",

        "Content-Security-Policy",

        "X-Frame-Options",

        "X-Content-Type-Options",

        "Referrer-Policy",

        "Permissions-Policy",

        "Cross-Origin-Embedder-Policy",

        "Cross-Origin-Resource-Policy",

        "Cross-Origin-Opener-Policy"

    ]

    def analyze(self,url):

        try:

            headers = HTTPSession().get(url).headers

            result = {}

            for item in self.HEADERS:

                result[item] = headers.get(

                    item,

                    "Missing"

                )

            return result

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# COOKIE ANALYZER
# ==========================================================

class CookieAnalyzer:

    def analyze(self,url):

        try:

            response = HTTPSession().get(url)

            cookies = []

            for cookie in response.cookies:

                cookies.append({

                    "name": cookie.name,

                    "secure": cookie.secure,

                    "expires": cookie.expires,

                    "domain": cookie.domain,

                    "path": cookie.path

                })

            return cookies

        except Exception as error:

            return {

                "error": str(error)

            }
# ==========================================================
# ROBOTS.TXT
# ==========================================================

class Robots:

    def fetch(self, url):

        try:

            robots_url = urljoin(url, "/robots.txt")

            response = HTTPSession().get(robots_url)

            return {

                "url": robots_url,

                "status": response.status_code,

                "content": response.text

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# SITEMAP.XML
# ==========================================================

class Sitemap:

    def fetch(self, url):

        try:

            sitemap_url = urljoin(url, "/sitemap.xml")

            response = HTTPSession().get(sitemap_url)

            return {

                "url": sitemap_url,

                "status": response.status_code,

                "content": response.text

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# FAVICON
# ==========================================================

class Favicon:

    def find(self, url):

        try:

            response = HTTPSession().get(url)

            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )

            icon = soup.find(

                "link",

                rel=lambda value:

                value and "icon" in value.lower()

            )

            if icon:

                return {

                    "favicon":

                        urljoin(

                            url,

                            icon.get("href")

                        )

                }

            return {

                "favicon":

                    urljoin(

                        url,

                        "/favicon.ico"

                    )

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# REDIRECT CHAIN
# ==========================================================

class RedirectChain:

    def analyze(self, url):

        try:

            response = HTTPSession().get(url)

            chain = []

            for item in response.history:

                chain.append({

                    "status": item.status_code,

                    "url": item.url

                })

            chain.append({

                "status": response.status_code,

                "url": response.url

            })

            return chain

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# SERVER FINGERPRINT
# ==========================================================

class ServerFingerprint:

    def detect(self, url):

        try:

            headers = HTTPSession().get(url).headers

            return {

                "server":

                    headers.get(

                        "Server",

                        "Unknown"

                    ),

                "powered_by":

                    headers.get(

                        "X-Powered-By",

                        "Unknown"

                    ),

                "via":

                    headers.get(

                        "Via",

                        "Unknown"

                    )

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# HSTS ANALYSIS
# ==========================================================

class HSTS:

    def analyze(self, url):

        try:

            headers = HTTPSession().get(url).headers

            value = headers.get(

                "Strict-Transport-Security"

            )

            return {

                "enabled": value is not None,

                "value": value

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# CSP ANALYSIS
# ==========================================================

class CSP:

    def analyze(self, url):

        try:

            headers = HTTPSession().get(url).headers

            policy = headers.get(

                "Content-Security-Policy"

            )

            return {

                "enabled": policy is not None,

                "policy": policy

            }

        except Exception as error:

            return {

                "error": str(error)

            }


# ==========================================================
# CORS ANALYSIS
# ==========================================================

class CORS:

    def analyze(self, url):

        try:

            headers = HTTPSession().get(url).headers

            return {

                "allow_origin":

                    headers.get(

                        "Access-Control-Allow-Origin"

                    ),

                "allow_methods":

                    headers.get(

                        "Access-Control-Allow-Methods"

                    ),

                "allow_headers":

                    headers.get(

                        "Access-Control-Allow-Headers"

                    )

            }

        except Exception as error:

            return {

                "error": str(error)

            }     
# ==========================================================
# TECHNOLOGY DETECTION
# ==========================================================

class TechnologyDetector:

    TECHNOLOGIES = {

        "WordPress": [
            "wp-content",
            "wp-includes"
        ],

        "Joomla": [
            "joomla"
        ],

        "Drupal": [
            "drupal"
        ],

        "React": [
            "react"
        ],

        "Angular": [
            "ng-version"
        ],

        "Vue": [
            "vue"
        ],

        "Bootstrap": [
            "bootstrap"
        ],

        "jQuery": [
            "jquery"
        ]

    }


    def detect(self, url):

        try:

            response = HTTPSession().get(url)

            source = response.text.lower()

            found = []

            for name, signatures in self.TECHNOLOGIES.items():

                for signature in signatures:

                    if signature.lower() in source:

                        found.append(name)

                        break


            return {

                "technologies": list(set(found))

            }


        except Exception as error:

            return {

                "error": str(error)

            }



# ==========================================================
# HTTP METHODS CHECK
# ==========================================================

class HTTPMethods:


    METHODS = [

        "GET",

        "POST",

        "PUT",

        "DELETE",

        "PATCH",

        "OPTIONS",

        "HEAD"

    ]


    def analyze(self,url):

        result = {}


        try:

            session = HTTPSession()


            for method in self.METHODS:


                try:

                    response = session.session.request(

                        method,

                        url,

                        timeout=5

                    )


                    result[method] = {

                        "status":

                            response.status_code

                    }


                except Exception:

                    result[method] = {

                        "status":

                            "Failed"

                    }


            return result



        except Exception as error:

            return {

                "error": str(error)

            }




# ==========================================================
# TLS INFORMATION
# ==========================================================

class TLSInformation:


    def analyze(self,hostname):

        try:

            context = ssl.create_default_context()


            with context.wrap_socket(

                socket.socket(),

                server_hostname=hostname

            ) as sock:


                sock.settimeout(10)


                sock.connect(

                    (

                        hostname,

                        443

                    )

                )


                cipher = sock.cipher()

                version = sock.version()



            return {


                "tls_version":

                    version,


                "cipher":

                    cipher[0],


                "bits":

                    cipher[2]


            }


        except Exception as error:


            return {

                "error": str(error)

            }





# ==========================================================
# CERTIFICATE SUMMARY
# ==========================================================

class CertificateSummary:


    def generate(self,certificate):


        try:


            return {


                "issuer":

                    certificate.get(

                        "issuer"

                    ),


                "subject":

                    certificate.get(

                        "subject"

                    ),


                "valid_from":

                    certificate.get(

                        "not_before"

                    ),


                "valid_until":

                    certificate.get(

                        "not_after"

                    ),


                "serial":

                    certificate.get(

                        "serial_number"

                    )


            }


        except Exception as error:


            return {


                "error":

                    str(error)

            }





# ==========================================================
# SECURITY SCORE
# ==========================================================

class SecurityScore:



    def calculate(self,data):


        score = 100


        checks = {


            "ssl":

                data.get(

                    "ssl",

                    {}

                ),


            "headers":

                data.get(

                    "security_headers",

                    {}

                )

        }



        ssl_data = checks["ssl"]


        if "error" in ssl_data:

            score -= 30



        headers = checks["headers"]


        for key,value in headers.items():


            if value == "Missing":

                score -= 5



        if score < 0:

            score = 0



        return {


            "score":

                score,


            "rating":

                self.rating(score)

        }



    def rating(self,score):


        if score >= 90:

            return "Excellent"


        elif score >= 70:

            return "Good"


        elif score >= 50:

            return "Medium"


        else:

            return "Low"
          # ==========================================================
# SECURITY ENGINE
# ==========================================================

from concurrent.futures import ThreadPoolExecutor



class SecurityEngine:


    def __init__(self):


        self.ssl = SSLCertificate()

        self.headers = HTTPHeaders()

        self.security_headers = SecurityHeaders()

        self.cookies = CookieAnalyzer()

        self.robots = Robots()

        self.sitemap = Sitemap()

        self.favicon = Favicon()

        self.redirect = RedirectChain()

        self.server = ServerFingerprint()

        self.hsts = HSTS()

        self.csp = CSP()

        self.cors = CORS()

        self.tech = TechnologyDetector()

        self.methods = HTTPMethods()

        self.tls = TLSInformation()

        self.score = SecurityScore()




    # ======================================================
    # MAIN SCAN
    # ======================================================


    def scan(self,url):


        hostname = (

            url

            .replace(

                "https://",

                ""

            )

            .replace(

                "http://",

                ""

            )

            .split("/")[0]

        )



        result = {


            "target":

                url,


            "security":

                {}

        }




        tasks = {


            "headers":

                lambda:

                self.headers.lookup(url),



            "security_headers":

                lambda:

                self.security_headers.analyze(url),



            "cookies":

                lambda:

                self.cookies.analyze(url),



            "robots":

                lambda:

                self.robots.fetch(url),



            "sitemap":

                lambda:

                self.sitemap.fetch(url),



            "favicon":

                lambda:

                self.favicon.find(url),



            "redirects":

                lambda:

                self.redirect.analyze(url),



            "server":

                lambda:

                self.server.detect(url),



            "hsts":

                lambda:

                self.hsts.analyze(url),



            "csp":

                lambda:

                self.csp.analyze(url),



            "cors":

                lambda:

                self.cors.analyze(url),



            "technology":

                lambda:

                self.tech.detect(url),



            "methods":

                lambda:

                self.methods.analyze(url),



            "ssl":

                lambda:

                self.ssl.lookup(hostname),



            "tls":

                lambda:

                self.tls.analyze(hostname)

        }



        with ThreadPoolExecutor(

            max_workers=10

        ) as executor:


            futures = {


                name:

                executor.submit(task)

                for name,task in tasks.items()

            }



            for name,future in futures.items():


                try:


                    result["security"][name] = (

                        future.result()

                    )


                except Exception as error:


                    result["security"][name] = {


                        "error":

                            str(error)

                    }




        result["security"]["score"] = (

            self.score.calculate(

                result["security"]

            )

        )



        return result




# ==========================================================
# JSON REPORT FORMAT
# ==========================================================


class SecurityReport:



    @staticmethod

    def create(data):


        return {


            "CyberScope":

                {


                    "module":

                        "Security Engine",


                    "version":

                        "2.0"



                },


            "report":

                data



        }




# ==========================================================
# MODULE INFORMATION
# ==========================================================


MODULE_NAME = "Security Assessment Engine"

MODULE_VERSION = "2.0"

MODULE_AUTHOR = "CyberScope"



# ==========================================================
# SELF TEST
# ==========================================================


def self_test():


    print("=" * 60)

    print(MODULE_NAME)

    print("Version:", MODULE_VERSION)

    print("=" * 60)



    target = input(

        "Target URL : "

    ).strip()



    if not target:


        print(

            "Target missing"

        )

        return



    engine = SecurityEngine()



    report = engine.scan(

        target

    )



    final = SecurityReport.create(

        report

    )



    import json



    print(

        json.dumps(

            final,

            indent=4

        )

    )





# ==========================================================
# DIRECT EXECUTION
# ==========================================================


if __name__ == "__main__":


    self_test()
