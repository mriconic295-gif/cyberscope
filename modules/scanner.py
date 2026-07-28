"""
=========================================================
CyberScope
Scanner Engine

Network & Web Scanner Module

Version : 2.0
=========================================================
"""


from __future__ import annotations


import socket
import time


import requests


from urllib.parse import urlparse


from concurrent.futures import ThreadPoolExecutor





# ==========================================================
# SCANNER SESSION
# ==========================================================


class ScannerSession:



    def __init__(self):


        self.session = requests.Session()



        self.session.headers.update({

            "User-Agent":

            "CyberScope Scanner Engine"

        })



        self.timeout = 8





    def request(self,url):


        return self.session.get(

            url,

            timeout=self.timeout,

            allow_redirects=True

        )






# ==========================================================
# URL SCANNER
# ==========================================================


class URLScanner:



    def check(self,url):


        try:


            start = time.time()



            response = ScannerSession().request(

                url

            )



            elapsed = round(

                time.time()-start,

                3

            )



            return {


                "url":

                    url,



                "status":

                    response.status_code,



                "response_time":

                    elapsed,



                "size":

                    len(

                        response.content

                    )

            }





        except Exception as error:


            return {


                "url":

                    url,



                "error":

                    str(error)

            }








# ==========================================================
# DOMAIN RESOLVER
# ==========================================================


class DomainResolver:



    def resolve(self,target):


        try:


            if target.startswith(

                "http"

            ):


                hostname = urlparse(

                    target

                ).hostname



            else:


                hostname = target




            ip = socket.gethostbyname(

                hostname

            )



            return {


                "hostname":

                    hostname,



                "ip":

                    ip

            }




        except Exception as error:


            return {


                "error":

                    str(error)

            }







# ==========================================================
# PORT CHECKER
# ==========================================================


class PortChecker:



    COMMON_PORTS = {


        21:

            "FTP",



        22:

            "SSH",



        25:

            "SMTP",



        53:

            "DNS",



        80:

            "HTTP",



        443:

            "HTTPS",



        3306:

            "MYSQL",



        5432:

            "POSTGRESQL",



        8080:

            "HTTP-ALT"

    }





    def check_port(self,host,port):


        try:


            sock = socket.socket()



            sock.settimeout(

                1

            )



            result = sock.connect_ex(

                (

                    host,

                    port

                )

            )



            sock.close()



            return {


                "port":

                    port,



                "service":

                    self.COMMON_PORTS.get(

                        port,

                        "Unknown"

                    ),



                "open":

                    result == 0

            }





        except Exception as error:


            return {


                "port":

                    port,



                "error":

                    str(error)

            }








# ==========================================================
# SERVICE INFORMATION
# ==========================================================


class ServiceInformation:



    def identify(self,host,port):


        try:


            service = socket.getservbyport(

                port

            )


            return {


                "port":

                    port,



                "service":

                    service

            }





        except Exception:


            return {


                "port":

                    port,



                "service":

                    "Unknown"

            }
          # ==========================================================
# MULTI THREAD PORT SCANNER
# ==========================================================


class PortScannerEngine:



    def __init__(self):


        self.checker = PortChecker()





    def scan(self,host,ports=None):


        if ports is None:


            ports = list(

                self.checker.COMMON_PORTS.keys()

            )



        results = []



        with ThreadPoolExecutor(

            max_workers=20

        ) as executor:


            jobs = [


                executor.submit(

                    self.checker.check_port,

                    host,

                    port

                )

                for port in ports

            ]



            for job in jobs:


                try:


                    results.append(

                        job.result()

                    )


                except Exception as error:


                    results.append({

                        "error":

                            str(error)

                    })



        return results






# ==========================================================
# SCAN PROFILE
# ==========================================================


class ScanProfile:



    PROFILES = {



        "quick":{


            "ports":[

                80,

                443

            ],


            "name":

                "Quick Scan"

        },



        "standard":{


            "ports":

                list(

                    PortChecker.COMMON_PORTS.keys()

                ),


            "name":

                "Standard Scan"

        },



        "web":{


            "ports":[

                80,

                443,

                8080

            ],


            "name":

                "Web Scan"

        }



    }




    def get(self,name):


        return self.PROFILES.get(

            name,

            self.PROFILES["standard"]

        )







# ==========================================================
# WEB ENDPOINT SCANNER
# ==========================================================


class WebEndpointScanner:



    COMMON_ENDPOINTS = [


        "/",

        "/robots.txt",

        "/sitemap.xml",

        "/favicon.ico",

        "/login",

        "/admin"



    ]





    def scan(self,base_url):


        results = []



        for endpoint in self.COMMON_ENDPOINTS:


            try:


                url = base_url.rstrip("/") + endpoint



                response = ScannerSession().request(

                    url

                )



                results.append({


                    "endpoint":

                        endpoint,



                    "status":

                        response.status_code,



                    "available":

                        response.status_code < 400



                })



            except Exception as error:



                results.append({


                    "endpoint":

                        endpoint,



                    "error":

                        str(error)

                })



        return results






# ==========================================================
# SCAN RESULT FORMATTER
# ==========================================================


