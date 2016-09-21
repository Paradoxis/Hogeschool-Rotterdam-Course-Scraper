import re
import time

import demjson
from bs4 import BeautifulSoup
from threading import Thread, BoundedSemaphore
from hr.browser import HrBrowser


class OsirisScraper:
    """
    Osiris Scraper to allow easy access to data within the platform
    Currently only limited to scraping course details
    """

    def __init__(self, username, password, auto_login=False):
        """
        Scraper constructor
        :param username: Username to log into the platform with
        :param password: Password to log into the platform with
        :param auto_login: Should the class automatically log in after instantiating the object?
        """
        self.lock = BoundedSemaphore()
        self.browser = HrBrowser(username, password)
        self.request_token = None

        if auto_login:
            self.login()

    def login(self):
        """
        Log into OSIRIS
        :return: void
        """
        if not self.browser.login_osiris():
            raise OsirisScraperException("Failed to log into OSIRIS")

    def get_request_token(self):
        """
        Get the request token (CSRF token)
        :return: string
        """
        if self.request_token:
            return self.request_token
        else:
            response = self.browser.get("https://student.osiris.hro.nl:9021/osiris_student/Onderwijs.do")
            content = BeautifulSoup(response.content, "lxml")
            self.request_token = content.find("input", {"id": "requestToken"}).attrs["value"]
            return self.request_token

    def get_courses_length(self, year):
        """
        Gets the amount of courses
        :param year: What year?
        :type year: int
        :return: int
        """
        response = self.get_courses_length_request(year)
        return int(re.findall(r'De volgende ([0-9]+) cursussen voldoen aan de opgegeven criteria.', response.content).pop())

    def get_courses_length_request(self, year):
        """
        Make the request to fetch the amount of courses
        :param year: What year?
        :type year: int
        :return: requests.Response
        """
        return self.browser.post("https://student.osiris.hro.nl:9021/osiris_student/OnderwijsZoekCursus.do", {
            "startUrl": "OnderwijsZoekCursus.do",
            "inPortal": "",
            "callDirect": "",
            "requestToken": self.get_request_token(),
            "jaar_1": year,
            "zoek": "",
            "toon": "",
            "aanvangs_blok": "geenVoorkeur",
            "timeslot": "geenVoorkeur",
            "cursustype": "geenVoorkeur",
            "faculteit": "geenVoorkeur",
            "organisatieonderdeel": "geenVoorkeur",
            "vrij_veld_1": "KEUZEVAK",
            "vrij_veld_1_naam": "VAKSOORT",
            "voertaal": "geenVoorkeur",
            "event": "zoeken",
            "source": "jaar_1",
            "cursuscode": "",
            "korteNaamCursus": "",
            "collegejaar": "",
            "faculteitCursus": "",
            "aanvangsblok": ""
        })

    def get_courses(self, year):
        """
        Get a list of all courses
        :param year: What year?
        :type year: int
        :return: list
        """
        amount = self.get_courses_length(year=year)
        courses = []

        for i in range(0, amount, 30):
            t = Thread(target=self.get_course_list, args=(i, courses))
            t.start()

        while len(courses) < amount:
            time.sleep(0.25)

        return courses

    def get_course_list(self, step_index, courses):
        """
        Get a list of courses starting at a given step index
        :param step_index: Step index to start at
        :param courses: Reference to the courses list
        :type step_index: int
        :type courses: list
        :return: void
        """
        response = self.browser.get("https://student.osiris.hro.nl:9021/osiris_student/OnderwijsZoekCursus.do", params={
            "event": "goto",
            "source": "OnderwijsZoekCursus",
            "value": step_index + 1,
            "size": "30",
            "partialTargets": "OnderwijsZoekCursus _uixState",
            "partial": "true",
            "requestToken": self.get_request_token()
        })

        for index, row in enumerate(BeautifulSoup(response.content, "lxml").find("table", {"class": "OraTableContent"}).find_all("tr")):
            if not index == 0:
                course = self.get_course_info(course_row=row)
                courses.append(course)

                self.lock.acquire()
                print("[+] Scraped course metadata: %s (%s)" % (course["korteNaamCursus"].encode("utf-8"), course["cursuscode"].encode("utf-8")))
                self.lock.release()

    def get_course_info(self, course_row):
        """
        Get the info related to a specific row (HTML table)
        :param course_row: Current row to inspect
        :return: dict
        """
        course = re.findall(r'submitForm\(\'form0\',1,({.*})\);', course_row.find("td").find("a").attrs["onclick"]).pop()
        course = demjson.decode(course)
        course["studiePunten"] = course_row.find_all("td")[6].string
        del course["event"]
        return course

    def get_course_text(self, course, year):
        """
        Get the text related to a course independently from the fetch loop
        :param course: The course details
        :type course: dict
        :param year: What year?
        :type year: int
        :return: string
        """
        response = self.get_course_text_request(course=course, year=year)
        text = str(BeautifulSoup(response.content, "lxml").find("span", {"id": "curs"}))

        self.lock.acquire()
        print("[+] Scraped course text: %s (%s)" % (course["korteNaamCursus"], course["cursuscode"]))
        self.lock.release()

        return text

    def get_course_text_request(self, course, year):
        """
        Make the 'get_course_text' request
        :param course: The course details
        :type course: dict
        :param year: What year?
        :type year: int
        :return: requests.Request
        """
        return self.browser.post("https://student.osiris.hro.nl:9021/osiris_student/OnderwijsZoekCursus.do", {
            "startUrl": "OnderwijsZoekCursus.do",
            "inPortal": "",
            "callDirect": "",
            "requestToken": self.get_request_token(),
            "jaar_1": year,
            "zoek": "",
            "toon": "",
            "aanvangs_blok": "geenVoorkeur",
            "timeslot": "geenVoorkeur",
            "cursustype": "geenVoorkeur",
            "faculteit": "geenVoorkeur",
            "organisatieonderdeel": "geenVoorkeur",
            "vrij_veld_1": "KEUZEVAK",
            "vrij_veld_1_naam": "VAKSOORT",
            "voertaal": "geenVoorkeur",
            "event": "selectCursus",
            "source": "",
            "cursuscode": course["cursuscode"],
            "korteNaamCursus": course["korteNaamCursus"],
            "collegejaar": course["collegejaar"],
            "faculteitCursus": course["faculteitCursus"],
            "aanvangsblok": course["aanvangsblok"]
        })


class OsirisScraperException(Exception):
    pass