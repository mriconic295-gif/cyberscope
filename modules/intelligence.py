"""
=========================================================
CyberScope
Intelligence Engine

Public Information Intelligence Module

Version : 2.0
=========================================================
"""


from __future__ import annotations


import socket
import requests

from urllib.parse import urlparse

from bs4 import BeautifulSoup



# ==========================================================
# HTTP CLIENT
# ==========================================================


class IntelligenceSession:


    def __init__(self):


        self.session = requests.Session()


        self.session.headers.update({

            "User-Agent":

            "CyberScope Intelligence Engine"

        })


        self.timeout = 10



    def get(self,url):


        return self.session.get(

            url,

            timeout=self.timeout,

            allow_redirects=True

        )





# ==========================================================
# DOMAIN PARSER
# ==========================================================


class DomainParser:



    def extract(self,url):


        try:


            if not url.startswith("http"):


                url = "https://" + url



            parsed = urlparse(url)



            hostname = parsed.hostname



            return {


                "domain":

                    hostname,


                "scheme":

                    parsed.scheme,


                "port":

                    parsed.port,


                "path":

                    parsed.path


            }



        except Exception as error:


            return {


                "error":

                    str(error)

            }





# ==========================================================
# DNS INTELLIGENCE
# ==========================================================


class DNSIntelligence:



    def lookup(self,domain):


        result = {}



        try:


            ip = socket.gethostbyname(domain)



            result["ip"] = ip



        except Exception as error:


            result["ip_error"] = str(error)




        try:


            hostname = socket.getfqdn(domain)



            result["hostname"] = hostname



        except Exception as error:


            result["hostname_error"] = str(error)



        return result





# ==========================================================
# IP INTELLIGENCE
# ==========================================================


class IPIntelligence:



    def lookup(self,ip):


        try:


            response = requests.get(

                f"https://ipapi.co/{ip}/json/",

                timeout=5

            )


            data = response.json()



            return {


                "country":

                    data.get(

                        "country_name"

                    ),


                "region":

                    data.get(

                        "region"

                    ),


                "city":

                    data.get(

                        "city"

                    ),


                "org":

                    data.get(

                        "org"

                    ),


                "asn":

                    data.get(

                        "asn"

                    )


            }



        except Exception as error:


            return {


                "error":

                    str(error)

            }





# ==========================================================
# PAGE METADATA ANALYZER
# ==========================================================


class MetadataAnalyzer:



    def analyze(self,url):


        try:


            response = IntelligenceSession().get(url)



            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )



            title = soup.find("title")



            description = soup.find(

                "meta",

                attrs={

                    "name":"description"

                }

            )



            keywords = soup.find(

                "meta",

                attrs={

                    "name":"keywords"

                }

            )



            return {


                "title":

                    title.text.strip()

                    if title

                    else None,



                "description":

                    description.get("content")

                    if description

                    else None,



                "keywords":

                    keywords.get("content")

                    if keywords

                    else None



            }



        except Exception as error:


            return {


                "error":

                    str(error)

            }
          # ==========================================================
# TECHNOLOGY INTELLIGENCE
# ==========================================================


class TechnologyIntelligence:



    SIGNATURES = {


        "WordPress":

            [

                "wp-content",

                "wp-includes"

            ],


        "Shopify":

            [

                "cdn.shopify.com",

                "shopify"

            ],


        "Laravel":

            [

                "laravel"

            ],


        "Django":

            [

                "csrfmiddlewaretoken"

            ],


        "React":

            [

                "react",

                "_reactroot"

            ],


        "Vue":

            [

                "vue"

            ],


        "Angular":

            [

                "ng-version"

            ],


        "Bootstrap":

            [

                "bootstrap"

            ]

    }



    def detect(self,url):


        try:


            response = IntelligenceSession().get(url)



            source = response.text.lower()



            detected = []



            for name,items in self.SIGNATURES.items():


                for item in items:


                    if item.lower() in source:


                        detected.append(name)

                        break




            return {


                "technologies":

                    list(set(detected))

            }




        except Exception as error:


            return {


                "error":

                    str(error)

            }







