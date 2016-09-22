# Hogeschool Rotterdam - Osiris Course Scraper 
<sup>Also an authentication library, just because</sup>

Rather than going through the absolute hell that is the school system called 'OSIRIS', I decided to just write a scraper and generate a beautiful and searchable website to do the same instead. Also a full website authentication 'framework' that allows easy access to HINT documents in scripts.

This was code written in a few hours, I had no intention of making it 'pretty' or 'perfect', so excuse my code if it's messy.

## Scraper usage
To use the scraper, simply install the required libraries and run the script `scraper.py`.

```plain
$ pip install -r requirements.txt
$ python scraper.py --username <hogeschool rotterdam student id> --password <i'm not even explaining this one>
```

## Website installation
To install the website, you'll need a (preferably linux based) web server with PHP 7+ and [Phalcon 3.X](https://phalconphp.com/en/) installed. Then just clone the repository, mark the directory `website/keuzecursussen/public/` as your web root and you're good to go! No database needed at all.

## Authentication library usage
Since I had to figure out the entire login system for the school, I might as well share that as an easy-to-use library, right?

To use it, simply create a new instance of `hr.browser.HrBrowser` and use the login methods. The class is a subclass of `requests.Session` so it will have all the features you're used to in the [requests](http://docs.python-requests.org/en/master/) library. All `login` methods return true on a successful login.

```python
# Import the HrBrowser class
from hr.browser import HrBrowser

# Instantiate a new browser object
browser = HrBrowser(username="<your username>", password="<your password>")

# Log in using any of these methods to your service of choice
browser.login()           # -> bool, log into the global `login.hro.nl` domain
browser.login_natschool() # -> bool, log into the natschool service
browser.login_myfiles()   # -> bool, log into the myfiles service
browser.login_osiris()    # -> bool, log into the osiris service
browser.login_hint()      # -> bool, log into the hint service

# Once you've logged into one of the five services
# you can use the class like any other `requests.Session` object 
# but request internal web pages that reside behind a login wall too
browser.get("https://hint.hro.nl/example") # -> requests.Response

```

# Disclaimer
I am not responsible if you get in trouble for using these tools, they can be considered 'noisy' as they make a lot of HTTP(S) GET and POST requests, hosting the data publicly may also not be allowed (I'm assuming it is until I get asked to take it down).

# License
MIT License

Copyright (c) 2016 - Luke Paris (Paradoxis)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
