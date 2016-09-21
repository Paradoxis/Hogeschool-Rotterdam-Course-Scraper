from requests import Session
from bs4 import BeautifulSoup


class HrBrowser(Session):
    """
    Hogeschool Rotterdam Browser
    Used to log into the official HR website and perform requests on the users' behalf
    """

    def __init__(self, username, password, auto_login=False):
        """
        Hogeschool Rotterdam Browser constructor
        :param username: Username used to log into your HR account
        :param password: Password used to log into your HR account
        :type username: str
        :type password: str
        """
        super(HrBrowser, self).__init__()

        self.username = username
        self.password = password

        self.login_platforms = {
            "osiris": "https://student.osiris.hro.nl:9021/osiris_student/LoginDirect.do",
            "natschool": "http://natschool.hro.nl/Security/cwips/Login.aspx?redirectUrl=http://natschool.hro.nl/",
            "myfiles": "https://myfiles.hro.nl/index.php",
            "hint": "http://hint.hro.nl/nl/Home/"
        }

        if auto_login:
            if not self.login():
                raise HrBrowserException("Failed to log into the HR login portal")

    def get_login_page(self):
        """
        Get the login page from the
        :return: requests.Response
        """
        return self.get("https://login.hro.nl/v1/login")

    def get_login_csrf_token(self, login_page=None):
        """
        Get the CSRF token from the login page
        :return: string|None
        """
        response = (login_page if login_page else self.get_login_page())
        csrf_field = BeautifulSoup(response.content, "lxml").find("input", {"name": "lt"})
        return csrf_field.attrs["value"] if csrf_field else None

    def login_successful(self, login_page):
        """
        Check if the current session is logged in or not
        :return: bool
        """
        return "logged in as" in (login_page if login_page else self.get_login_page()).content

    def login(self, params=None):
        """
        Log the current browser in
        :param params: Custom parameters to pass to the login request (used in platform requests)
        :type params: dict
        :return: void
        """
        login_page = self.get_login_page()
        csrf_token = self.get_login_csrf_token(login_page=login_page)

        if not self.login_successful(login_page=login_page):
            response = self.login_post_request(csrf_token=csrf_token, params=params)
            return self.login_successful(login_page=response)
        else:
            return True

    def login_post_request(self, csrf_token=None, params=None):
        """
        Perform a login POST request
        :param csrf_token: The CSRF token obtained from the login page
        :param params: Custom parameters to pass to the login request (used in platform requests)
        :type csrf_token: str
        :type params: dict
        :return: requests.Response
        """
        return self.post("https://login.hro.nl/v1/login", {
            "credentialsType": "ldap",
            "_eventId": "submit",
            "username": self.username,
            "password": self.password,
            "lt": (csrf_token if csrf_token else self.get_login_csrf_token())
        }, params=params)

    def login_platform(self, platform):
        """
        Log into a specific platform
        :param platform: Platform to log into, accepts: "webmail", "osiris", "natschool", "myfiles", "service", "hint"
        :type platform: str
        :return: bool
        """
        if platform not in self.login_platforms:
            platforms = ", ".join(self.login_platforms.keys())
            raise HrBrowserException("Invalid login platform: %s, accepted platforms are: %s" % (platform, platforms))

        if platform == "osiris":
            self.login_osiris()
            return

        if platform == "natschool":
            self.login_natschool()
            return

        if platform == "myfiles":
            self.login_myfiles()
            return

        if platform == "hint":
            self.login_hint()
            return

        raise HrBrowserException("Platform %s not implemented" % platform)

    def login_osiris(self):
        """
        Log into the OSIRIS service
        :return: bool
        """
        self.login_post_request(params={"service_url": self.login_platforms["osiris"], "rcl": 65})
        return self.login_osiris_successful()

    def login_osiris_successful(self):
        """
        Check if the OSIRIS login was successful
        :return: bool
        """
        return self.username in self.get("https://student.osiris.hro.nl:9021/osiris_student/ToonPersonalia.do").content

    def login_natschool(self):
        """
        Log into the natschool service
        :return: bool
        """
        self.login_post_request(params={"service_url": self.login_platforms["natschool"], "allow": "ntt-upt"})
        return self.login_natschool_successful()

    def login_natschool_successful(self):
        """
        Check if the HINT login was successful
        :return: bool
        """
        return self.username in self.get("http://natschool.hro.nl/Pages/DashBoard/DashBoard.aspx?isactive=false").content

    def login_myfiles(self):
        """
        Log into the myfiles service
        :return: bool
        """
        self.login_post_request(params={"service_url": self.login_platforms["myfiles"], "allow": "upt"})
        return self.login_myfiles_successful()

    def login_myfiles_successful(self):
        """
        Check if the HINT login was successful
        :return: bool
        """
        return self.username in self.get("https://myfiles.hro.nl/index.php").content

    def login_hint(self):
        """
        Log into the hint service
        :return: bool
        """
        self.login_post_request(params={"service_url": self.login_platforms["hint"], "allow": "mcr-nt-upt"})
        return self.login_hint_successful()

    def login_hint_successful(self):
        """
        Check if the HINT login was successful
        :return: bool
        """
        return self.username in self.get("http://hint.hro.nl/nl/Home/").content


class HrBrowserException(Exception):
    pass
