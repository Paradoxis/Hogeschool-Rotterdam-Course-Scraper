import os
import json
import datetime
from multiprocessing.pool import ThreadPool
from threading import Thread

from hr.osiris import OsirisScraper, OsirisScraperException
from argparse import ArgumentParser


def output_courses_metadata(courses):
    """
    Outputs the course metadata
    :param courses: list
    :return: void
    """
    with open("courses.json", "w") as output:
        output.truncate()
        output.seek(0)
        output.write(json.dumps(courses))

def output_course_text(course, text):
    """
    Outputs the course text into a file
    :param course: The course metadata
    :param text: The course text
    :return: void
    """
    if not os.path.exists("courses") or not os.path.isdir("courses"):
        os.mkdir("courses")

    with open("courses/%s.html" % course["cursuscode"], "w") as output:
        output.truncate()
        output.seek(0)
        output.write(text)


def scrape_course_text(course, year, scraper):
    """
    Scrape an individual courses' text (threaded)
    :param course: Course metadata
    :param year: What year?
    :param scraper: Scraper object
    :return: void
    """
    output_course_text(course, scraper.get_course_text(course=course, year=year))


def scrape(username, password, year):
    """
    Scrape OSIRIS
    :param username: Username to log in with
    :param password: Password to log in with
    :param year: Year to scrape
    :return: void
    """
    try:
        print("OSIRIS course list scraper")
        print("Copyright (c) %d - Luke Paris (Paradoxis)" % datetime.datetime.now().year)
        print("-------------------------------------------------------------")
        print("[*] Logging into OSIRIS.. ")

        scraper = OsirisScraper(username=username, password=password)
        scraper.login()

        print("[*] Starting scraper (year: %d).." % year)
        print("-------------------------------------------------------------")
        print("")
        print("[*] Fetching metadata..")

        courses = scraper.get_courses(year=year)
        output_courses_metadata(courses)

        print("-------------------------------------------------------------")
        print("[*] Done! Wrote metadata to: courses.json")
        print("")
        print("[*] Fetching course text (wait for it..)")
        print("[*] Course text will be stored in: courses/{course code}.html")
        print("-------------------------------------------------------------")

        pool = ThreadPool()

        for course in courses:
            pool.apply_async(scrape_course_text, args=(course, year, scraper))

        pool.close()
        pool.join()

    except OsirisScraperException or KeyboardInterrupt as e:
        print("-------------------------------------------------------------")
        print("\b\b[!] Error: %s" % e)


def main():
    """
    Main entry point of the scraper
    :return: void
    """

    # Parse CLI arguments
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", type=str, help="Username to log into OSIRIS with", required=True)
    parser.add_argument("-p", "--password", type=str, help="Password to log into OSIRIS with", required=True)
    parser.add_argument("-y", "--year", type=int, help="What year to scrape", default=datetime.datetime.now().year)
    options = parser.parse_args()

    # Scrape OSIRIS
    scrape(username=options.username, password=options.password, year=options.year)

if __name__ == '__main__':
    main()