# ==========================================================
# WEB SERVER ANALYSIS
# ==========================================================


class WebServerAnalysis:



    def analyze(self,url):


        try:


            response = IntelligenceSession().get(url)



            headers = response.headers



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



                "cache":

                    headers.get(

                        "Cache-Control",

                        "Unknown"

                    ),



                "encoding":

                    headers.get(

                        "Content-Encoding",

                        "Unknown"

                    )

            }




        except Exception as error:


            return {


                "error":

                    str(error)

            }






# ==========================================================
# PUBLIC LINK EXTRACTOR
# ==========================================================


class PublicLinkExtractor:



    def extract(self,url):


        try:


            response = IntelligenceSession().get(url)



            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )



            links = []



            for link in soup.find_all(

                "a",

                href=True

            ):


                href = link["href"]



                if href.startswith(

                    "http"

                ):


                    links.append(href)




            return {


                "links":

                    list(set(links))

            }




        except Exception as error:


            return {


                "error":

                    str(error)

            }





# ==========================================================
# DOMAIN INFORMATION
# ==========================================================


class DomainInformation:



    def analyze(self,domain):


        result = {



            "domain":

                domain,



            "length":

                len(domain),



            "contains_digits":

                any(

                    char.isdigit()

                    for char in domain

                ),



            "contains_dash":

                "-" in domain

        }



        return result






# ==========================================================
# EMAIL PATTERN ANALYZER
# ==========================================================


class EmailPatternAnalyzer:



    def analyze(self,url):


        try:


            response = IntelligenceSession().get(url)



            text = response.text



            emails = []



            import re



            matches = re.findall(

                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

                text

            )



            for email in matches:


                emails.append(email)



            return {


                "emails":

                    list(set(emails))

            }




        except Exception as error:


            return {


                "error":

                    str(error)

            }





# ==========================================================
# INTELLIGENCE FORMATTER
# ==========================================================


class IntelligenceFormatter:



    @staticmethod

    def format(data):


        return {


            "module":

                "CyberScope Intelligence",



            "version":

                "2.0",



            "data":

                data

        }
      # ==========================================================
# INTELLIGENCE ENGINE
# ==========================================================


from concurrent.futures import ThreadPoolExecutor