class ScanResultFormatter:



    @staticmethod

    def format(data):


        return {


            "CyberScope":

                {


                    "module":

                        "Scanner Engine",



                    "version":

                        "2.0"

                },



            "scan":

                data

        }






# ==========================================================
# SCAN STATISTICS
# ==========================================================


class ScanStatistics:



    def generate(self,ports):


        total = len(

            ports

        )



        opened = len([


            port

            for port in ports

            if port.get(

                "open"

            )



        ])





        return {


            "total_ports":

                total,



            "open_ports":

                opened,



            "closed_ports":

                total-opened



        }
      # ==========================================================
# MAIN SCANNER ENGINE
# ==========================================================


class ScannerEngine:



    def __init__(self):


        self.resolver = DomainResolver()


        self.url_scanner = URLScanner()


        self.port_scanner = PortScannerEngine()


        self.profile = ScanProfile()


        self.endpoint = WebEndpointScanner()


        self.statistics = ScanStatistics()






    # ======================================================
    # COMPLETE SCAN
    # ======================================================


    def scan(self,target,profile="standard"):


        result = {


            "target":

                target,



            "network":

                {},



            "web":

                {},



            "statistics":

                {}

        }





        # ----------------------------------
        # Resolve Domain
        # ----------------------------------


        resolved = self.resolver.resolve(

            target

        )


        result["network"]["resolver"] = resolved




        if "error" in resolved:


            return result




        host = resolved.get(

            "hostname"

        )





        # ----------------------------------
        # Port Scan
        # ----------------------------------


        scan_profile = self.profile.get(

            profile

        )



        ports = scan_profile.get(

            "ports"

        )



        port_result = self.port_scanner.scan(

            host,

            ports

        )



        result["network"]["ports"] = port_result




        result["statistics"] = self.statistics.generate(

            port_result

        )





        # ----------------------------------
        # Website Check
        # ----------------------------------


        if target.startswith(

            "http"

        ):


            url = target


        else:


            url = "https://" + target





        result["web"]["availability"] = (

            self.url_scanner.check(

                url

            )

        )




        result["web"]["endpoints"] = (

            self.endpoint.scan(

                url

            )

        )





        return result






# ==========================================================
# SCAN PIPELINE
# ==========================================================


class ScanPipeline:



    def __init__(self):


        self.engine = ScannerEngine()





    def execute(self,target):


        data = self.engine.scan(

            target

        )



        return {


            "pipeline":

                "completed",



            "data":

                data

        }








# ==========================================================
# DASHBOARD DATA BUILDER
# ==========================================================


class DashboardScannerData:



    @staticmethod

    def build(scan):


        statistics = scan.get(

            "statistics",

            {}

        )



        return {


            "cards": [



                {


                    "title":

                        "Open Ports",



                    "value":

                        statistics.get(

                            "open_ports",

                            0

                        )

                },



                {


                    "title":

                        "Total Checked",



                    "value":

                        statistics.get(

                            "total_ports",

                            0

                        )

                },



                {


                    "title":

                        "Closed Ports",



                    "value":

                        statistics.get(

                            "closed_ports",

                            0

                        )

                }



            ]

        }







# ==========================================================
# SCAN HISTORY STRUCTURE
# ==========================================================


class ScanHistory:



    def __init__(self):


        self.history = []





    def add(self,data):


        self.history.append(

            data

        )





    def get_all(self):


        return self.history
      # ==========================================================
# SCAN REPORT EXPORTER
# ==========================================================


class ScanReportExporter:



    @staticmethod

    def create(data):


        return {


            "CyberScope":

                {


                    "module":

                        "Scanner Engine",



                    "version":

                        "2.0",



                    "type":

                        "Network & Web Scanner"

                },



            "report":

                data

        }






    @staticmethod

    def save(data,path="scanner_report.json"):


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

                    indent=4

                )



            return True



        except Exception:


            return False






# ==========================================================
# SCAN SUMMARY
# ==========================================================


class ScanSummary:



    @staticmethod

    def generate(data):


        stats = data.get(

            "statistics",

            {}

        )



        return {



            "target":

                data.get(

                    "target"

                ),



            "open_ports":

                stats.get(

                    "open_ports",

                    0

                ),



            "checked_ports":

                stats.get(

                    "total_ports",

                    0

                ),



            "status":

                "Completed"

        }






# ==========================================================
# MODULE INFORMATION
# ==========================================================


MODULE_NAME = "CyberScope Scanner Engine"

MODULE_VERSION = "2.0"

MODULE_AUTHOR = "CyberScope"

MODULE_TYPE = "Network Discovery"







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




    scanner = ScannerEngine()



    print(

        "\nRunning scan...\n"

    )



    result = scanner.scan(

        target

    )



    report = ScanReportExporter.create(

        result

    )



    ScanReportExporter.save(

        report

    )



    print(

        "Report saved: scanner_report.json"

    )



    print(

        "\nSummary"

    )



    print(

        ScanSummary.generate(

            result

        )

    )







# ==========================================================
# DIRECT EXECUTION
# ==========================================================


if __name__ == "__main__":


    self_test()
