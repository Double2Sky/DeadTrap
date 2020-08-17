import os
import selenium
import requests
from configobj import ConfigObj
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import time
import sys
from html.parser import HTMLParser
import json
from deadtrap.SocialMedia.scrapefb import fb
from deadtrap.SocialMedia.scrapetwitter import twit
from deadtrap.SocialMedia.scrapelinkedin import linked
from deadtrap.Info.Spamcalls import risk
from deadtrap.Info.fouroneone import fouroneone
from deadtrap.Info.google import trace
from deadtrap.Info.googlemaps import maps
from deadtrap.Style.banner import banner

DEFAULT_NUMVERIFY_API_KEY = "a65976cc48a83b234e1b7177d0b3840f"
CONFIG_FILE = os.path.join(
    os.path.expanduser("~"),
    ".config",
    "deadtrap",
    "deadtrap.conf"
)

n = []

class colors:
    yellow =  '\033[1;33m'
    green =  '\033[1;32m'
    red =   '\033[1;31m'
    magenta = '\033[1;35m'
    darkwhite = '\033[0;37m'
    reset = '\033[0m'

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataArray = []
        self.countLanguages = 0
        self.lasttag = None
        self.lastname = None
        self.lastvalue = None

    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'h1':
            for name, value in attrs:
                if name == 'class' and value == 'flex-1 text-xl text-fontPrimaryColor leading-tight':
                    self.countLanguages += 1
                    self.inLink = True
                    self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == "h1":
            self.inlink = False

    def handle_data(self, data):
        if self.lasttag == 'h1' and self.inLink and data.strip():
            print(colors.green + "Name : " + data + colors.green)
            
class HTML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataArray = []
        self.countLanguages = 0
        self.lasttag = None
        self.lastname = None
        self.lastvalue = None

    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'flex-1 h-16 leading-16 border-b border-borderColor truncate pr-4':
                    self.countLanguages += 1
                    self.inLink = True
                    self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == "div":
            self.inlink = False

    def handle_data(self, data):
	    if self.lasttag == 'div' and self.inLink and data.strip():
		    if "@" in data:
			    print(colors.magenta + "Email : " + data + colors.magenta)
		    else:
			    pass


def get_config():
    numverify_api_key = DEFAULT_NUMVERIFY_API_KEY
    config = {}
    if os.path.isfile(CONFIG_FILE):
        config = ConfigObj(CONFIG_FILE)

        if "numverify_api_key" in config["deadtrap"] and config["deadtrap"]["numverify_api_key"]:
            numverify_api_key = config["deadtrap"]["numverify_api_key"]

    return numverify_api_key


def query_numverify(numverify_api_key, phone_number):
    response = requests.get(f'http://apilayer.net/api/validate?access_key={numverify_api_key}&number={phone_number}')

    if response.status_code != 200:
        raise Exception(f"Got HTTP status code {response.status_code} from numverify API")

    answer = json.loads(response.text)

    if "success" in answer and answer["success"] is False:
        error_code = answer['error']['code']
        error_msg = (
            f"{colors.red}Error from numverify API{colors.reset} -- Code: {error_code}, "
            f"Info: {answer['error']['info']}"
        )

        if error_code == 104 and numverify_api_key == DEFAULT_NUMVERIFY_API_KEY:
            error_msg += (
                f"\n\n{colors.yellow}NOTE{colors.reset}: A default numverify API "
                "key is provided with DeadTrap for convenience, but it is currently "
                "exhausted. Please follow the instructions at "
                "https://github.com/Chr0m0s0m3s/DeadTrap#numverify-api to configure "
                "DeadTrap with your own numverify api key."
            )
        raise Exception(error_msg)

    return answer

def query_truecaller(browser, phone_number, country_code):
    browser.get(f"https://www.truecaller.com/search/{str(country_code).lower()}/{phone_number.replace('+91', '')}")


    if browser.current_url == 'https://www.truecaller.com/auth/sign-in':
        actionchains = ActionChains(browser)

        click = browser.find_element_by_xpath('/html/body/div/main/div/a[2]')

        actionchains.move_to_element(click).click().perform()

        time.sleep(20)
        email = browser.find_element_by_css_selector('#i0116')
        email.send_keys('rubenrobinson82@outlook.com', Keys.ENTER)

        time.sleep(20)
        password = browser.find_element_by_css_selector('#i0118')
        password.send_keys('mq2jvgzH', Keys.ENTER)

        time.sleep(30)

    parser = MyHTMLParser()
    parser.feed(browser.page_source)

def main():
    numverify_api_key = get_config()
    banner()
    query = input(colors.green + "\n└──=>Enter the phone number (along with prefix) :")

    line_1 = "\nRunning Scan..."

    for x in line_1:
        print(x, end='')
        sys.stdout.flush()
        time.sleep(0.1)
    try:
        answer = query_numverify(numverify_api_key, query)
    except Exception as ex:
        print("\n\n" + str(ex))
        exit(1)

    optionss = webdriver.FirefoxOptions()
    optionss.headless = True
    optionss.add_argument("--disable-popup-blocking")
    optionss.add_argument("--disable-extensions")

    browser = webdriver.Firefox(options=optionss)

    parse = HTML()


    print(colors.red+"\nInfo Scan\n"+colors.red)
    print(colors.red+"------------------------"+colors.red)

    try:
        query_truecaller(browser, query, answer['country_code'])
    except Exception as ex:
        print(colors.yellow + "\n\nWARNING: " + colors.reset + "Failed to query truecaller.com: " + str(ex))

    print(colors.green+f'''
    Valid : {str(answer['valid'])}
    Number: {str(answer['number'])}
    Local Format: {str(answer['local_format'])}
    International Format: {str(answer['international_format'])}
    Country Prefix: {str(answer['country_prefix'])}
    Country Code: {str(answer['country_code'])}
    Country Name: {str(answer['country_name'])}
    Location: {str(answer['location'])}
    Maps : {maps(str(answer['location']))}
    Carrier: {str(answer['carrier'])}
    Line Type: {str(answer['line_type'])}'''+colors.green)
        
    print("")
    print(colors.magenta + "[*] Scanning Social Media Footprints" + colors.magenta)
    print("-------------------------------------")
    print("")
    print(fb(query))
    print("")
    print(twit(query))
    print("")
    print(linked(query))
    print("")
    parse.feed(browser.page_source)
    print("")

    print(colors.darkwhite + "Spamcalls.net Search" + colors.darkwhite)
    print("------------")
    print("")
    print(risk(query))

    print(colors.darkwhite + "\n411.com search" + colors.darkwhite)
    print("------------")
    print("")
    print(fouroneone(query))

    print(colors.red + "\nGoogle Exception Results")
    print(colors.red + "-------------")
    print("")
    print(trace(query))
    print("")
    browser.quit()

if __name__ == "__main__":
    main()