class IntelligenceEngine:



    def __init__(self):


        self.domain = DomainParser()


        self.dns = DNSIntelligence()


        self.ip = IPIntelligence()


        self.metadata = MetadataAnalyzer()


        self.tech = TechnologyIntelligence()


        self.server = WebServerAnalysis()


        self.links = PublicLinkExtractor()


        self.domain_info = DomainInformation()


        self.email = EmailPatternAnalyzer()





    # ======================================================
    # MAIN INTELLIGENCE SCAN
    # ======================================================


    def scan(self,target):


        if not target.startswith("http"):


            url = "https://" + target


        else:


            url = target




        parsed = self.domain.extract(url)



        domain = parsed.get(

            "domain"

        )



        result = {



            "target":

                target,



            "domain":

                {},



            "network":

                {},



            "website":

                {},



            "risk":

                {}

        }





        tasks = {



            "domain_info":

                lambda:

                self.domain_info.analyze(

                    domain

                ),




            "dns":

                lambda:

                self.dns.lookup(

                    domain

                ),





            "metadata":

                lambda:

                self.metadata.analyze(

                    url

                ),





            "technology":

                lambda:

                self.tech.detect(

                    url

                ),





            "server":

                lambda:

                self.server.analyze(

                    url

                ),





            "links":

                lambda:

                self.links.extract(

                    url

                ),





            "emails":

                lambda:

                self.email.analyze(

                    url

                )

        }





        with ThreadPoolExecutor(

            max_workers=8

        ) as executor:


            jobs = {


                name:

                executor.submit(task)

                for name,task in tasks.items()

            }



            for name,job in jobs.items():


                try:


                    data = job.result()



                    if name in [

                        "dns"

                    ]:


                        result["network"][name] = data



                    else:


                        result["website"][name] = data




                except Exception as error:


                    result["website"][name] = {


                        "error":

                            str(error)

                    }





        result["risk"] = self.calculate_risk(

            result

        )



        return result






    # ======================================================
    # RISK INDICATOR
    # ======================================================


    def calculate_risk(self,data):


        score = 100



        warnings = []




        tech = data["website"].get(

            "technology",

            {}

        )



        if not tech.get("technologies"):


            warnings.append(

                "Technology information unavailable"

            )


            score -= 5




        server = data["website"].get(

            "server",

            {}

        )



        if server.get("server") != "Unknown":


            warnings.append(

                "Server information exposed"

            )


            score -= 10





        metadata = data["website"].get(

            "metadata",

            {}

        )



        if not metadata.get("description"):


            warnings.append(

                "Missing website description"

            )


            score -= 5





        if score < 0:


            score = 0





        return {


            "score":

                score,



            "level":

                self.level(score),



            "warnings":

                warnings

        }






    def level(self,score):


        if score >= 85:


            return "Low Risk"



        elif score >= 60:


            return "Medium Risk"



        else:


            return "High Risk"
          # ==========================================================
# INTELLIGENCE REPORT GENERATOR
# ==========================================================


class IntelligenceReport:



    @staticmethod

    def create(data):


        return {


            "CyberScope":

                {


                    "module":

                        "Intelligence Engine",



                    "version":

                        "2.0",



                    "type":

                        "Public Intelligence Report"

                },



            "report":

                data

        }






    @staticmethod

    def summary(data):


        return {


            "target":

                data.get(

                    "target"

                ),



            "risk_score":

                data.get(

                    "risk",

                    {}

                ).get(

                    "score"

                ),



            "risk_level":

                data.get(

                    "risk",

                    {}

                ).get(

                    "level"

                ),



            "technologies":

                data.get(

                    "website",

                    {}

                )

                .get(

                    "technology",

                    {}

                )

                .get(

                    "technologies",

                    []

                )

        }







# ==========================================================
# EXPORT HELPER
# ==========================================================


class IntelligenceExporter:



    @staticmethod

    def save_json(data,path="intelligence_report.json"):


        import json



        try:


            with open(

                path,

                "w",

                encoding="utf-8"

            ) as file:


                json.dump(

                    data,

                    file,

                    indent=4,

                    ensure_ascii=False

                )



            return True



        except Exception:


            return False







# ==========================================================
# MODULE INFORMATION
# ==========================================================


MODULE_NAME = "CyberScope Intelligence Engine"

MODULE_VERSION = "2.0"

MODULE_AUTHOR = "CyberScope"

MODULE_TYPE = "OSINT Intelligence"







# ==========================================================
# SELF TEST
# ==========================================================


def self_test():


    print("=" * 60)

    print(MODULE_NAME)

    print("Version:", MODULE_VERSION)

    print("=" * 60)



    target = input(

        "Target Domain/URL : "

    ).strip()



    if not target:


        print(

            "Target required"

        )

        return




    engine = IntelligenceEngine()



    print(

        "\nCollecting intelligence...\n"

    )



    result = engine.scan(

        target

    )



    report = IntelligenceReport.create(

        result

    )



    IntelligenceExporter.save_json(

        report

    )



    print(

        "Report saved: intelligence_report.json"

    )



    print(

        "\nSummary"

    )


    print(

        IntelligenceReport.summary(

            result

        )

    )







# ==========================================================
# DIRECT EXECUTION
# ==========================================================


if __name__ == "__main__":


    self_test()
